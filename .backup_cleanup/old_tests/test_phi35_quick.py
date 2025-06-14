#!/usr/bin/env python3
"""Quick test of Phi-3.5 Mini integration."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from implement_proper_architecture import ProperThinkAI


async def quick_test():
    """Quick integration test."""
    print("🧪 Quick Test: Phi-3.5 Mini + Think AI")
    print("="*60)
    
    # Initialize
    think_ai = ProperThinkAI()
    await think_ai.initialize()
    
    # Test query
    query = "What is artificial intelligence?"
    print(f"\n📝 Query: '{query}'")
    
    result = await think_ai.process_with_proper_architecture(query)
    
    print(f"\n✅ Response received!")
    print(f"Source: {result['source']}")
    print(f"Response: {result['response'][:200]}...")
    
    # Verify Phi-3.5 was used
    if result['source'] == 'distributed':
        print("\n🎉 SUCCESS: Phi-3.5 Mini generated the response!")
    else:
        print(f"\n⚠️  Response came from: {result['source']}")
    
    # Test cache
    print("\n🔄 Testing cache (same query)...")
    result2 = await think_ai.process_with_proper_architecture(query)
    
    if result2['source'] == 'cache':
        print("✅ Cache working correctly!")
    else:
        print(f"⚠️  Expected cache, got: {result2['source']}")
    
    # Cleanup
    try:
        await think_ai.system.initializer.shutdown()
    except:
        pass
    
    print("\n✨ Test complete!")


if __name__ == "__main__":
    asyncio.run(quick_test())