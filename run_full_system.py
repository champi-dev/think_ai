#!/usr/bin/env python3
"""Run Think AI Full System with all distributed components."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.engine.full_system import DistributedThinkAI
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

async def main():
    """Run the full distributed system."""
    print("\n🧠 THINK AI - FULL DISTRIBUTED SYSTEM")
    print("=" * 50)
    print("Components: ScyllaDB • Redis • Milvus • Neo4j • Consciousness")
    print("=" * 50)
    
    # Initialize the system
    system = DistributedThinkAI()
    
    try:
        # Start all services
        print("\n🚀 Starting distributed services...")
        await system.start()
        
        # Run some test queries
        print("\n📝 Running test queries...\n")
        
        test_queries = [
            "What is consciousness?",
            "How does distributed AI work?",
            "Explain neural pathways",
        ]
        
        for query in test_queries:
            print(f"\n❓ Query: {query}")
            print("-" * 40)
            
            result = await system.process_with_full_system(query)
            
            print(f"✅ Services used: {', '.join(result['services_used'])}")
            print(f"📊 Response quality: {result['distributed_response_quality']}")
            
            # Show responses from each service
            for service, response in result['responses'].items():
                print(f"\n💬 {service}:")
                if isinstance(response, str):
                    print(f"   {response[:150]}..." if len(response) > 150 else f"   {response}")
                elif isinstance(response, dict):
                    if 'content' in response:
                        content = response['content']
                        print(f"   {content[:150]}..." if len(content) > 150 else f"   {content}")
                    else:
                        print(f"   {response}")
            
            await asyncio.sleep(1)  # Small delay between queries
        
        print("\n" + "=" * 50)
        print("✅ Full system test completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Shutdown
        print("\n🔄 Shutting down services...")
        await system.shutdown()
        print("✅ Shutdown complete")

if __name__ == "__main__":
    asyncio.run(main())