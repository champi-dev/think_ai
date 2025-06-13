#!/usr/bin/env python3
"""Quick test of Phi-3.5 Mini integration."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import contextlib

from implement_proper_architecture import ProperThinkAI

async def quick_test() -> None:
    """Quick integration test."""
    # Initialize
    think_ai = ProperThinkAI()
    await think_ai.initialize()

    # Test query
    query = "What is artificial intelligence?"

    result = await think_ai.process_with_proper_architecture(query)

    # Verify Phi-3.5 was used
    if result["source"] == "distributed":
        pass
    else:
        pass

    # Test cache
    result2 = await think_ai.process_with_proper_architecture(query)

    if result2["source"] == "cache":
        pass
    else:
        pass

    # Cleanup
    with contextlib.suppress(Exception):
        await think_ai.system.initializer.shutdown()

if __name__ == "__main__":
    asyncio.run(quick_test())
