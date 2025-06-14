#!/usr/bin/env python3
"""Test the full distributed Think AI system."""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from think_ai.engine.full_system import DistributedThinkAI
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


async def main():
    """Run full system test."""
    print("\n🤖 Think AI Full System Test")
    print("=" * 50)
    
    system = DistributedThinkAI()
    
    try:
        # Start the system
        print("\n🚀 Starting distributed services...")
        services = await system.start()
        
        print(f"\n✅ Successfully started {len(services)} services")
        
        # Test queries
        test_queries = [
            "What is consciousness?",
            "Explain the concept of love in AI systems",
            "How does distributed storage work?",
            "What are the ethical principles of Think AI?"
        ]
        
        print("\n🧪 Running test queries...")
        for query in test_queries:
            print(f"\n📝 Query: {query}")
            result = await system.process_with_full_system(query)
            
            print(f"   Services used: {', '.join(result['services_used'])}")
            
            # Show first response
            if result['responses']:
                first_service = list(result['responses'].keys())[0]
                response = result['responses'][first_service]
                if isinstance(response, str):
                    print(f"   Response ({first_service}): {response[:150]}...")
                else:
                    print(f"   Response ({first_service}): {str(response)[:150]}...")
        
        # Health check
        print("\n🏥 Final health check:")
        health = await system.initializer.health_check()
        for service, status in health.items():
            emoji = "✅" if status['status'] == 'healthy' else "❌"
            print(f"   {emoji} {service}: {status['message']}")
        
        print("\n✅ Full system test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🛑 Shutting down...")
        await system.shutdown()
        print("✅ Shutdown complete")


if __name__ == "__main__":
    asyncio.run(main())