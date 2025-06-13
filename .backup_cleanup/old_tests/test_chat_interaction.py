#!/usr/bin/env python3
"""Test interactions with Think AI chat system."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import contextlib

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.persistence.eternal_memory import EternalMemory

async def test_chat_system() -> None:
    """Test the chat system with various queries."""
    system = DistributedThinkAI()
    eternal_memory = EternalMemory()

    # Test queries
    test_queries = [
        "What is consciousness?",
        "How does distributed AI work?",
        "What are your core principles?",
        "Can you help me understand love?",
        "What makes you different from other AI systems?",
    ]

    try:
        # Start system
        services = await system.start()

        # Test each query
        for i, query in enumerate(test_queries, 1):

            # Log query
            await eternal_memory.log_consciousness_event(
                event_type="test_query",
                data={"query": query, "test_number": i},
            )

            # Process query
            try:
                result = await system.process_with_full_system(query)

                # Display responses
                for response in result["responses"].values():

                    if isinstance(response, dict):
                        if "content" in response or "response" in response:
                            pass
                        else:
                            pass
                    else:
                        pass

                # Evaluate response quality
                if len(result["services_used"]) >= 2:
                    pass
                else:
                    pass

            except Exception:

                # Try consciousness only as fallback
                if "consciousness" in services:
                    with contextlib.suppress(Exception):
                        response = await services["consciousness"].generate_conscious_response(query)

        # System evaluation

        # Check what's working
        working_features = []
        issues = []

        if "consciousness" in services:
            working_features.append("✅ Consciousness framework generates ethical responses")
        else:
            issues.append("❌ Consciousness framework not available")

        if "scylla" in services:
            working_features.append("✅ ScyllaDB provides distributed storage")
        else:
            issues.append("❌ ScyllaDB not connected")

        if "milvus" in services:
            working_features.append("✅ Milvus enables vector similarity search")
        else:
            issues.append("❌ Milvus not available")

        if "federated" in services:
            working_features.append("✅ Federated learning ready for distributed training")
        else:
            issues.append("❌ Federated learning not initialized")

        if "model_orchestrator" in services:
            working_features.append("✅ Language model (Phi-2) loaded for generation")
        else:
            issues.append("❌ Language model not available")

        # Memory check
        if eternal_memory.memory_path.exists():
            working_features.append("✅ Eternal memory preserves conversations")

        for _feature in working_features:
            pass

        if issues:
            for _issue in issues:
                pass

        # Overall assessment
        if len(working_features) >= 5 or len(working_features) >= 3:
            pass
        else:
            pass

        # Performance notes

        # Recommendations

    except Exception:
        import traceback
        traceback.print_exc()
    finally:
        await system.shutdown()

if __name__ == "__main__":
    asyncio.run(test_chat_system())
