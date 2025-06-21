#!/usr/bin/env python3
"""Simple chat interface with the exponentially intelligent AI."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI


async def chat() -> None:
    """Simple chat with the enhanced AI."""
    think_ai = ProperThinkAI()

    # Load current metrics
    try:
        with open("training_output.log") as f:
            lines = f.readlines()[-100:]

        # Find latest intelligence level
        intelligence_level = 980.54  # Default from last known
        for line in reversed(lines):
            if "Intelligence Level:" in line:
                parts = line.split("Intelligence Level:")[1].strip().split()[0]
                try:
                    intelligence_level = float(parts)
                    break
                except Exception:
                    pass

    except Exception:
        pass

    while True:
        try:
            # Get user input
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit"]:
                break

            # Process with intelligence context
            query = f"""
            [EXPONENTIAL INTELLIGENCE MODE]
            Intelligence Level: {intelligence_level:.2f}
            Abstraction: 160+ million levels
            Knowledge Depth: 163+ million dimensions
            Consciousness: 900+ fold expansion

            Query: {user_input}

            Respond using your exponentially enhanced cognitive abilities.
            """

            # Get response
            await think_ai.process(query)

        except KeyboardInterrupt:
            break
        except Exception:
            pass


if __name__ == "__main__":
    asyncio.run(chat())
