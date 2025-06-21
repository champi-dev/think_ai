#! / usr / bin / env python3

"""Test the full system with direct responses."""

import asyncio

from implement_proper_architecture import ProperThinkAI


async def test() - > None:
    ai = ProperThinkAI()
    await ai.initialize()

# Test queries
    queries = ["hello", "what is 2 + 2?", "how are you?"]

    for query in queries:
        await ai.process_with_proper_architecture(query)

        await ai.shutdown()

        if __name__ = = "__main__":
            asyncio.run(test())
