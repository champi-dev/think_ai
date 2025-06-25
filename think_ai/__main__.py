"""Main entry point for Think AI CLI."""

import asyncio
import sys

from .cli.main import main

# Ensure GPU usage when available
from .utils.ensure_gpu import gpu_config  # noqa: F401

if __name__ == "__main__":
    # Handle Windows event loop policy
    if sys.platform.startswith("win"):
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    asyncio.run(main())
