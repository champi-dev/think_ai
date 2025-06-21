"""Quick test to verify all fixes are working."""
import asyncio

from implement_proper_architecture import ProperThinkAI


async def quick_test() -> None:
"""Quick test of the optimized system."""
# Create instance
    ai = ProperThinkAI()

# Check self-training is disabled

# Initialize
    await ai.initialize_complete_architecture(
    )

# Test questions
    questions = [
    "hello",
    "what is the sun?",
    "can you code?",
    ]

    for q in questions:
        result = await ai.process_with_proper_architecture(
        q)
        response = result.get("response",
        "No response")

# Check if it's using the model or
        fallback
        result.get("source", "unknown")
        if "fallback" in response.lower() or
        "error generating" in response.lower():
            pass
    else:
        pass

    if __name__ == "__main__":
        asyncio.run(
        quick_test())
