#!/usr/bin/env python3
"""Test the distributed Think AI system with a query."""

import asyncio
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

from think_ai.engine.full_system import DistributedThinkAI


async def main():
    """Test distributed query processing."""
    print("🤖 Testing Distributed Think AI System")
    print("=" * 50)
    
    system = DistributedThinkAI()
    
    try:
        # Start system
        print("\n🚀 Starting services...")
        await system.start()
        
        # Test queries
        queries = [
            "What is consciousness?",
            "Explain distributed AI systems",
            "How does love guide artificial intelligence?"
        ]
        
        print("\n🧪 Running test queries...")
        for query in queries:
            print(f"\n📝 Query: {query}")
            result = await system.process_with_full_system(query)
            
            print(f"   Services used: {', '.join(result['services_used'])}")
            
            # Show responses
            for service, response in result['responses'].items():
                print(f"\n   💭 {service}:")
                if isinstance(response, str):
                    print(f"      {response[:200]}...")
                elif isinstance(response, dict) and 'response' in response:
                    print(f"      {response['response'][:200]}...")
                else:
                    print(f"      {str(response)[:200]}...")
        
        print("\n✅ Test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🛑 Shutting down...")
        await system.shutdown()


if __name__ == "__main__":
    asyncio.run(main())