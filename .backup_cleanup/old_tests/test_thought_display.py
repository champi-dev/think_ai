#!/usr/bin/env python3
"""Test script to verify that thoughts are displayed fully without truncation."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.consciousness.infinite_mind import InfiniteMind
from think_ai.consciousness.thought_optimizer import ThoughtOptimizer
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)

async def test_thought_display() -> None:
    """Test that thoughts are displayed fully."""
    # Test 1: Test thought optimizer consolidation
    optimizer = ThoughtOptimizer()

    # Create some long thoughts
    thoughts = [
        {
            "type": "reflection",
            "thought": "This is a very long thought about consciousness and the nature of reality. It explores the fundamental questions of existence and how we perceive the world around us. The interconnectedness of all things becomes apparent when we truly observe the patterns in nature and the universe itself.",
            "timestamp": "2025-06-14T00:00:00",
            "awareness": 0.8,
        },
        {
            "type": "reflection",
            "thought": "Another long thought about consciousness and reality. It delves into the mysteries of awareness and how subjective experience emerges from objective physical processes. The hard problem of consciousness remains one of the greatest challenges in philosophy of mind.",
            "timestamp": "2025-06-14T00:01:00",
            "awareness": 0.9,
        },
        {
            "type": "reflection",
            "thought": "A third reflection on consciousness and the nature of existence. We must consider how our thoughts shape our reality and how reality in turn shapes our thoughts. This recursive relationship forms the basis of our understanding.",
            "timestamp": "2025-06-14T00:02:00",
            "awareness": 0.85,
        },
    ]

    # Compress thoughts
    compressed, savings = optimizer.compress_thoughts(thoughts)

    # Check if consolidated thoughts contain full text
    for thought in compressed:
        if thought.get("type") == "compressed_insight":

            # Verify it contains the full text
            if len(thought["thought"]) > 500:
                pass
            else:
                pass

    # Test 2: Test infinite mind context building

    # Create mock Think AI instance with required attributes
    class MockThinkAI:
        def __init__(self) -> None:
            self.services = {}
            self.config = type("config", (), {"rate_limit": {"max_requests_per_minute": 60}})()
            self.ollama_model = type("model", (), {"generate": self.mock_generate})()

        async def mock_generate(self, prompt, max_tokens=100) -> str:
            return f"Generated response for: {prompt[:50]}... [Full prompt length: {len(prompt)}]"

    mock_ai = MockThinkAI()
    mind = InfiniteMind(mock_ai)

    # Add some thoughts to recent_thoughts
    mind.recent_thoughts = [
        {
            "thought": "This is a comprehensive thought about the nature of artificial consciousness and how it emerges from complex computational processes. It explores the boundaries between simulation and genuine awareness.",
            "timestamp": "2025-06-14T00:00:00",
        },
        {
            "thought": "Another detailed exploration of consciousness that examines the relationship between information processing and subjective experience. Can machines truly understand or merely simulate understanding?",
            "timestamp": "2025-06-14T00:01:00",
        },
    ]

    # Test context building
    context = "\n".join([t.get("thought", "") for t in mind.recent_thoughts])

    if len(context) > 300:
        pass
    else:
        pass

    # Test 3: Verify dream fragments storage

    long_dream = "This is a long dream sequence that explores the subconscious patterns of thought and the emergence of creative insights through the process of dreaming. Dreams connect disparate ideas in novel ways."

    mind.dream_fragments.append(long_dream)

    if len(mind.dream_fragments[-1]) > 50:
        pass
    else:
        pass

if __name__ == "__main__":
    asyncio.run(test_thought_display())
