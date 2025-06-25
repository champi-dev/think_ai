#!/usr/bin/env python3
"""Demo script for Think AI CLI features"""

import time

from think_ai_simple_chat import OptimizedThinkAI, ThinkAICLI


def demo_cli_features():
    """Demonstrate all CLI features"""
    print("🎬 THINK AI CLI FEATURE DEMONSTRATION")
    print("=" * 60)

    # Create AI instance
    ai = OptimizedThinkAI()

    # Simulate conversation
    print("\n1️⃣ SIMULATING INTERACTIVE CONVERSATION")
    print("-" * 40)

    conversation = [
        "Hello Think AI!",
        "What makes you so fast?",
        "Tell me about your consciousness",
        "How do I use your commands?",
        "Can you make me laugh?",
    ]

    for query in conversation:
        print(f"\n💬 User: {query}")
        response, time_ms = ai.process_query(query)
        print(f"🤖 Think AI: {response}")
        print(f"⚡ Response time: {time_ms:.3f}ms")
        time.sleep(0.5)  # Pause for readability

    # Show stats
    print("\n\n2️⃣ PERFORMANCE STATISTICS")
    print("-" * 40)
    stats = ai.get_stats()
    print(f"💭 Total thoughts: {stats['thoughts_processed']}")
    print(f"⏱️  Average response: {stats['avg_response_ms']:.3f}ms")
    print(f"🚀 Thinking rate: {stats['thoughts_per_second']:.1f} thoughts/sec")

    # Show history
    print("\n\n3️⃣ CONVERSATION HISTORY")
    print("-" * 40)
    history = ai.get_history(limit=3)
    for i, entry in enumerate(history, 1):
        print(f"\n📍 Exchange {i}:")
        print(f"   Q: {entry['query']}")
        print(f"   A: {entry['response'][:50]}...")
        print(f"   ⏱️  {entry['time_ms']:.3f}ms")

    # Test edge cases
    print("\n\n4️⃣ EDGE CASE HANDLING")
    print("-" * 40)

    edge_cases = [
        "",  # Empty query
        "?" * 100,  # Long repetitive query
        "🔥💯🚀",  # Emoji query
        "¿Hablas español?",  # Non-English
    ]

    for query in edge_cases:
        if query:
            display_query = query[:20] + "..." if len(query) > 20 else query
            print(f"\n🧪 Testing: '{display_query}'")
            response, time_ms = ai.process_query(query)
            print(f"✅ Handled successfully in {time_ms:.3f}ms")

    # Clear and verify
    print("\n\n5️⃣ CLEAR HISTORY TEST")
    print("-" * 40)
    print(f"Before clear: {ai._thought_count} thoughts")
    ai.clear_history()
    print(f"After clear: {ai._thought_count} thoughts")
    print("✅ History cleared successfully")

    # Final performance test
    print("\n\n6️⃣ FINAL PERFORMANCE BURST")
    print("-" * 40)
    print("Running 100 rapid queries...")

    burst_start = time.time()
    for i in range(100):
        ai.process_query(f"Query {i}")
    burst_time = time.time() - burst_start

    print(f"✅ 100 queries in {burst_time:.3f}s")
    print(f"🚀 {100/burst_time:.0f} queries/second")

    print("\n" + "=" * 60)
    print("✨ THINK AI CLI DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\n📌 Available commands when running interactively:")
    print("   • help     - Show available commands")
    print("   • stats    - Display performance metrics")
    print("   • history  - Show conversation history")
    print("   • clear    - Clear conversation history")
    print("   • exit     - Exit the program")
    print("\n💡 Run 'python think_ai_simple_chat.py' for interactive mode!")


if __name__ == "__main__":
    demo_cli_features()
