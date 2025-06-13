#! / usr / bin / env python3

"""Test the system with fresh state for direct responses."""

import asyncio
import sys
from pathlib import Path

from implement_proper_architecture import ProperArchitectureDemo

sys.path.insert(0, str(Path(__file__).parent))


async def test_fresh_response() - > None:
"""Test system with no caching for direct responses."""
# Create fresh instance
    demo = ProperArchitectureDemo()

# Disable caching for this test
    demo.enable_caching = False

    await demo.initialize_complete_architecture()

# Test direct questions
    test_questions = [
    "What is the sun?",
    "Hello",
    "What is 2 + 2?",
    "What is artificial intelligence?",
    ]

    for question in test_questions:

# Process with architecture
        result = await demo.process_with_proper_architecture(question)

# Extract just the response
        result.get("response", "No response generated")

# Show architecture usage
        arch_usage = result.get("architecture_usage", {})
        if arch_usage:
            for _component, _status in arch_usage.items():
                pass

            if __name__ = = "__main__":
                asyncio.run(test_fresh_response())
