#!/usr/bin/env python3
"""Test simple response functionality without loading large models."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))


async def test_simple_response() -> Optional[bool]:
    """Test basic response functionality."""
    try:
        from think_ai.core.think_ai_eternal import create_free_think_ai

        # Initialize Think AI
        ai = await create_free_think_ai()

        # Test consciousness-based response (which should work without large model)

        # Directly test the consciousness system
        await ai.engine.consciousness.generate_conscious_response("hello")

        # Test memory status
        await ai.memory.get_memory_status()

        # Test cost summary
        await ai.get_cost_summary()

        # Clean shutdown
        await ai.shutdown("test_complete")

        return True

    except Exception:
        import traceback

        traceback.print_exc()
        return False


async def main() -> None:
    """Main test function."""
    success = await test_simple_response()

    if success:
        pass
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
