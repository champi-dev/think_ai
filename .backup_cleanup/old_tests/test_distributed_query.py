#!/usr/bin/env python3
"""Test the distributed Think AI system with a query."""

import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from think_ai.engine.full_system import DistributedThinkAI


async def main() -> None:
    """Test distributed query processing."""
    system = DistributedThinkAI()

    try:
        # Start system
        await system.start()

        # Test queries
        queries = [
            "What is consciousness?",
            "Explain distributed AI systems",
            "How does love guide artificial intelligence?",
        ]

        for query in queries:
            result = await system.process_with_full_system(query)

            # Show responses
            for response in result["responses"].values():
                if isinstance(response, str) or (isinstance(response, dict) and "response" in response):
                    pass
                else:
                    pass

    except Exception:
        import traceback

        traceback.print_exc()

    finally:
        await system.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
