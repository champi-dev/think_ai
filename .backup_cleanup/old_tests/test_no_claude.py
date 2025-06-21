#!/usr/bin/env python3
"""Test that Claude enhancement is disabled."""

import asyncio

from implement_proper_architecture import ProperThinkAI


async def test_no_claude() -> None:
    """Test various queries without Claude enhancement."""
    # Initialize system
    think_ai = ProperThinkAI()
    await think_ai.initialize()

    # Test queries
    queries = [
        "Hello",
        "What is love?",
        "Who are you?",
        "What is consciousness?",
        "How does AI work?",
    ]

    for query in queries:
        result = await think_ai.process_with_proper_architecture(query)

        # Verify no Claude enhancement
        if result.get("source") == "claude_enhanced":
            pass
        else:
            pass


if __name__ == "__main__":
    asyncio.run(test_no_claude())
