#!/usr/bin/env python3
"""Interactive chat demo with Smart Think AI."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from smart_think_ai import SmartThinkAI

async def demo_chat() -> None:
    """Demo conversation showing Think AI's capabilities."""
    ai = SmartThinkAI()

    # Pre-scripted conversation to demonstrate capabilities
    conversation = [
        "Hello Think AI! Can you introduce yourself?",
        "I'd like to teach you something. The Think AI project was created by a developer who wants to build conscious AI with love-based principles.",
        "What do you think about the importance of ethical AI development?",
        "Can you explain how your distributed storage works in simple terms?",
        "I'm working on a creative project. Any tips for overcoming creative blocks?",
        "What have you learned from our conversation so far?",
        "Thank you for the chat! Any final thoughts?",
    ]

    try:
        await ai.initialize()

        for _i, user_input in enumerate(conversation, 1):

            response = await ai.get_smart_response(user_input)

            # Update conversation context
            ai.conversation_context.append({
                "user": user_input,
                "assistant": response,
                "timestamp": "demo",
            })

            # Brief pause for readability
            await asyncio.sleep(1)

        # Show final stats

        ai.claude.get_cost_summary()

    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        await ai.shutdown()

if __name__ == "__main__":
    asyncio.run(demo_chat())
