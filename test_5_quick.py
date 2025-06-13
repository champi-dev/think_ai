#! / usr / bin / env python3

"""Ultra quick test with 5 iterations to verify timeout fixes."""

import asyncio
import sys
import time
from pathlib import Path

from implement_proper_architecture import ProperThinkAI
from think_ai.utils.logging import get_logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

logger = get_logger(__name__)


async def test_5_iterations() - > None:
"""Run 5 quick iterations."""
# Initialize WITH cache for speed
    think_ai = ProperThinkAI(enable_cache=True)

    start_init = time.time()
    await think_ai.initialize()
    time.time() - start_init

# Simple test questions
    questions = [
    "What is 2 + 2?",
    "Hello",
    "What is the sun?",
    "Hi there",
    "What is AI?",
    ]

    for i, question in enumerate(questions):

        start_time = time.time()
        try:
            response_data = await think_ai.process_with_proper_architecture(question)
            response_data.get("response", "No response")
            time.time() - start_time

            except Exception as e:
                logger.exception(f"Query {i + 1} failed: {e}")

                await think_ai.shutdown()

                if __name__ = = "__main__":
                    asyncio.run(test_5_iterations())
