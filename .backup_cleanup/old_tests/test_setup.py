#!/usr/bin/env python3
"""Test Think AI setup without requiring rich terminal."""

import asyncio
import os
import sys
from pathlib import Path
from typing import Optional

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))


async def test_setup() -> Optional[bool]:
    """Test Think AI setup components."""
    try:
        # Test imports
        from think_ai.consciousness import ConsciousnessState
        from think_ai.core.think_ai_eternal import create_free_think_ai
        from think_ai.integrations.claude_api import ClaudeAPI

        # Test Claude API
        if os.getenv("CLAUDE_API_KEY"):
            claude = ClaudeAPI()
            claude.get_cost_summary()
            await claude.close()
        else:
            pass

        # Test consciousness states
        [state.value for state in ConsciousnessState]

        # Test memory initialization (brief test)
        ai = await create_free_think_ai()
        await ai.shutdown("test_complete")

        return True

    except Exception:
        import traceback

        traceback.print_exc()
        return False


async def main() -> None:
    """Main test function."""
    success = await test_setup()

    if success:
        pass
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
