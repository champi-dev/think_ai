#!/usr/bin/env python3
"""Demo of the full distributed Think AI system."""

import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from think_ai.engine.claude_internal_tool import ClaudeInternalTool
from think_ai.engine.full_system import DistributedThinkAI

async def main() -> None:
    """Demo the full system capabilities."""
    system = DistributedThinkAI()
    claude_tool = None

    try:
        # Start system
        services = await system.start()

        for _service in services:
            pass

        # Initialize Claude as internal tool
        if "consciousness" in services:
            claude_tool = ClaudeInternalTool(services["consciousness"])

        # Demo 1: Consciousness Framework
        query = "What is the meaning of consciousness?"

        await services["consciousness"].generate_conscious_response(query)

        # Demo 2: Distributed Storage

        # Store knowledge
        await services["scylla"].put(
            key="consciousness_definition",
            value="Consciousness is the state of being aware of and able to think about one's existence, thoughts, and surroundings.",
            metadata={"category": "philosophy", "love_score": 0.9},
        )

        # Retrieve knowledge
        result = await services["scylla"].get("consciousness_definition")
        if result:
            pass

        # Demo 3: Vector Search (Milvus)

        # Demo 4: Federated Learning
        services["federated"].get_global_stats()

        # Demo 5: Claude Enhancement
        if claude_tool:

            knowledge = await claude_tool.consult_for_knowledge(
                topic="distributed AI systems",
                context={"focus": "benefits and architecture"},
            )

            if knowledge["success"]:
                pass

        # System Summary

    except Exception:
        import traceback
        traceback.print_exc()

    finally:
        await system.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
