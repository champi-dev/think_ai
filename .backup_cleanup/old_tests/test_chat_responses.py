#!/usr/bin/env python3
"""Test script to verify Think AI responses."""

import asyncio

from chat_with_exponential_ai import ExponentialThinkAIChat


async def test_responses() -> None:
    """Test various queries to see responses."""
    chat = ExponentialThinkAIChat()

    try:
        await chat.initialize()

        test_queries = [
            "what is passion?",
            "are u ok?",
            "explain consciousness",
            "hello",
        ]

        for query in test_queries:
            await chat.process_with_exponential_intelligence(query)

    finally:
        if hasattr(chat.think_ai, "system"):
            await chat.think_ai.system.shutdown()
        if chat.claude_api:
            await chat.claude_api.close()


if __name__ == "__main__":
    asyncio.run(test_responses())
