#!/usr/bin/env python3
"""Quick test of Think AI chat responses."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from chat_with_exponential_ai import ExponentialThinkAIChat


async def test_single_query() -> None:
    """Test a single query."""
    chat = ExponentialThinkAIChat()

    try:
        await chat.initialize()

        query = "what is passion?"

        await chat.process_with_exponential_intelligence(query)

    finally:
        if hasattr(chat.think_ai, "system"):
            await chat.think_ai.system.shutdown()
        if chat.claude_api:
            await chat.claude_api.close()


if __name__ == "__main__":
    asyncio.run(test_single_query())
