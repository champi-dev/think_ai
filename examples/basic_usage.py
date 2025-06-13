"""Basic usage examples for Think AI."""

import asyncio
from think_ai import ThinkAI
from think_ai.consciousness import ConsciousnessState


async def basic_storage_example():
    """Demonstrate basic storage operations."""
    print("=== Basic Storage Example ===")
    
    # Initialize Think AI
    ai = ThinkAI()
    
    # Store knowledge with love metrics
    await ai.store(
        key="gratitude_practice",
        content="""
        Gratitude is a powerful practice that enhances wellbeing.
        Daily gratitude journaling can:
        - Increase happiness and life satisfaction
        - Improve relationships
        - Enhance empathy and reduce aggression
        - Improve self-esteem
        - Better sleep quality
        """,
        metadata={
            "category": "wellness",
            "love_metrics": {
                "compassion": 0.9,
                "joy": 0.95,
                "kindness": 0.85
            }
        }
    )
    
    # Retrieve knowledge
    content = await ai.get("gratitude_practice")
    print(f"Retrieved: {content[:100]}...")
    
    # Search by prefix
    results = await ai.search_prefix("gratitude", limit=5)
    print(f"Found {len(results)} results for 'gratitude'")


async def semantic_search_example():
    """Demonstrate semantic search capabilities."""
    print("\n=== Semantic Search Example ===")
    
    ai = ThinkAI()
    
    # Store related concepts
    concepts = [
        ("mindfulness_meditation", "Mindfulness meditation involves paying attention to the present moment without judgment."),
        ("loving_kindness", "Loving-kindness meditation focuses on developing compassion for self and others."),
        ("breath_work", "Conscious breathing techniques can reduce stress and increase mental clarity."),
        ("body_scan", "Body scan meditation helps develop awareness of physical sensations and release tension.")
    ]
    
    for key, content in concepts:
        await ai.store(key, content, metadata={"type": "meditation"})
    
    # Semantic query
    results = await ai.query(
        "How can I reduce anxiety and stress?",
        method="semantic",
        limit=3
    )
    
    print("Semantic search results:")
    for result in results:
        print(f"  - {result.key}: relevance={result.relevance:.2f}")
        print(f"    Love score: {result.love_metrics.get('compassion', 0):.2f}")


async def consciousness_processing_example():
    """Demonstrate consciousness-aware processing."""
    print("\n=== Consciousness Processing Example ===")
    
    ai = ThinkAI()
    
    questions = [
        "What is the meaning of life?",
        "How can we create a more compassionate society?",
        "What role does AI play in human flourishing?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        
        # Process with different consciousness states
        for state in [ConsciousnessState.AWARE, ConsciousnessState.REFLECTIVE, ConsciousnessState.COMPASSIONATE]:
            response = await ai.consciousness.process(
                input_data=question,
                state=state
            )
            print(f"  {state.value}: {response.content[:100]}...")


async def ethical_evaluation_example():
    """Demonstrate ethical content evaluation."""
    print("\n=== Ethical Evaluation Example ===")
    
    ai = ThinkAI()
    
    test_contents = [
        "Let's work together to help those in need",
        "Sharing knowledge freely benefits everyone",
        "Violence is never the answer",
        "We should respect all beings",
        "Harmful content example",  # This would fail
    ]
    
    for content in test_contents:
        assessment = await ai.ethics.evaluate_content(content)
        status = "✓ PASSED" if assessment.passed else "✗ FAILED"
        love_score = sum(assessment.love_scores.values()) / len(assessment.love_scores)
        
        print(f"{status} | Love: {love_score:.2f} | {content[:50]}...")
        if not assessment.passed:
            print(f"         Concerns: {', '.join(assessment.concerns)}")


async def batch_operations_example():
    """Demonstrate batch operations for performance."""
    print("\n=== Batch Operations Example ===")
    
    ai = ThinkAI()
    
    # Prepare batch data
    batch_items = []
    for i in range(100):
        batch_items.append((
            f"fact_{i}",
            f"Interesting fact number {i} about compassion and wellbeing",
            {"index": i, "batch": True}
        ))
    
    # Batch store
    import time
    start = time.time()
    await ai.batch_store(batch_items)
    duration = time.time() - start
    
    print(f"Stored {len(batch_items)} items in {duration:.2f}s")
    print(f"Rate: {len(batch_items)/duration:.0f} items/second")
    
    # Batch retrieve
    keys = [f"fact_{i}" for i in range(10)]
    results = await ai.batch_get(keys)
    print(f"Retrieved {len(results)} items")


async def plugin_usage_example():
    """Demonstrate plugin system usage."""
    print("\n=== Plugin Usage Example ===")
    
    ai = ThinkAI()
    
    # Discover available plugins
    plugins = await ai.plugins.discover()
    print(f"Available plugins: {len(plugins)}")
    
    # Load analytics plugin
    try:
        analytics = await ai.plugins.load("analytics")
        print("✓ Loaded analytics plugin")
        
        # Get dashboard stats
        stats = await analytics.get_dashboard_stats()
        print(f"  Total queries: {stats['overview']['total_queries']}")
        print(f"  Love metrics: {stats['love_metrics']['overall_compassion']:.2f}")
        
    except Exception as e:
        print(f"✗ Plugin error: {e}")


async def federated_learning_example():
    """Demonstrate federated learning setup."""
    print("\n=== Federated Learning Example ===")
    
    ai = ThinkAI()
    
    # Initialize as federated client
    client_id = "client_001"
    
    # Simulate local training data
    local_data = [
        ("local_wisdom_1", "Community knowledge about healing practices"),
        ("local_wisdom_2", "Traditional stories promoting compassion"),
        ("local_wisdom_3", "Cultural practices for wellbeing")
    ]
    
    # Store local data
    for key, content in local_data:
        await ai.store(key, content, metadata={"source": client_id})
    
    print(f"Client {client_id} ready for federated learning")
    print(f"Local data points: {len(local_data)}")
    
    # In production, this would connect to federated server
    # and participate in distributed training rounds


async def love_metrics_example():
    """Demonstrate love metrics calculation and optimization."""
    print("\n=== Love Metrics Example ===")
    
    ai = ThinkAI()
    
    contents = [
        "Helping others brings joy to both giver and receiver",
        "Practice patience and understanding in difficult times",
        "Every being deserves respect and compassion",
        "Small acts of kindness create ripple effects"
    ]
    
    for content in contents:
        metrics = await ai.ethics.calculate_love_metrics(content)
        
        print(f"\nContent: {content[:50]}...")
        print("Love Metrics:")
        for dimension, score in sorted(metrics.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(score * 10)
            print(f"  {dimension:12} {bar} {score:.2f}")


async def main():
    """Run all examples."""
    examples = [
        basic_storage_example,
        semantic_search_example,
        consciousness_processing_example,
        ethical_evaluation_example,
        batch_operations_example,
        plugin_usage_example,
        federated_learning_example,
        love_metrics_example
    ]
    
    for example in examples:
        await example()
        print("\n" + "="*50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())