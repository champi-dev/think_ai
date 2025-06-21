"""Test the fixed Think AI response system."""

import asyncio
from think_ai.consciousness.awareness import ConsciousnessFramework


async def test_direct_responses():
    """Test that Think AI now gives direct, helpful responses."""
    
    # Initialize consciousness framework
    cf = ConsciousnessFramework()
    
    # Test queries that were problematic before
    test_queries = [
        "hello",
        "what do u know?",
        "can u code?",
        "who are you",
        "what can you do"
    ]
    
    print("🧠 Testing Think AI Fixed Responses\n")
    print("=" * 50)
    
    for query in test_queries:
        response = await cf.respond_to_query(query)
        content = response['content']
        
        print(f"\nQuery: '{query}'")
        print(f"Response: {content}")
        
        # Verify no generic responses
        assert "exponential analysis" not in content.lower()
        assert "complexity level" not in content.lower()
        assert "Self-training evolution suggests" not in content
        
        # Verify direct, helpful responses
        if "hello" in query:
            assert any(word in content.lower() for word in ["hello", "hi", "help", "assist"])
        elif "know" in query:
            assert any(word in content.lower() for word in ["programming", "code", "ai", "knowledge"])
        elif "code" in query:
            assert any(word in content.lower() for word in ["yes", "python", "javascript", "write"])
    
    print("\n" + "=" * 50)
    print("✅ All tests passed! Think AI now provides direct, helpful responses!")


if __name__ == "__main__":
    asyncio.run(test_direct_responses())