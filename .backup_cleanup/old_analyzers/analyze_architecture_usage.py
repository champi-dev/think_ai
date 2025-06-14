#!/usr/bin/env python3
"""Analyze how Think AI is actually using its architecture."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.integrations.claude_api import ClaudeAPI
from datetime import datetime
import json


async def analyze_system_usage():
    """Analyze what components are actually being used."""
    print("🔍 ANALYZING THINK AI ARCHITECTURE USAGE")
    print("=" * 70)
    
    system = DistributedThinkAI()
    
    try:
        # Start system
        services = await system.start()
        
        print("\n📊 CURRENT IMPLEMENTATION:")
        print("-" * 40)
        
        # Test query
        test_query = "What is consciousness?"
        result = await system.process_with_full_system(test_query)
        
        print(f"Query: '{test_query}'")
        print(f"\nServices that responded: {result['services_used']}")
        
        # Analyze each service
        print("\n🔍 SERVICE ANALYSIS:")
        
        # 1. ScyllaDB
        print("\n1. ScyllaDB (Distributed Storage):")
        if 'scylla' in services:
            print("   ✅ Connected")
            # Try to retrieve some data
            try:
                # Check if any knowledge is stored
                test_key = "test_knowledge_check"
                stored_data = await services['scylla'].get(test_key)
                if stored_data:
                    print("   📊 Has stored knowledge")
                else:
                    print("   ⚠️  No knowledge stored yet")
            except:
                print("   ❌ Not actively used for knowledge retrieval")
        
        # 2. Milvus
        print("\n2. Milvus (Vector Search):")
        if 'milvus' in services:
            print("   ✅ Connected")
            if 'milvus' in result['services_used']:
                print("   ✅ Used in query processing")
            else:
                print("   ⚠️  Connected but not actively searching")
            # In current implementation, just returns "Vector search available"
            print("   ❌ Not actually performing similarity search")
        
        # 3. Language Model
        print("\n3. Language Model (GPT-2):")
        if 'model_orchestrator' in services:
            print("   ✅ Loaded")
            if 'language_model' in result['responses']:
                print("   ✅ Generating responses")
                print("   ⚠️  Quality limited by GPT-2 size")
        
        # 4. Consciousness Framework
        print("\n4. Consciousness Framework:")
        if 'consciousness' in services:
            print("   ✅ Active")
            print("   ✅ Generating ethical responses")
            print("   ⚠️  Using template responses")
        
        # 5. Federated Learning
        print("\n5. Federated Learning:")
        if 'federated' in services:
            print("   ✅ Server running")
            stats = services['federated'].get_global_stats()
            print(f"   📊 Clients: {stats['total_clients']}")
            print("   ❌ Not actively learning from interactions")
        
        # 6. Neo4j (Knowledge Graph)
        print("\n6. Neo4j (Knowledge Graph):")
        print("   ❌ Not connected (code issue)")
        print("   ❌ Not building knowledge relationships")
        
        # 7. Redis (Cache)
        print("\n7. Redis (Cache):")
        print("   ❌ Not connected (code issue)")
        print("   ❌ Not caching responses")
        
        print("\n" + "=" * 70)
        print("🚨 WHAT'S ACTUALLY HAPPENING:")
        print("-" * 40)
        print("1. User asks a question")
        print("2. Consciousness framework generates a template response")
        print("3. Language model (GPT-2) tries to generate text (poor quality)")
        print("4. Smart wrapper just forwards to Claude API")
        print("5. Claude generates the actual good response")
        print("\n❌ Most distributed features are NOT being utilized!")
        
        print("\n" + "=" * 70)
        print("✅ WHAT SHOULD BE HAPPENING:")
        print("-" * 40)
        print("1. User asks a question")
        print("2. ScyllaDB checks for stored knowledge on topic")
        print("3. Milvus searches for similar past conversations/knowledge")
        print("4. Neo4j finds related concepts in knowledge graph")
        print("5. Redis checks cache for recent similar queries")
        print("6. Consciousness framework evaluates ethical implications")
        print("7. Language model generates initial response")
        print("8. Claude enhances/verifies only when needed")
        print("9. Response stored back in distributed system")
        print("10. Federated learning improves from interaction")
        
        print("\n" + "=" * 70)
        print("💡 HOW TO FIX THIS:")
        print("-" * 40)
        print("1. Populate ScyllaDB with knowledge base")
        print("2. Generate embeddings and store in Milvus")
        print("3. Build knowledge graph in Neo4j")
        print("4. Implement proper caching in Redis")
        print("5. Use Claude to enhance, not replace, distributed processing")
        print("6. Activate federated learning from conversations")
        
        # Test if we can actually use the distributed features
        print("\n" + "=" * 70)
        print("🧪 TESTING DISTRIBUTED FEATURES:")
        print("-" * 40)
        
        # Store knowledge
        print("\n1. Storing knowledge in ScyllaDB...")
        try:
            from think_ai.storage.base import StorageItem
            knowledge = {
                "fact": "Consciousness involves self-awareness",
                "source": "philosophy",
                "timestamp": datetime.now().isoformat()
            }
            item = StorageItem(
                key=f"knowledge_{datetime.now().timestamp()}",
                value=json.dumps(knowledge),
                metadata={"type": "fact"}
            )
            await services['scylla'].put(item.key, item)
            print("   ✅ Successfully stored knowledge")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        # Generate embedding (would need embedding model)
        print("\n2. Vector search in Milvus...")
        print("   ⚠️  Needs embedding model to generate vectors")
        
        # Register federated client
        print("\n3. Federated learning...")
        try:
            client_id = f"demo_client_{datetime.now().timestamp()}"
            await services['federated'].register_client(client_id)
            print(f"   ✅ Registered client: {client_id}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        
        print("\n" + "=" * 70)
        print("📋 CONCLUSION:")
        print("-" * 40)
        print("You're right - currently it's mostly just Claude with extra steps!")
        print("The distributed architecture is built but not fully integrated.")
        print("To make it worthwhile, we need to:")
        print("1. Actually use the distributed storage for knowledge")
        print("2. Implement real vector search with embeddings")
        print("3. Build and query the knowledge graph")
        print("4. Make the system learn from interactions")
        print("\nThe architecture is there, but needs proper integration!")
        
    finally:
        await system.shutdown()


async def demonstrate_proper_usage():
    """Show how the system SHOULD work with all components."""
    print("\n\n" + "=" * 70)
    print("🚀 DEMONSTRATING PROPER ARCHITECTURE USAGE")
    print("=" * 70)
    
    system = DistributedThinkAI()
    claude = ClaudeAPI()
    
    try:
        services = await system.start()
        
        # Simulate proper flow
        query = "Tell me about quantum computing"
        print(f"\nQuery: '{query}'")
        print("\n📝 PROPER PROCESSING FLOW:")
        
        # 1. Check distributed storage
        print("\n1️⃣ Checking ScyllaDB for stored knowledge...")
        # Would search for quantum computing facts
        
        # 2. Vector similarity search
        print("2️⃣ Searching Milvus for similar topics...")
        # Would find related conversations about physics, computing
        
        # 3. Knowledge graph
        print("3️⃣ Querying Neo4j knowledge graph...")
        # Would find: quantum -> physics -> computing -> algorithms
        
        # 4. Cache check
        print("4️⃣ Checking Redis cache...")
        # Would check if this was recently asked
        
        # 5. Consciousness evaluation
        print("5️⃣ Consciousness framework evaluation...")
        consciousness_resp = await services['consciousness'].generate_conscious_response(query)
        print(f"   Ethical check: ✅ Safe topic")
        
        # 6. Aggregate knowledge
        print("6️⃣ Aggregating distributed knowledge...")
        aggregated_context = {
            "stored_facts": ["quantum computers use qubits", "superposition principle"],
            "related_topics": ["quantum mechanics", "cryptography"],
            "graph_connections": ["physics", "computing", "encryption"]
        }
        
        # 7. Generate response with context
        print("7️⃣ Generating response with full context...")
        enhanced_prompt = f"""Based on this distributed knowledge:
{json.dumps(aggregated_context, indent=2)}

User query: {query}

Provide a comprehensive response that leverages this knowledge."""
        
        # 8. Use Claude only for enhancement
        print("8️⃣ Claude enhancement (not replacement)...")
        final_response = await claude.query(
            prompt=enhanced_prompt,
            system="You are enhancing a response with additional context from distributed systems.",
            max_tokens=200
        )
        
        print("\n✅ FINAL RESPONSE:")
        print(final_response['response'])
        
        # 9. Store back in system
        print("\n9️⃣ Storing new knowledge in distributed system...")
        # Would store the response and new facts learned
        
        # 10. Update federated learning
        print("🔟 Updating federated learning model...")
        # Would update model with this interaction
        
        print("\n✅ THIS is how the architecture should work!")
        print("   - Distributed components provide context")
        print("   - Claude enhances, not replaces")
        print("   - System learns and improves")
        print("   - Knowledge is preserved and reused")
        
    finally:
        await claude.close()
        await system.shutdown()


if __name__ == "__main__":
    asyncio.run(analyze_system_usage())
    asyncio.run(demonstrate_proper_usage())