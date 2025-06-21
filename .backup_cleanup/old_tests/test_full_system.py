#!/usr/bin/env python3
"""Test the full distributed Think AI system."""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


async def main() -> None:
    """Run full system test."""
    system = DistributedThinkAI()

    try:
        # Start the system
        await system.start()

        # Test queries
        test_queries = [
            "What is consciousness?",
            "Explain the concept of love in AI systems",
            "How does distributed storage work?",
            "What are the ethical principles of Think AI?",
        ]

        for query in test_queries:
            result = await system.process_with_full_system(query)

            # Show first response
            if result["responses"]:
                first_service = next(iter(result["responses"].keys()))
                response = result["responses"][first_service]
                if isinstance(response, str):
                    pass
                else:
                    pass

        # Health check
        health = await system.initializer.health_check()
        for status in health.values():
            "✅" if status["status"] == "healthy" else "❌"

    except Exception:
        import traceback

        traceback.print_exc()

    finally:
        await system.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
