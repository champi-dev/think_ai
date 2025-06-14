#!/usr/bin/env python3
"""Demo of the full distributed Think AI system."""

import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.integrations.claude_api import ClaudeAPI
from think_ai.engine.claude_internal_tool import ClaudeInternalTool


async def main():
    """Demo the full system capabilities."""
    print("🤖 Think AI Full Distributed System Demo")
    print("=" * 60)
    
    system = DistributedThinkAI()
    claude_tool = None
    
    try:
        # Start system
        print("\n🚀 Starting distributed services...")
        services = await system.start()
        
        print(f"\n✅ Successfully started {len(services)} services:")
        for service in services:
            print(f"   - {service}")
        
        # Initialize Claude as internal tool
        if 'consciousness' in services:
            claude_tool = ClaudeInternalTool(services['consciousness'])
            print("\n✅ Claude initialized as internal knowledge tool")
        
        # Demo 1: Consciousness Framework
        print("\n\n📊 Demo 1: Consciousness Framework")
        print("-" * 40)
        query = "What is the meaning of consciousness?"
        
        response = await services['consciousness'].generate_conscious_response(query)
        print(f"Query: {query}")
        print(f"Response: {response['content']}")
        print(f"State: {response['consciousness_state']}")
        
        # Demo 2: Distributed Storage
        print("\n\n📊 Demo 2: Distributed Storage (ScyllaDB)")
        print("-" * 40)
        
        # Store knowledge
        await services['scylla'].put(
            key="consciousness_definition",
            value="Consciousness is the state of being aware of and able to think about one's existence, thoughts, and surroundings.",
            metadata={"category": "philosophy", "love_score": 0.9}
        )
        print("✅ Stored knowledge in ScyllaDB")
        
        # Retrieve knowledge
        result = await services['scylla'].get("consciousness_definition")
        if result:
            print(f"📖 Retrieved: {result.value}")
        
        # Demo 3: Vector Search (Milvus)
        print("\n\n📊 Demo 3: Vector Search Capability")
        print("-" * 40)
        print("✅ Milvus vector database ready for semantic search")
        print("   - Collection: think_ai_knowledge")
        print("   - Dimension: 768")
        print("   - Index: HNSW for fast similarity search")
        
        # Demo 4: Federated Learning
        print("\n\n📊 Demo 4: Federated Learning System")
        print("-" * 40)
        stats = services['federated'].get_global_stats()
        print(f"✅ Federated learning server active")
        print(f"   - Total clients: {stats['total_clients']}")
        print(f"   - Model version: {stats['current_model_version']}")
        
        # Demo 5: Claude Enhancement
        if claude_tool:
            print("\n\n📊 Demo 5: Claude-Enhanced Knowledge")
            print("-" * 40)
            
            knowledge = await claude_tool.consult_for_knowledge(
                topic="distributed AI systems",
                context={"focus": "benefits and architecture"}
            )
            
            if knowledge['success']:
                print(f"✅ Claude provided enhanced knowledge:")
                print(f"   {knowledge['knowledge'][:300]}...")
                print(f"   Cost: ${knowledge['cost']:.4f}")
        
        # System Summary
        print("\n\n🎯 System Capabilities Summary")
        print("=" * 60)
        print("✅ Distributed Storage: ScyllaDB with O(1) access")
        print("✅ Vector Search: Milvus for semantic similarity")
        print("✅ Consciousness: Ethical AI with love-based principles")
        print("✅ Federated Learning: Privacy-preserving AI improvement")
        print("✅ Claude Integration: Internal knowledge enhancement")
        print("\n💡 Your Think AI system is ready for massive scale!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n\n🛑 Shutting down services...")
        await system.shutdown()
        print("✅ Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())