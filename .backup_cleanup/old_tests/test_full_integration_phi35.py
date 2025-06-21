#!/usr/bin/env python3
"""Test full integration of Phi-3.5 Mini with Think AI architecture."""

import asyncio
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI


async def test_full_integration() -> None:
    """Test that Phi-3.5 Mini is properly integrated."""
    # Initialize system
    think_ai = ProperThinkAI()
    await think_ai.initialize()

    # Test queries
    test_cases = [
        {
            "query": "What is consciousness?",
            "expected_source": "distributed",  # Should use Phi-3.5
            "description": "Philosophy question",
        },
        {
            "query": "Write a Python function to calculate factorial",
            "expected_source": "distributed",  # Should use Phi-3.5
            "description": "Code generation",
        },
        {
            "query": "What is consciousness?",  # Same query
            "expected_source": "cache",  # Should hit cache
            "description": "Cached query",
        },
        {
            "query": "Explain the latest advances in quantum computing from 2024",
            "expected_source": "claude_enhanced",  # Needs recent info
            "description": "Recent information query",
        },
    ]

    results = []

    for _i, test in enumerate(test_cases, 1):
        start = time.time()
        result = await think_ai.process_with_proper_architecture(test["query"])
        elapsed = time.time() - start

        # Check if Phi-3.5 was used
        if (result["source"] == "distributed" and test["expected_source"] == "distributed") or result["source"] == test[
            "expected_source"
        ]:
            pass
        else:
            pass

        results.append(
            {
                "test": test["description"],
                "source": result["source"],
                "time": elapsed,
                "success": result["source"] == test["expected_source"],
            }
        )

    # Summary

    sum(1 for r in results if r["success"])

    sources = {}
    for r in results:
        sources[r["source"]] = sources.get(r["source"], 0) + 1

    for _source, _count in sources.items():
        pass

    # Cleanup
    await think_ai.system.stop()


if __name__ == "__main__":
    asyncio.run(test_full_integration())
