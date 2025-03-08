import time
from functools import wraps

import structlog

from .config import path_var


def log_method(logger_name: str = None):
    """
    Decorator for logging method calls in services and repositories.

    Args:
        logger_name (str, optional): The name of the logger. Defaults to the class name.

    Returns:
        Callable: The decorated function.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            """
            Wrapper function to log method entry, exit, and exceptions.

            Args:
                self: The instance of the class.
                *args: Positional arguments for the method.
                **kwargs: Keyword arguments for the method.

            Returns:
                Any: The result of the method call.
            """
            logger = structlog.get_logger(logger_name or self.__class__.__name__)
            method_path = f"{self.__class__.__name__}.{func.__name__}"
            previous_path = path_var.get()
            start_time = time.time()

            try:
                path_var.set(method_path)
                logger.debug("Entering method")
                result = await func(self, *args, **kwargs)
                duration_ms = round((time.time() - start_time) * 1000, 2)
                logger.debug("Completed method", duration_ms=duration_ms)
                return result
            except Exception as e:
                duration_ms = round((time.time() - start_time) * 1000, 2)
                logger.exception("Error in method", duration_ms=duration_ms, error=str(e), exc_info=e)
                raise
            finally:
                path_var.set(previous_path)

        return wrapper

    return decorator
