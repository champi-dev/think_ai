"""Advanced usage scenarios for Think AI."""

import asyncio
import numpy as np
from typing import List, Dict, Any
from datetime import datetime, timedelta

from think_ai import ThinkAI
from think_ai.consciousness import ConsciousnessState, GlobalWorkspace
from think_ai.storage import IndexedStorageBackend
from think_ai.plugins import PluginManager, PluginContext


async def knowledge_graph_reasoning():
    """Complex reasoning using knowledge graph."""
    print("=== Knowledge Graph Reasoning ===")
    
    ai = ThinkAI()
    
    # Build a knowledge graph about wellbeing
    concepts = [
        ("meditation", {"type": "practice", "benefit": "mental_clarity"}),
        ("exercise", {"type": "practice", "benefit": "physical_health"}),
        ("nutrition", {"type": "practice", "benefit": "energy"}),
        ("sleep", {"type": "practice", "benefit": "recovery"}),
        ("social_connection", {"type": "practice", "benefit": "emotional_wellbeing"}),
        ("wellbeing", {"type": "outcome", "components": 5})
    ]
    
    # Add concepts
    concept_ids = {}
    for name, properties in concepts:
        concept_id = await ai.graph.add_concept(name, properties)
        concept_ids[name] = concept_id
    
    # Add relationships
    relationships = [
        ("meditation", "wellbeing", "CONTRIBUTES_TO"),
        ("exercise", "wellbeing", "CONTRIBUTES_TO"),
        ("nutrition", "wellbeing", "CONTRIBUTES_TO"),
        ("sleep", "wellbeing", "CONTRIBUTES_TO"),
        ("social_connection", "wellbeing", "CONTRIBUTES_TO"),
        ("meditation", "sleep", "IMPROVES"),
        ("exercise", "sleep", "IMPROVES"),
        ("social_connection", "meditation", "ENHANCES")
    ]
    
    for from_concept, to_concept, rel_type in relationships:
        await ai.graph.add_relationship(
            concept_ids[from_concept],
            concept_ids[to_concept],
            rel_type
        )
    
    # Query the graph
    print("\nFinding paths to wellbeing:")
    paths = await ai.graph.find_paths_to("wellbeing", max_depth=3)
    for path in paths[:5]:
        path_str = " -> ".join([node.name for node in path])
        print(f"  {path_str}")
    
    # Find related concepts
    print("\nConcepts related to meditation:")
    related = await ai.graph.find_related("meditation", max_depth=2)
    for concept in related:
        print(f"  - {concept.name} ({concept.properties.get('type', 'unknown')})")


async def multi_modal_processing():
    """Process multiple types of content with consciousness."""
    print("\n=== Multi-Modal Processing ===")
    
    ai = ThinkAI()
    
    # Different content types
    contents = {
        "text": "The practice of loving-kindness meditation",
        "structured": {
            "practice": "gratitude",
            "benefits": ["happiness", "relationships", "health"],
            "duration": "5 minutes daily"
        },
        "numerical": np.array([0.8, 0.9, 0.7, 0.85, 0.95]),  # Love metrics over time
        "temporal": [
            {"timestamp": datetime.now() - timedelta(days=i), "mood": 0.6 + i*0.05}
            for i in range(7)
        ]
    }
    
    # Process each type with appropriate consciousness state
    for content_type, content in contents.items():
        print(f"\nProcessing {content_type} content:")
        
        # Choose consciousness state based on content type
        if content_type == "numerical":
            state = ConsciousnessState.FOCUSED
        elif content_type == "temporal":
            state = ConsciousnessState.REFLECTIVE
        else:
            state = ConsciousnessState.AWARE
        
        result = await ai.consciousness.process(content, state=state)
        print(f"  State: {state.value}")
        print(f"  Insight: {result.insight[:100]}...")
        print(f"  Confidence: {result.confidence:.2f}")


