#!/usr/bin/env python3
"""Test graceful shutdown and memory preservation."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))


async def test_graceful_shutdown() -> Optional[bool]:
    """Test graceful shutdown functionality."""
    try:
        from think_ai.core.think_ai_eternal import create_free_think_ai

        # Initialize Think AI
        ai = await create_free_think_ai()

        # Add some interactions to memory
        await ai.query_with_cost_awareness("test message", prefer_free=True)

        # Check memory before shutdown
        await ai.memory.get_memory_status()

        # Test normal shutdown
        await ai.shutdown("test_normal_shutdown")

        # Re-initialize to test memory persistence
        ai2 = await create_free_think_ai()
        await ai2.memory.get_memory_status()

        # Test interrupted shutdown (simulate)
        ai2.memory._emergency_backup_sync()

        # Clean shutdown
        await ai2.shutdown("test_complete")

        return True

    except Exception:
        import traceback

        traceback.print_exc()
        return False


async def main() -> None:
    """Main test function."""
    success = await test_graceful_shutdown()

    if success:
        pass
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
