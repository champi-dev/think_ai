"""Colab - specific logging configuration for Think AI."""

import builtins
import logging
import sys

import structlog
from rich.console import Console
from rich.logging import RichHandler

# Check if running in Colab
IN_COLAB = "google.colab" in sys.modules


def setup_colab_logging(log_level: str = "INFO"):
"""Configure logging specifically for Google Colab environment."""

# Create Rich console for better output in notebooks
    console = Console(force_terminal=True, width=120)

# Configure Python's logging with RichHandler for better notebook display
    logging.basicConfig(
    level=getattr(logging, log_level.upper()),
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
    RichHandler(
    console=console,
    rich_tracebacks=True,
    markup=True,
    show_time=True,
    show_level=True,
    show_path=True
    )
    ]
    )

# Configure structlog to work with Rich
    structlog.configure(
    processors=[
    structlog.stdlib.filter_by_level,
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.UnicodeDecoder(),
    structlog.processors.CallsiteParameterAdder(
    parameters=[structlog.processors.CallsiteParameter.FILENAME,
    structlog.processors.CallsiteParameter.LINENO]
    ),
    structlog.processors.dict_tracebacks,
    structlog.dev.ConsoleRenderer(colors=True)
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
    )

# Force flush stdout / stderr for immediate output in notebooks
    sys.stdout.flush()
    sys.stderr.flush()

# Create a logger instance
    logger = structlog.get_logger()

# Test logging
    logger.info("🎯 Colab logging configured successfully!",
    environment="Google Colab" if IN_COLAB else "Local",
    log_level=log_level)

    return logger, console


def get_colab_logger(name: str):
"""Get a logger instance configured for Colab."""
    logger = structlog.get_logger(name)
    return logger


# Monkey - patch print to always flush in Colab
if IN_COLAB:
    _original_print = print

    def colab_print(*args, **kwargs):
        kwargs["flush"] = True
        _original_print(*args, **kwargs)

# Replace built - in print
        builtins.print = colab_print

# Test function to verify logging works


        def test_logging():
"""Test all logging mechanisms in Colab."""
            logger, console = setup_colab_logging("DEBUG")

# Test different log levels
            logger.debug("🐛 Debug message", extra_data={"test": True})
            logger.info("ℹ️ Info message", step="testing")
            logger.warning("⚠️ Warning message", important=True)
            logger.error("❌ Error message", error_code=404)

# Test console output
            console.print("\n[bold green]✓ Rich console output working![/bold green]")
            console.print(
            "[yellow]This should appear in the notebook with colors[/yellow]")

# Test regular print (now with auto - flush)
            print("\n📝 Regular print statements are now auto - flushed!")

            return logger, console
