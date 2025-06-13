"""Structured logging configuration for Think AI."""

import structlog
import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


def configure_logging(
    log_level: str = "INFO",
    log_file: Optional[Path] = None,
    json_logs: bool = False
) -> structlog.BoundLogger:
    """Configure structured logging for the application."""
    
    # Configure Python's logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper())
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


def get_logger(name: str) -> structlog.BoundLogger:
    """Get a logger instance with the given name."""
    return structlog.get_logger(name)


class LogContext:
    """Context manager for adding temporary log context."""
    
    def __init__(self, logger: structlog.BoundLogger, **kwargs):
        self.logger = logger
        self.context = kwargs
        self.original_context = None
    
    def __enter__(self):
        self.original_context = self.logger._context
        return self.logger.bind(**self.context)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger._context = self.original_context