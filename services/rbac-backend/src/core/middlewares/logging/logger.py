import time
import uuid

import structlog
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from .config import path_var, request_id_var


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log requests and responses.

    Attributes:
        logger (structlog.BoundLogger): The logger instance for logging.
    """

    def __init__(self, app):
        """
        Initialize the LoggingMiddleware.

        Args:
            app (FastAPI): The FastAPI application instance.
        """
        super().__init__(app)
        self.logger = structlog.get_logger("api")

    async def dispatch(self, request: Request, call_next):
        """
        Process the incoming request and log the request and response details.

        Args:
            request (Request): The incoming HTTP request.
            call_next (RequestResponseEndpoint): The next middleware or route handler.

        Returns:
            Response: The HTTP response.
        """
        request_id = str(uuid.uuid4())
        request_id_var.set(request_id)
        path_var.set(request.url.path)
        start_time = time.time()

        self.logger.info("Request started", http_method=request.method)

        try:
            response = await call_next(request)
            duration_ms = round((time.time() - start_time) * 1000, 2)
            self.logger.info("Request completed", status_code=response.status_code, duration_ms=duration_ms)
            response.headers["X-Request-ID"] = request_id
            return response
        except Exception as e:
            duration_ms = round((time.time() - start_time) * 1000, 2)
            self.logger.exception("Request failed", exc_info=e, duration_ms=duration_ms)
            raise
        finally:
            path_var.set("")
            request_id_var.set("")


# Get Logger
def get_logger(name: str = "api"):
    """
    Get a structlog logger with the specified name.

    Args:
        name (str): The name of the logger.

    Returns:
        structlog.BoundLogger: The configured logger instance.
    """
    return structlog.get_logger(name)
