#! / usr / bin / env python3

"""Quick test with 10 iterations to verify fixes."""

import asyncio
import sys
import time
from pathlib import Path

from implement_proper_architecture import ProperThinkAI
from think_ai.utils.logging import get_logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

logger = get_logger(__name__)


async def test_10_iterations():
"""Run 10 quick iterations."""
# Initialize WITHOUT cache to ensure real services
    think_ai = ProperThinkAI(enable_cache=False)

    start_init = time.time()
    await think_ai.initialize()
    time.time() - start_init

# Simple test questions
    questions = [
    "What is 2 + 2?",
    "What is consciousness?",
    "How does ScyllaDB work?",
    "What is Python?",
    "Explain AI ethics",
    "What is the sun?",
    "How do computers work?",
    "What is machine learning?",
    "Explain quantum computing",
    "What is a nuclear reactor?",
    ]

    success_count = 0
    total_time = 0

    for i, question in enumerate(questions):

        start_time = time.time()
        try:
            response_data = await think_ai.process_with_proper_architecture(question)
            response = response_data.get("response", "No response")
            query_time = time.time() - start_time
            total_time + = query_time

# Check for actual response (not error or generic)
            if response and len(response) > 20 and "error" not in response.lower():
                success_count + = 1
            else:
                pass

            except Exception as e:
                logger.exception(f"Query {i + 1} failed: {e}")

# Summary

                await think_ai.shutdown()

                return success_count = = 10  # Return True if all succeeded

            if __name__ = = "__main__":
                success = asyncio.run(test_10_iterations())
                sys.exit(0 if success else 1)
