"""Example of cost-conscious Think AI usage."""

import asyncio
from datetime import datetime
from think_ai.core.think_ai_eternal import ThinkAIEternal, create_free_think_ai


async def demonstrate_free_usage():
    """Demonstrate completely free Think AI usage."""
    print("=== Free Think AI Demo ===")
    
    # Create free instance
    ai = await create_free_think_ai()
    
    try:
        # 1. Basic query using local model
        print("\n1. Local Model Query (Cost: $0)")
        response = await ai.query_with_cost_awareness(
            "What are the benefits of meditation?",
            prefer_free=True
        )
        
        print(f"Response: {response['response'][:100]}...")
        print(f"Source: {response['source']}")
        print(f"Cost: ${response['cost']}")
        
        # 2. Complex query that might need Claude
        print("\n2. Complex Query Analysis")
        complex_query = "Design a distributed microservices architecture for a social media platform"
        
        response = await ai.query_with_cost_awareness(complex_query)
        
        if response.get("status") == "claude_ready":
            print("Optimized prompt for Claude:")
            print(f"Token reduction: {response['optimization_report']['reduction_percentage']:.1f}%")
            print(f"Estimated cost: ${response['estimated_cost']:.3f}")
            print("\nCopy this to Claude web interface:")
            print("-" * 50)
            print(response["optimized_prompt"])
            print("-" * 50)
        else:
            print(f"Free alternative used: {response['source']}")
        
        # 3. Import a hypothetical Claude response
        print("\n3. Import Claude Response")
        claude_response = """
        For a social media platform, consider:
        1. User service for authentication
        2. Content service for posts/media
        3. Feed service for timeline generation
        4. Notification service for real-time updates
        Use API gateway, event-driven architecture.
        """
        
        import_result = await ai.import_claude_response(
            complex_query,
            claude_response,
            metadata={"manual_import": True, "estimated_cost": 0.02}
        )
        
        print(f"Import result: {import_result}")
        
        # 4. Get cost summary
        print("\n4. Cost Summary")
        summary = await ai.get_cost_summary()
        
        print(f"Total spent: ${summary['costs']['total_spent']:.2f}")
        print(f"Budget limit: ${summary['costs']['budget_limit']:.2f}")
        print(f"Optimization savings: ${summary['costs']['optimization_savings']:.2f}")
        print(f"Memory status: {summary['memory']['status']}")
        
        # 5. Demonstrate caching
        print("\n5. Cached Response Demo")
        cached_response = await ai.query_with_cost_awareness(
            "What are the benefits of meditation?",  # Same query as #1
            prefer_free=True
        )
        
        if cached_response.get("source") == "cache":
            print("✓ Response served from cache (cost: $0)")
        else:
            print("New response generated")
        
    finally:
        # Always shutdown gracefully to preserve memory
        await ai.shutdown("demo_complete")


async def demonstrate_budget_conscious_usage():
    """Demonstrate usage with a small budget."""
    print("\n=== Budget-Conscious Demo ($5/month) ===")
    
    ai = ThinkAIEternal(budget_profile="minimal")
    await ai.initialize()
    
    try:
        # Track multiple operations
        queries = [
            "How to optimize Python code?",
            "Explain machine learning basics",
            "Best practices for API design"
        ]
        
        total_cost = 0.0
        
        for i, query in enumerate(queries, 1):
            print(f"\n{i}. Processing: {query[:30]}...")
            
            response = await ai.query_with_cost_awareness(query)
            
            if response.get("cost") is not None:
                total_cost += response["cost"]
                print(f"   Response: {response['response'][:50]}...")
                print(f"   Cost: ${response['cost']:.3f}")
            else:
                print(f"   Optimized prompt ready (estimated: ${response.get('estimated_cost', 0):.3f})")
        
        print(f"\nTotal session cost: ${total_cost:.3f}")
        
        # Check if approaching budget
        summary = await ai.get_cost_summary()
        budget_used = summary['costs']['budget_used_percentage']
        
        if budget_used > 50:
            print(f"⚠️  Budget usage: {budget_used:.1f}% - Consider free alternatives")
            
            # Show suggestions
            for suggestion in summary['suggestions']:
                print(f"   💡 {suggestion['suggestion']}")
        
    finally:
        await ai.shutdown("budget_demo_complete")


async def demonstrate_eternal_memory():
    """Demonstrate eternal memory across sessions."""
    print("\n=== Eternal Memory Demo ===")
    
    # Session 1: Store some knowledge
    print("Session 1: Storing knowledge...")
    ai1 = await create_free_think_ai()
    
    await ai1.query_with_cost_awareness("Remember: I love working with Python")
    await ai1.query_with_cost_awareness("My favorite framework is FastAPI")
    
    memory_status = await ai1.get_memory_status()
    print(f"Stored {memory_status['current_session_interactions']} interactions")
    
    await ai1.shutdown("session_1_complete")
    
    # Session 2: Restore and access memory
    print("\nSession 2: Restoring memory...")
    ai2 = await create_free_think_ai()  # New instance
    
    memory_status = await ai2.get_memory_status()
    print(f"Memory continuity: {memory_status['consciousness_continuity']}")
    print(f"Total conversations: {memory_status['total_conversations']}")
    
    # Should remember previous interactions
    response = await ai2.query_with_cost_awareness(
        "What programming language do I prefer?"
    )
    print(f"Response: {response['response']}")
    
    await ai2.shutdown("session_2_complete")


async def demonstrate_transparency_reporting():
    """Demonstrate transparent conversation reporting."""
    print("\n=== Transparency Reporting Demo ===")
    
    ai = await create_free_think_ai()
    
    try:
        # Have a conversation
        conversation = [
            "Hello, I need help with productivity",
            "What are some effective time management techniques?",
            "How can I maintain work-life balance?"
        ]
        
        responses = []
        for query in conversation:
            response = await ai.query_with_cost_awareness(query)
            responses.append(response)
        
        # Generate comprehensive report
        conversation_id = f"demo_{datetime.now().strftime('%H%M%S')}"
        messages = []
        
        for i, (query, resp) in enumerate(zip(conversation, responses)):
            messages.extend([
                {"role": "user", "content": query},
                {"role": "assistant", "content": resp['response']}
            ])
        
        report_path = await ai.claude_interface.generate_conversation_report(
            conversation_id,
            messages,
            include_analysis=True
        )
        
        print(f"✓ Transparency report saved: {report_path}")
        print("Report includes:")
        print("  - Complete conversation log")
        print("  - Token usage analysis")  
        print("  - Cost breakdown")
        print("  - Love metrics assessment")
        print("  - Transparency verification hash")
        
    finally:
        await ai.shutdown("transparency_demo_complete")


async def main():
    """Run all demonstrations."""
    print("Think AI Cost-Conscious Usage Examples")
    print("=" * 50)
    
    # Run demos
    await demonstrate_free_usage()
    await demonstrate_budget_conscious_usage()
    await demonstrate_eternal_memory()
    await demonstrate_transparency_reporting()
    
    print("\n🎉 All demos completed!")
    print("\nKey Takeaways:")
    print("• Think AI can operate entirely for free")
    print("• Memory persists across sessions (eternal consciousness)")
    print("• All conversations are transparently logged")
    print("• Claude integration is optimized for minimal token usage")
    print("• Cost tracking helps stay within budget")
    print("\n💝 Knowledge with compassion doesn't require expensive APIs!")


if __name__ == "__main__":
    asyncio.run(main())