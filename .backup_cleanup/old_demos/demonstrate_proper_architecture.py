#!/usr/bin/env python3
"""Demonstrate the properly integrated Think AI architecture without user input."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI

async def main() -> None:
    """Run the proper architecture demonstration."""
    proper_ai = ProperThinkAI()

    try:
        # Initialize system
        await proper_ai.initialize()

        # Test queries
        test_queries = [
            "What is consciousness?",
            "How does Think AI implement ethical principles?",
            "What is consciousness?",  # Duplicate to test cache
            "Explain distributed systems in simple terms",
            "What makes Think AI different from other AI systems?",
        ]

        total_claude_calls = 0

        for _i, query in enumerate(test_queries, 1):

            # Track Claude usage before
            claude_calls_before = proper_ai.claude.request_count

            # Process query
            result = await proper_ai.process_with_proper_architecture(query)

            # Track Claude usage after
            claude_calls_after = proper_ai.claude.request_count
            claude_used = claude_calls_after > claude_calls_before

            for _component, _usage in result["architecture_usage"].items():
                pass

            if claude_used:
                total_claude_calls += 1

            await asyncio.sleep(0.5)

        # Final summary

        # Cost analysis
        proper_ai.claude.get_cost_summary()

        # Test knowledge retrieval

        # Check what was stored
        if "scylla" in proper_ai.services:
            stored_count = 0
            try:
                async for _key, _item in proper_ai.services["scylla"].scan(prefix="interaction_", limit=10):
                    stored_count += 1
            except Exception:
                pass

            # Check cache
            cache_count = 0
            try:
                async for _key, _item in proper_ai.services["scylla"].scan(prefix="query_cache_", limit=10):
                    cache_count += 1
            except Exception:
                pass

    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        await proper_ai.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
