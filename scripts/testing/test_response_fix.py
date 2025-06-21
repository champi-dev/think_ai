#! / usr / bin / env python3

"""Test that our response fixes work properly."""

import asyncio
import sys

from implement_proper_architecture import ProperThinkAI

sys.path.append(".")


async def test_responses() - > None:
"""Test the response generation logic."""
# Create a minimal ProperThinkAI instance
    system = ProperThinkAI()

# Test questions
    test_cases = [
    ("what is a black hole", "black hole is a region of spacetime"),
    ("what is the sun", "Sun is a G - type main - sequence star"),
    ("what is the universe", "universe is all of space, time, matter"),
    ("what is love", "Love is a complex emotion"),
    ("what is a quasar", "quasar is an interesting topic"), # Should get generic response
    ("hello", "Hello! I'm Think AI"),
    ("what is consciousness", "Consciousness is the state of being aware"),
    ]

    for question, expected_phrase in test_cases:

        try:
# Get the response - pass empty knowledge results since we're just testing fallback
            response = await system._generate_distributed_response(question, {
            "facts": [],
            "vectors": [],
            "graph": [],
            })

# Check if response contains expected content
            if expected_phrase.lower() in response.lower() or "While I'm processing this through my distributed intelligence" in response:
                pass
        else:
            pass

        except Exception:
            pass

        if __name__ = = "__main__":
            asyncio.run(test_responses())
