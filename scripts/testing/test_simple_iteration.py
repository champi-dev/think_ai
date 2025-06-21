#! / usr / bin / env python3

"""Simple test to verify iteration system works."""

import asyncio
import sys
import time
from pathlib import Path

from implement_proper_architecture import ProperThinkAI

from think_ai.utils.logging import get_logger

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

logger = get_logger(__name__)


async def test_simple_iterations() - > None:
"""Run a simple 10 iteration test."""
# Initialize with cache for speed
    think_ai = ProperThinkAI(enable_cache=True)

    await think_ai.initialize()

# Simple test questions
    questions = [
    "What is 2 + 2?",
    "What is consciousness?",
    "How does ScyllaDB work?",
    "What is Python?",
    "Explain AI ethics",
    "What is Milvus?",
    "How do neural networks work?",
    "What is Redis used for?",
    "Explain quantum computing",
    "What is machine learning?",
    ]

    for i, question in enumerate(questions):
# Progress indicator
        int((i / len(questions)) * 20)

        start_time = time.time()
        try:
            response_data = await think_ai.process_with_proper_architecture(question)
            response_data.get("response", "No response")
            time.time() - start_time

# Show result

            except Exception as e:
                logger.exception(f"Failed: {e}")

                await think_ai.shutdown()

                if __name__ = = "__main__":
                    asyncio.run(test_simple_iterations())
