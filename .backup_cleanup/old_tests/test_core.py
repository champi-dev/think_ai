#!/usr/bin/env python3
"""Simple test script to verify Think AI core functionality."""

import asyncio
import os
from typing import Optional

from think_ai.integrations.claude_api import ClaudeAPI

async def test_claude_api() -> Optional[bool]:
    """Test Claude API integration."""
    try:
        # Check if API key is available
        api_key = os.getenv("CLAUDE_API_KEY")
        if not api_key:
            return False

        # Initialize Claude API
        claude = ClaudeAPI()

        # Get cost summary
        claude.get_cost_summary()

        await claude.close()
        return True

    except Exception:
        return False

async def main() -> None:
    """Main test function."""
    # Test Claude API
    claude_ok = await test_claude_api()

    if claude_ok:
        pass
    else:
        pass

if __name__ == "__main__":
    asyncio.run(main())
