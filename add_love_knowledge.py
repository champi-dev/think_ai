#!/usr/bin/env python3
"""
Add love and emotion-related knowledge to the knowledge base
"""
import json
from pathlib import Path

# Load existing evaluated knowledge
knowledge_file = Path("./cache/evaluated_knowledge.json")
with open(knowledge_file, 'r') as f:
    data = json.load(f)

# Add love knowledge entry
love_entry = {
    "love": {
        "topic": "love",
        "content": "Love is a complex emotional and psychological state involving deep affection, attachment, and care for another person, thing, or idea. It encompasses romantic love between partners, familial love between relatives, platonic love between friends, and self-love. Neurologically, love activates brain regions associated with reward, motivation, and attachment, releasing hormones like oxytocin and dopamine. Love evolves through stages from initial attraction to deep attachment, playing a crucial role in human bonding, reproduction, and social cooperation.",
        "metadata": {
            "conversational_patterns": [
                "Love is a complex emotional and psychological state involving deep affection, attachment, and care for another person, thing, or idea. It encompasses romantic love between partners, familial love between relatives, platonic love between friends, and self-love. Neurologically, love activates brain regions associated with reward, motivation, and attachment, releasing hormones like oxytocin and dopamine. Love evolves through stages from initial attraction to deep attachment, playing a crucial role in human bonding, reproduction, and social cooperation.",
                "Let me explain love. Love is a complex emotional and psychological state involving deep affection, attachment, and care for another person, thing, or idea. It encompasses romantic love between partners, familial love between relatives, platonic love between friends, and self-love. Neurologically, love activates brain regions associated with reward, motivation, and attachment, releasing hormones like oxytocin and dopamine.",
                "When it comes to love, it's a complex emotional and psychological state involving deep affection, attachment, and care. Love encompasses romantic love between partners, familial love between relatives, platonic love between friends, and self-love. It plays a crucial role in human bonding and social cooperation.",
                "Love is fundamentally about deep affection, attachment, and care for another person, thing, or idea. It manifests as romantic love, familial love, platonic love, and self-love, each serving important roles in human life and relationships."
            ],
            "evaluation_score": 0.95,
            "source": "enhanced_knowledge",
            "generated_at": "2025-08-01T12:00:00"
        },
        "related_concepts": [
            "emotion",
            "attachment",
            "relationships",
            "affection",
            "bonding",
            "romance",
            "caring",
            "compassion",
            "intimacy",
            "what is love",
            "types of love",
            "how does love work"
        ]
    }
}

# Add to knowledge base
data["knowledge_base"].update(love_entry)

# Save updated knowledge
with open(knowledge_file, 'w') as f:
    json.dump(data, f, indent=2)

# Also update response cache
response_cache_file = Path("./cache/response_cache.json")
with open(response_cache_file, 'r') as f:
    cache_data = json.load(f)

# Add love responses
love_responses = {
    "what is love": {
        "response": "Love is a complex emotional and psychological state involving deep affection, attachment, and care for another person, thing, or idea. It encompasses romantic love between partners, familial love between relatives, platonic love between friends, and self-love. Neurologically, love activates brain regions associated with reward, motivation, and attachment, releasing hormones like oxytocin and dopamine. Love evolves through stages from initial attraction to deep attachment, playing a crucial role in human bonding, reproduction, and social cooperation.",
        "timestamp": 1753980000.0
    },
    "love": {
        "response": "Love is a complex emotional and psychological state involving deep affection, attachment, and care for another person, thing, or idea. It encompasses romantic love between partners, familial love between relatives, platonic love between friends, and self-love. Neurologically, love activates brain regions associated with reward, motivation, and attachment, releasing hormones like oxytocin and dopamine.",
        "timestamp": 1753980000.0
    },
    "tell me about love": {
        "response": "Love is fundamentally about deep affection, attachment, and care for another person, thing, or idea. It manifests as romantic love, familial love, platonic love, and self-love, each serving important roles in human life and relationships. Love plays a crucial role in human bonding and social cooperation.",
        "timestamp": 1753980000.0
    },
    "explain love": {
        "response": "Love is a complex emotional and psychological state involving deep affection, attachment, and care. It encompasses romantic love between partners, familial love between relatives, platonic love between friends, and self-love. Love activates brain regions associated with reward and attachment, releasing hormones like oxytocin and dopamine.",
        "timestamp": 1753980000.0
    }
}

cache_data.update(love_responses)

# Save updated cache
with open(response_cache_file, 'w') as f:
    json.dump(cache_data, f, indent=2)

print("✅ Added love knowledge to the knowledge base")
print("✅ Updated response cache with love entries")