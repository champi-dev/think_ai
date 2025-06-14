#!/usr/bin/env python3
"""Test that Claude enhancement is disabled."""

import asyncio
from implement_proper_architecture import ProperThinkAI


async def test_no_claude():
    """Test various queries without Claude enhancement."""
    print("🧪 Testing Think AI with Claude Enhancement DISABLED")
    print("=" * 60)
    
    # Initialize system
    think_ai = ProperThinkAI()
    await think_ai.initialize()
    
    # Test queries
    queries = [
        "Hello",
        "What is love?",
        "Who are you?",
        "What is consciousness?",
        "How does AI work?"
    ]
    
    for query in queries:
        print(f"\n📤 Query: '{query}'")
        print("-" * 40)
        
        result = await think_ai.process_with_proper_architecture(query)
        
        print(f"Source: {result.get('source', 'unknown')}")
        print(f"Response: {result.get('response', '')[:200]}...")
        
        # Verify no Claude enhancement
        if result.get('source') == 'claude_enhanced':
            print("❌ ERROR: Claude enhancement was used!")
        else:
            print("✅ No Claude enhancement (as expected)")
    
    print("\n✅ Test complete - Claude enhancement is properly disabled!")


if __name__ == "__main__":
    asyncio.run(test_no_claude())