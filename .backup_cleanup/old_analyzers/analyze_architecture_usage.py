#!/usr/bin/env python3
"""Analyze how Think AI is actually using its architecture."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import json
from datetime import datetime

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.integrations.claude_api import ClaudeAPI

async def analyze_system_usage() -> None:
    """Analyze what components are actually being used."""
    system = DistributedThinkAI()

    try:
        # Start system
        services = await system.start()

        # Test query
        test_query = "What is consciousness?"
        result = await system.process_with_full_system(test_query)

        # Analyze each service

        # 1. ScyllaDB
        if "scylla" in services:
            # Try to retrieve some data
            try:
                # Check if any knowledge is stored
                test_key = "test_knowledge_check"
                stored_data = await services["scylla"].get(test_key)
                if stored_data:
                    pass
                else:
                    pass
            except Exception:
                pass

        # 2. Milvus
        if "milvus" in services:
            if "milvus" in result["services_used"]:
                pass
            else:
                pass
            # In current implementation, just returns "Vector search available"

        # 3. Language Model
        if "model_orchestrator" in services and "language_model" in result["responses"]:
            pass

        # 4. Consciousness Framework
        if "consciousness" in services:
            pass

        # 5. Federated Learning
        if "federated" in services:
            services["federated"].get_global_stats()

        # 6. Neo4j (Knowledge Graph)

        # 7. Redis (Cache)

        # Test if we can actually use the distributed features

        # Store knowledge
        try:
            from think_ai.storage.base import StorageItem
            knowledge = {
                "fact": "Consciousness involves self-awareness",
                "source": "philosophy",
                "timestamp": datetime.now().isoformat(),
            }
            item = StorageItem(
                key=f"knowledge_{datetime.now().timestamp()}",
                value=json.dumps(knowledge),
                metadata={"type": "fact"},
            )
            await services["scylla"].put(item.key, item)
        except Exception:
            pass

        # Generate embedding (would need embedding model)

        # Register federated client
        try:
            client_id = f"demo_client_{datetime.now().timestamp()}"
            await services["federated"].register_client(client_id)
        except Exception:
            pass

    finally:
        await system.shutdown()

async def demonstrate_proper_usage() -> None:
    """Show how the system SHOULD work with all components."""
    system = DistributedThinkAI()
    claude = ClaudeAPI()

    try:
        services = await system.start()

        # Simulate proper flow
        query = "Tell me about quantum computing"

        # 1. Check distributed storage
        # Would search for quantum computing facts

        # 2. Vector similarity search
        # Would find related conversations about physics, computing

        # 3. Knowledge graph
        # Would find: quantum -> physics -> computing -> algorithms

        # 4. Cache check
        # Would check if this was recently asked

        # 5. Consciousness evaluation
        await services["consciousness"].generate_conscious_response(query)

        # 6. Aggregate knowledge
        aggregated_context = {
            "stored_facts": ["quantum computers use qubits", "superposition principle"],
            "related_topics": ["quantum mechanics", "cryptography"],
            "graph_connections": ["physics", "computing", "encryption"],
        }

        # 7. Generate response with context
        enhanced_prompt = f"""Based on this distributed knowledge:
{json.dumps(aggregated_context, indent=2)}

User query: {query}

Provide a comprehensive response that leverages this knowledge."""

        # 8. Use Claude only for enhancement
        await claude.query(
            prompt=enhanced_prompt,
            system="You are enhancing a response with additional context from distributed systems.",
            max_tokens=200,
        )

        # 9. Store back in system
        # Would store the response and new facts learned

        # 10. Update federated learning
        # Would update model with this interaction

    finally:
        await claude.close()
        await system.shutdown()

if __name__ == "__main__":
    asyncio.run(analyze_system_usage())
    asyncio.run(demonstrate_proper_usage())
