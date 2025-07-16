#!/usr/bin/env python3
"""Demo Think AI interactions to show functionality."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))


async def demo_interactions() -> Optional[bool]:
    """Demo various Think AI interactions."""
    try:
        import os

        from think_ai.core.think_ai_eternal import create_free_think_ai
        from think_ai.integrations.claude_api import ClaudeAPI

        # Initialize Think AI
        ai = await create_free_think_ai()

        # Initialize Claude API if available
        claude_api = None
        if os.getenv("CLAUDE_API_KEY"):
            claude_api = ClaudeAPI()
            claude_api.get_cost_summary()

        # Demo different types of queries
        queries = [
            ("hello", "🌟 Greeting Test"),
            ("What is consciousness?", "🧠 Deep Question Test"),
            ("help me understand meditation", "🧘 Learning Request Test"),
            ("thank you", "💝 Gratitude Test"),
        ]

        for query, _description in queries:
            # Process with consciousness system
            response = await ai.query_with_cost_awareness(
                query,
                prefer_free=True,
            )

            "FREE" if response["cost"] == 0 else f"${response['cost']:.4f}"

            # Small delay for readability
            await asyncio.sleep(0.5)

        # Show memory status
        await ai.memory.get_memory_status()

        # Show cost summary
        await ai.get_cost_summary()

        if claude_api:
            claude_api.get_cost_summary()

        # Graceful shutdown
        await ai.shutdown("demo_complete")
        if claude_api:
            await claude_api.close()

        return True

    except Exception:
        import traceback

        traceback.print_exc()
        return False


async def main() -> None:
    """Main demo function."""
    success = await demo_interactions()

    if success:
        pass
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
