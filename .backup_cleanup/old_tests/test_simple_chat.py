#!/usr/bin/env python3
"""Simple test of Think AI chat."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import contextlib

from implement_proper_architecture import ProperThinkAI

async def test_chat() -> None:
    """Test Think AI responses."""
    ai = ProperThinkAI()
    await ai.initialize()

    queries = [
        "What is passion?",
        "Are you ok?",
        "Hello",
    ]

    for query in queries:

        with contextlib.suppress(Exception):
            await ai.process_with_proper_architecture(query)

    # Cleanup
    await ai.system.shutdown()

if __name__ == "__main__":
    asyncio.run(test_chat())
