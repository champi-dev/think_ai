"""Alternative logging configuration without structlog dependency."""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class StructuredLogger:
    """A simple structured logger that mimics structlog interface."""

    def __init__(self, name: str, context: Dict[str, Any] = None):
        self.logger = logging.getLogger(name)
        self.context = context or {}
        self._context = self.context.copy()

    def bind(self, **kwargs) -> "StructuredLogger":
        """Bind additional context to the logger."""
        new_logger = StructuredLogger(self.logger.name, self.context)
        new_logger._context.update(kwargs)
        return new_logger

    def _format_message(self, msg: str, **kwargs) -> str:
        """Format message with context."""
        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "logger": self.logger.name,
            "message": msg,
            **self._context,
            **kwargs,
        }
        return json.dumps(data)

    def debug(self, msg: str, **kwargs):
        self.logger.debug(self._format_message(msg, **kwargs))

    def info(self, msg: str, **kwargs):
        self.logger.info(self._format_message(msg, **kwargs))

    def warning(self, msg: str, **kwargs):
        self.logger.warning(self._format_message(msg, **kwargs))

    def error(self, msg: str, **kwargs):
        self.logger.error(self._format_message(msg, **kwargs))

    def exception(self, msg: str, **kwargs):
        self.logger.exception(self._format_message(msg, **kwargs))


def configure_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    json_logs: bool = False,
) -> StructuredLogger:
    """Configure structured logging for the application."""
    # Configure Python's logging
    log_format = "%(message)s" if json_logs else "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging.basicConfig(
        format=log_format,
        stream=sys.stdout,
        level=getattr(logging, log_level.upper()),
    )

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(log_format))
        logging.getLogger().addHandler(file_handler)

    return StructuredLogger("think_ai")


def get_logger(name: str) -> StructuredLogger:
    """Get a logger instance with the given name."""
    return StructuredLogger(name)


class LogContext:
    """Context manager for adding temporary log context."""

    def __init__(self, logger: StructuredLogger, **kwargs) -> None:
        self.logger = logger
        self.context = kwargs
        self.original_context = None

    def __enter__(self):
        self.original_context = self.logger._context.copy()
        self.logger._context.update(self.context)
        return self.logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger._context = self.original_context
