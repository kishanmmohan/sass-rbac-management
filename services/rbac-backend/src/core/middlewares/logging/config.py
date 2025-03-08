import contextvars
import inspect
import logging
import sys
from datetime import datetime
import structlog
from pydantic import BaseModel

# Context variables for tracking request ID and path
request_id_var = contextvars.ContextVar("request_id", default=None)
path_var = contextvars.ContextVar("path", default=None)


# JSON Serializer
def json_serializer(obj):
    """
    Serialize objects to JSON-compatible format.

    Args:
        obj: The object to serialize.

    Returns:
        str or dict: The serialized object.

    Raises:
        TypeError: If the object type is not serializable.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, BaseModel):
        return obj.dict()
    raise TypeError(f"Type {type(obj)} not serializable")


# Auto Detect Path
def get_auto_path():
    """
    Automatically detect the caller's module and function name.

    Returns:
        str: The detected path in the format 'module.function' or 'class.function'.
    """
    stack = inspect.stack()
    for frame in stack:
        module = frame.frame.f_globals.get("__name__", "unknown")
        function_name = frame.function
        if "self" in frame.frame.f_locals:
            class_name = frame.frame.f_locals["self"].__class__.__name__
            full_method = f"{class_name}.{function_name}"
            if "Repository" in class_name or "Service" in class_name:
                return full_method
    return "unknown"


# Context Injection Processor
def add_context(_, __, event_dict):
    """
    Inject context variables into the log event dictionary.

    Args:
        _ : Unused positional argument.
        __ : Unused positional argument.
        event_dict (dict): The event dictionary to modify.

    Returns:
        dict: The modified event dictionary with context variables.
    """
    request_id = request_id_var.get()
    if request_id:
        event_dict["request_id"] = request_id
    path = get_auto_path()
    if path != "unknown":
        event_dict["path"] = path
    event_dict["message"] = event_dict.pop("event", None)
    event_dict["name"] = event_dict.pop("logger", None)
    ordered_event_dict = {
        "level": event_dict.pop("level", None),
        "name": event_dict.pop("name", None),
        "timestamp": event_dict.pop("timestamp", None),
        "request_id": event_dict.pop("request_id", None),
        "message": event_dict.pop("message", None),
    }
    if "path" in event_dict:
        ordered_event_dict["path"] = event_dict.pop("path")
    ordered_event_dict.update(event_dict)
    return ordered_event_dict


# Configure Structlog
def configure_logging():
    """
    Configure structlog with JSON formatting and console output.
    """
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            add_context,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


# Call the configure_logging function to set up logging
configure_logging()
