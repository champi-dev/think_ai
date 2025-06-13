#! / usr / bin / env python3

"""Test that black hole questions now get proper answers."""

import asyncio
import sys

from implement_proper_architecture import ProperThinkAI

sys.path.append(".")


async def test_black_hole_response() - > None:
"""Test the black hole response."""
# Initialize the system
    system = ProperThinkAI()
    await system.initialize()

# Test questions
    questions = [
    "what is a black hole",
    "what is the sun",
    "what is the universe",
    "what is a quasar",  # This should still get the generic response
    ]

    for question in questions:

# Get the distributed response directly
        response = system._generate_distributed_response(question)

# Check if it's the unhelpful generic response
        if "While I'm processing this through my distributed intelligence" in response:
            pass
    else:
        pass

    if __name__ = = "__main__":
        asyncio.run(test_black_hole_response())
