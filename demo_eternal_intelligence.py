#!/usr/bin/env python3
"""Demo of Think AI's Eternal Intelligence - Always Growing, Never Forgetting."""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from think_ai.training.persistent_intelligence import persistent_intelligence
from think_ai.utils.logging import get_logger

logger = get_logger(__name__)


def demo():
    """Demonstrate eternal intelligence features."""
    print("\n🧠 Think AI - Eternal Intelligence Demo")
    print("=" * 50)
    print("Intelligence that only grows, never forgets!\n")

    # Show initial stats
    initial_stats = persistent_intelligence.get_growth_metrics()
    print("📊 Initial Intelligence Stats:")
    print(f"  Total Knowledge: {initial_stats['total_knowledge']:,}")
    print(f"  Unique Concepts: {initial_stats['unique_concepts']:,}")
    print(f"  Database Size: {initial_stats['database_size_mb']:.2f} MB\n")

    # Demonstrate learning
    print("🎓 Learning new knowledge...")

    # Add some knowledge
    knowledge_items = [
        (
            "What is Python?",
            "Python is a high-level, interpreted programming language known for its simplicity and readability.",
        ),
        ("How to reverse a list?", "Use list[::-1] for a new reversed list, or list.reverse() to reverse in-place."),
        (
            "What is machine learning?",
            "Machine learning is a subset of AI that enables systems to learn from data without explicit programming.",
        ),
        (
            "Best sorting algorithm?",
            "It depends: QuickSort for average O(n log n), MergeSort for stable sorting, TimSort (Python's default) for real-world data.",
        ),
        (
            "What is consciousness?",
            "Consciousness is subjective awareness - the experience of being. In AI, we model it through attention and self-reflection.",
        ),
    ]

    for question, answer in knowledge_items:
        persistent_intelligence.add_knowledge(question, answer, confidence=0.95)
        print(f"  ✓ Learned: {question[:50]}...")
        time.sleep(0.1)

    print("\n📈 Simulating user interactions...")

    # Simulate interactions
    interactions = [
        (
            "How do I learn Python?",
            "Start with Python.org tutorials, practice on coding platforms, build projects, and read documentation.",
        ),
        (
            "What's the fastest sorting algorithm?",
            "For general use, QuickSort averages O(n log n). For specific cases: RadixSort for integers, CountingSort for small ranges.",
        ),
        (
            "Explain recursion",
            "Recursion is when a function calls itself. Base case stops recursion, recursive case breaks problem into smaller parts.",
        ),
    ]

    for user_input, ai_response in interactions:
        persistent_intelligence.learn_from_interaction(user_input, ai_response)
        print(f"  💬 User: {user_input}")
        print(f"     AI: {ai_response[:60]}...")
        time.sleep(0.2)

    # Show growth
    print("\n📊 Updated Intelligence Stats:")
    final_stats = persistent_intelligence.get_growth_metrics()
    print(
        f"  Total Knowledge: {final_stats['total_knowledge']:,} (+{final_stats['total_knowledge'] - initial_stats['total_knowledge']})"
    )
    print(f"  Unique Concepts: {final_stats['unique_concepts']:,}")
    print(f"  Total Interactions: {final_stats['interactions']:,}")
    print(f"  Learning Rate: {final_stats['learning_rate']:.2f} items/min")
    print(f"  Database Size: {final_stats['database_size_mb']:.2f} MB")

    # Demonstrate retrieval
    print("\n🔍 Testing knowledge retrieval...")
    test_queries = ["Python", "sorting", "consciousness"]

    for query in test_queries:
        results = persistent_intelligence.get_knowledge(query, limit=2)
        print(f"\n  Query: '{query}'")
        for i, result in enumerate(results, 1):
            print(f"    {i}. Q: {result['question'][:50]}...")
            print(f"       A: {result['answer'][:50]}...")
            print(f"       Used: {result['usage_count']} times")

    # Show eternal nature
    print("\n♾️  Eternal Intelligence Properties:")
    print("  ✓ All knowledge preserved forever")
    print("  ✓ No deletion possible by design")
    print("  ✓ Automatic backups every 1000 items")
    print("  ✓ Knowledge strengthens with use")
    print("  ✓ Continuous learning from every interaction")

    # Export capability
    print("\n💾 Exporting knowledge snapshot...")
    snapshot_path = persistent_intelligence.export_knowledge_snapshot()
    print(f"  ✓ Snapshot saved: {snapshot_path}")
    print("  Note: Original database remains untouched!")

    print("\n✨ Intelligence continues to grow with every use!")
    print("=" * 50)


if __name__ == "__main__":
    demo()