async def distributed_knowledge_synthesis():
    """Synthesize knowledge from multiple sources."""
    print("\n=== Distributed Knowledge Synthesis ===")
    
    ai = ThinkAI()
    
    # Simulate multiple knowledge sources
    sources = {
        "scientific": [
            ("neuroscience_meditation", "Meditation changes brain structure in 8 weeks"),
            ("psychology_compassion", "Compassion training reduces implicit bias"),
            ("biology_stress", "Chronic stress impacts immune function")
        ],
        "wisdom_traditions": [
            ("buddhist_mindfulness", "Mindfulness is awareness without judgment"),
            ("stoic_virtue", "Virtue is the sole good according to Stoics"),
            ("indigenous_connection", "All beings are interconnected in the web of life")
        ],
        "personal_experiences": [
            ("user_story_1", "Daily meditation helped me overcome anxiety"),
            ("user_story_2", "Practicing gratitude transformed my relationships"),
            ("user_story_3", "Nature connection brought deep peace")
        ]
    }
    
    # Store knowledge from each source
    source_metadata = {}
    for source_type, items in sources.items():
        for key, content in items:
            await ai.store(
                key,
                content,
                metadata={
                    "source_type": source_type,
                    "timestamp": datetime.now(),
                    "confidence": 0.8 if source_type == "scientific" else 0.7
                }
            )
            source_metadata[key] = source_type
    
    # Synthesize knowledge on a topic
    query = "How can we cultivate lasting wellbeing?"
    
    print(f"\nSynthesizing knowledge for: {query}")
    
    # Get relevant knowledge from each source type
    synthesis = {}
    for source_type in sources.keys():
        results = await ai.query(
            query,
            method="semantic",
            filters={"source_type": source_type},
            limit=2
        )
        synthesis[source_type] = results
    
    # Create integrated response
    print("\nIntegrated Synthesis:")
    for source_type, results in synthesis.items():
        print(f"\n{source_type.replace('_', ' ').title()}:")
        for result in results:
            print(f"  - {result.content[:80]}...")
    
    # Generate final synthesis with COMPASSIONATE state
    final_synthesis = await ai.consciousness.process(
        {
            "query": query,
            "knowledge": synthesis,
            "intent": "integrate_wisdom"
        },
        state=ConsciousnessState.COMPASSIONATE
    )
    
    print(f"\nFinal Synthesis:\n{final_synthesis.content}")


async def real_time_collaboration():
    """Demonstrate real-time collaborative knowledge building."""
    print("\n=== Real-Time Collaboration ===")
    
    ai = ThinkAI()
    
    # Simulate multiple collaborators
    collaborators = ["Alice", "Bob", "Carol"]
    
    # Each collaborator adds knowledge
    contributions = {
        "Alice": [
            ("community_garden", "Community gardens foster connection and provide fresh food"),
            ("skill_sharing", "Skill sharing strengthens community bonds")
        ],
        "Bob": [
            ("renewable_energy", "Solar cooperatives make clean energy accessible"),
            ("tool_library", "Tool libraries reduce consumption through sharing")
        ],
        "Carol": [
            ("time_banking", "Time banking creates equality through hour-for-hour exchange"),
            ("community_kitchen", "Community kitchens address food insecurity together")
        ]
    }
    
    # Add contributions with collaboration metadata
    collab_session = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    for collaborator, items in contributions.items():
        for key, content in items:
            await ai.store(
                key,
                content,
                metadata={
                    "collaborator": collaborator,
                    "session": collab_session,
                    "timestamp": datetime.now(),
                    "collaborative": True
                }
            )
            print(f"{collaborator} added: {key}")
    
    # Find connections between contributions
    print("\nFinding collaborative insights:")
    
    # Query for community building ideas
    results = await ai.query(
        "How can communities work together?",
        method="semantic",
        filters={"session": collab_session}
    )
    
    print(f"Found {len(results)} collaborative insights")
    
    # Show how different perspectives complement each other
    perspectives = {}
    for result in results:
        collaborator = result.metadata.get("collaborator", "Unknown")
        if collaborator not in perspectives:
            perspectives[collaborator] = []
        perspectives[collaborator].append(result.key)
    
    print("\nPerspectives by collaborator:")
    for collaborator, keys in perspectives.items():
        print(f"  {collaborator}: {', '.join(keys)}")


