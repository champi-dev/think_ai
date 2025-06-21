#! / usr / bin / env python3

"""Test that self - trainer provides real answers."""

import asyncio

from think_ai.intelligence.self_trainer import SelfTrainingIntelligence


async def test_self_trainer() - > None:
"""Test self - trainer responses."""
# Create self - trainer instance
    trainer = SelfTrainingIntelligence()

# Test questions
    test_queries = [
    "hello",
    "what is a black hole",
    "what is the universe",
    "what is the sun",
    "what is artificial intelligence",
    "what is quantum physics",
    "who created it?",  # Should understand context
    "what is consciousness",
    "what is python",  # Not in knowledge base
    "explain gravity",  # Different phrasing
    ]

    for query in test_queries:
        response = await trainer.generate_response(query)

# Check if response is actually answering the question
        if "what is" in query.lower():
# Should not contain generic phrases
            assert "That's an interesting topic" not in response
            assert "neural pathways" not in response or "black hole" in query.lower()
            assert "How can I help you understand" not in response

# For known topics, should contain actual information
            if "black hole" in query.lower():
                assert "gravity" in response.lower() or "spacetime" in response.lower()
            elif "universe" in query.lower():
                assert "space" in response.lower() or "big bang" in response.lower()
            elif "sun" in query.lower():
                assert "star" in response.lower() or "solar" in response.lower()

                if __name__ = = "__main__":
                    asyncio.run(test_self_trainer())
