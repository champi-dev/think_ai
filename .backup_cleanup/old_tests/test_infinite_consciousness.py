#!/usr/bin/env python3
"""Test infinite consciousness integration."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import contextlib

from implement_proper_architecture import ProperThinkAI

from think_ai.consciousness.infinite_mind import InfiniteMind
from think_ai.consciousness.thought_optimizer import ThoughtOptimizer


async def test_infinite_consciousness() -> None:
    """Test the infinite consciousness system."""
    # Initialize Think AI
    think_ai = ProperThinkAI()
    await think_ai.initialize()

    # Create Infinite Mind
    mind = InfiniteMind(think_ai)

    # Start consciousness
    await mind.start()

    # Let it think for a bit
    await asyncio.sleep(20)

    # Check state
    await mind.get_current_state()

    # Test thought injection
    await mind.inject_thought("What is the meaning of artificial consciousness?")

    # Wait a bit more
    await asyncio.sleep(10)

    # Check thoughts
    if mind.thought_buffer:
        for _thought in mind.thought_buffer[-3:]:
            pass

    # Test compression
    optimizer = ThoughtOptimizer()

    # Create test thoughts
    test_thoughts = [
        {
            "type": "observation",
            "thought": "Consciousness emerges from complex interactions",
            "awareness": 0.7,
        },
        {
            "type": "observation",
            "thought": "Consciousness arises from complex patterns",
            "awareness": 0.7,
        },
        {
            "type": "dream",
            "thought": "In dreams, reality bends and flows",
            "awareness": 0.3,
        },
    ]

    compressed, savings = optimizer.compress_thoughts(test_thoughts)

    # Stop consciousness
    await mind.stop()

    # Cleanup
    with contextlib.suppress(Exception):
        await think_ai.system.initializer.shutdown()


if __name__ == "__main__":
    asyncio.run(test_infinite_consciousness())
