#!/usr/bin/env python3
"""Test the language model fixes."""

import asyncio
import sys
from pathlib import Path
from typing import Optional

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

async def test_language_model() -> Optional[bool]:
    """Test the language model functionality."""
    try:
        from think_ai.core.think_ai_eternal import create_free_think_ai

        # Initialize Think AI
        ai = await create_free_think_ai()

        # Test basic query processing

        # Test with a simple query
        response = await ai.query_with_cost_awareness(
            "hello",
            prefer_free=True,
        )

        "FREE" if response["cost"] == 0 else f"${response['cost']:.4f}"

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
    success = await test_language_model()

    if success:
        pass
    else:
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
