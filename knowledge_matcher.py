#!/usr/bin/env python3
"""
Knowledge Matcher - Properly matches queries to knowledge base entries
"""

import json
from pathlib import Path
from difflib import SequenceMatcher
import re

class KnowledgeMatcher:
    def __init__(self):
        self.knowledge = self.load_knowledge()
        
    def load_knowledge(self):
        """Load knowledge from evaluated_knowledge.json"""
        knowledge_file = Path("./cache/evaluated_knowledge.json")
        if knowledge_file.exists():
            with open(knowledge_file, 'r') as f:
                data = json.load(f)
                return data.get("knowledge_base", {})
        return {}
    
    def find_best_match(self, query):
        """Find the best matching knowledge entry for a query"""
        query_lower = query.lower().strip()
        
        # Remove common words
        query_words = set(query_lower.split()) - {'what', 'is', 'are', 'the', 'a', 'an', 'tell', 'me', 'about', 'explain'}
        
        best_score = 0
        best_topic = None
        
        for topic, data in self.knowledge.items():
            score = 0
            topic_lower = topic.lower()
            
            # Check exact match
            if query_lower == topic_lower:
                return data["content"]
            
            # Check if topic is in query
            if topic_lower in query_lower:
                score += 3
            
            # Check word overlap
            topic_words = set(topic_lower.split())
            overlap = len(query_words & topic_words)
            score += overlap * 2
            
            # Use fuzzy matching
            similarity = SequenceMatcher(None, query_lower, topic_lower).ratio()
            score += similarity * 2
            
            # Check related concepts
            related = data.get("related_concepts", [])
            for concept in related:
                if concept.lower() in query_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_topic = topic
        
        if best_score > 1 and best_topic:
            return self.knowledge[best_topic]["content"]
        
        return None

# Export for use in other modules
knowledge_matcher = KnowledgeMatcher()
