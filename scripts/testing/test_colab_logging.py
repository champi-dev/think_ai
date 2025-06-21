import logging
import time

from colab_logging import setup_colab_logging, test_logging

logger = logging.getLogger(__name__)
"""Test script to verify logging works in Colab."""

# Import the Colab logging setup

# Test 1: Basic logging setup

logger, console = setup_colab_logging("DEBUG")

# Test 2: Direct logging

logger.info("Starting Think AI system...", phase="initialization")
logger.debug("Debug details", memory_usage="256MB", cpu_cores=4)
logger.warning("GPU not detected", fallback="CPU mode")

# Test 3: Console output

console.print("[bold cyan]Think AI System Status[/bold cyan]")
console.print("• Model: [green]Loaded[/green]")
console.print("• Memory: [yellow]Medium Usage[/yellow]")
console.print("• Status: [green]Ready[/green]")

# Test 4: Progress simulation

for i in range(5):
    logger.info(f"Processing step {i + 1}/5", progress=f"{(i + 1)*20}%")
    time.sleep(0.5)

    # Test 5: Error handling

    try:
        msg = "Test error for logging"
        raise ValueError(msg)
    except Exception as e:
        logger.error("Caught an error", error=str(e), exc_info=True)

        # Test 6: Run the built - in test

        test_logging()
