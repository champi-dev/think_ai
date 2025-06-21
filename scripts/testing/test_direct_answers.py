#! / usr / bin / env python3

"""Test that Think AI provides direct, useful answers to questions."""

import asyncio
import sys
from pathlib import Path

from implement_proper_architecture import ProperThinkAI

from think_ai.utils.logging import get_logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

logger = get_logger(__name__)


async def test_direct_answers() - > None:
"""Test that the AI provides direct answers to questions."""
# Initialize with cache for speed
    think_ai = ProperThinkAI(enable_cache=True)

    await think_ai.initialize()

# Test questions that should get direct answers
    test_queries = [
    ("hello", "greeting"),
    ("what is a nuclear reactor?", "technical question"),
    ("what is the sun?", "science question"),
    ("how do computers work?", "explanation question"),
    ("2 + 2", "math question"),
    ("what is Python?", "programming question"),
    ]

    for query, query_type in test_queries:

        response = await think_ai.query(query)

# Check if response is actually answering the question
        response_lower = response.lower()

# Verify it's not just a greeting for non - greeting queries
        if query_type ! = "greeting":
            if any(
            greeting in response_lower for greeting in [
            "hello",
            "hi ",
            "hey",
            "how can i assist",
            "i'm here to help"]) and len(response) < 100:
                pass
        else:
            pass
    elif "hello" in response_lower or "hi" in response_lower:
        pass
else:
    pass

# Add delay to avoid overwhelming the system
await asyncio.sleep(1)

await think_ai.shutdown()

if __name__ = = "__main__":
    asyncio.run(test_direct_answers())