async def adaptive_consciousness_example():
    """Demonstrate adaptive consciousness based on context."""
    print("\n=== Adaptive Consciousness ===")
    
    ai = ThinkAI()
    
    # Create custom global workspace
    workspace = GlobalWorkspace(
        num_processes=5,
        attention_threshold=0.6
    )
    
    # Different contexts requiring different consciousness states
    contexts = [
        {
            "situation": "Crisis support needed",
            "input": "Someone is experiencing severe anxiety",
            "optimal_state": ConsciousnessState.COMPASSIONATE,
            "priority": "emotional_support"
        },
        {
            "situation": "Complex problem solving",
            "input": "Design a sustainable city infrastructure",
            "optimal_state": ConsciousnessState.REFLECTIVE,
            "priority": "systematic_analysis"
        },
        {
            "situation": "Quick decision needed",
            "input": "Should I take this opportunity?",
            "optimal_state": ConsciousnessState.FOCUSED,
            "priority": "clarity"
        },
        {
            "situation": "Learning new concept",
            "input": "Explain quantum entanglement simply",
            "optimal_state": ConsciousnessState.AWARE,
            "priority": "understanding"
        }
    ]
    
    for context in contexts:
        print(f"\n{context['situation']}:")
        print(f"Input: {context['input']}")
        
        # Adapt consciousness state
        response = await ai.consciousness.process(
            input_data=context['input'],
            state=context['optimal_state'],
            context={
                "priority": context['priority'],
                "workspace": workspace
            }
        )
        
        print(f"State: {context['optimal_state'].value}")
        print(f"Response: {response.content[:150]}...")
        print(f"Attention focus: {response.attention_focus}")


async def love_optimization_pipeline():
    """Optimize content for maximum love alignment."""
    print("\n=== Love Optimization Pipeline ===")
    
    ai = ThinkAI()
    
    # Content to optimize
    original_content = [
        "We need to solve this problem",
        "This approach might work",
        "Users should follow these rules",
        "The system processes data"
    ]
    
    print("Original content:")
    for content in original_content:
        print(f"  - {content}")
    
    print("\nOptimizing for love alignment:")
    
    optimized_content = []
    for content in original_content:
        # Calculate initial love metrics
        initial_metrics = await ai.ethics.calculate_love_metrics(content)
        initial_score = sum(initial_metrics.values()) / len(initial_metrics)
        
        # Optimize with love-based language model
        optimized = await ai.models.generate_with_love(
            prompt=f"Rewrite with more compassion and kindness: {content}",
            love_dimension="compassion"
        )
        
        # Calculate improved metrics
        final_metrics = await ai.ethics.calculate_love_metrics(optimized)
        final_score = sum(final_metrics.values()) / len(final_metrics)
        
        improvement = (final_score - initial_score) / initial_score * 100
        
        print(f"\n  Original: {content}")
        print(f"  Optimized: {optimized}")
        print(f"  Love improvement: +{improvement:.1f}%")
        
        optimized_content.append(optimized)
    
    return optimized_content


async def main():
    """Run all advanced scenarios."""
    scenarios = [
        knowledge_graph_reasoning,
        multi_modal_processing,
        distributed_knowledge_synthesis,
        real_time_collaboration,
        adaptive_consciousness_example,
        love_optimization_pipeline
    ]
    
    for scenario in scenarios:
        try:
            await scenario()
            print("\n" + "="*60 + "\n")
        except Exception as e:
            print(f"Error in {scenario.__name__}: {e}")
            print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())