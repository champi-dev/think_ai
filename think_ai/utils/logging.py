"""Structured logging configuration for Think AI."""

import logging
import sys
from pathlib import Path
from typing import Optional

try:
    import structlog

    HAS_STRUCTLOG = True
except ImportError:
    HAS_STRUCTLOG = False
    # Import our alternative implementation
    from .logging_alternative import LogContext as AltLogContext
    from .logging_alternative import StructuredLogger


def configure_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    json_logs: bool = False,
):
    """Configure structured logging for the application."""
    if HAS_STRUCTLOG:
        # Configure Python's logging
        logging.basicConfig(
            format="%(message)s",
            stream=sys.stdout,
            level=getattr(logging, log_level.upper()),
        )

        # Processors for structlog
        processors = [
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
        ]

        if json_logs:
            processors.append(structlog.processors.JSONRenderer())
        else:
            processors.append(structlog.dev.ConsoleRenderer())

        # Configure structlog
        structlog.configure(
            processors=processors,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        # Add file handler if specified
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter("%(message)s"))
            logging.getLogger().addHandler(file_handler)

        return structlog.get_logger()
    else:
        # Use alternative implementation
        from .logging_alternative import configure_logging as alt_configure_logging

        return alt_configure_logging(log_level, log_file, json_logs)


def get_logger(name: str):
    """Get a logger instance with the given name."""
    if HAS_STRUCTLOG:
        return structlog.get_logger(name)
    else:
        from .logging_alternative import get_logger as alt_get_logger

        return alt_get_logger(name)


class LogContext:
    """Context manager for adding temporary log context."""

    def __init__(self, logger, **kwargs) -> None:
        if HAS_STRUCTLOG:
            self.logger = logger
            self.context = kwargs
            self.original_context = None
        else:
            self._alt_context = AltLogContext(logger, **kwargs)

    def __enter__(self):
        if HAS_STRUCTLOG:
            self.original_context = self.logger._context
            return self.logger.bind(**self.context)
        else:
            return self._alt_context.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if HAS_STRUCTLOG:
            self.logger._context = self.original_context
        else:
            self._alt_context.__exit__(exc_type, exc_val, exc_tb)
