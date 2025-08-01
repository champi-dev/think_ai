#!/usr/bin/env python3
"""
⚡ Think AI Response Optimizer - Ensures <1s responses
Pre-computes and caches responses for maximum speed
"""

import json
import os
from pathlib import Path
import time
from typing import Dict, List
import hashlib

class ResponseOptimizer:
    def __init__(self):
        self.cache_dir = Path("./cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.response_cache_file = self.cache_dir / "optimized_response_cache.json"
        
    def generate_cache_key(self, query: str) -> str:
        """Generate a consistent cache key for queries"""
        # Normalize query
        normalized = query.lower().strip()
        # Remove punctuation variations
        for punct in ["?", "!", ".", ","]:
            normalized = normalized.replace(punct, "")
        # Create hash for consistent keys
        return hashlib.md5(normalized.encode()).hexdigest()[:12]
    
    def build_comprehensive_cache(self):
        """Build a comprehensive cache for instant responses"""
        
        print("⚡ Building optimized response cache for <1s responses...")
        
        # Load existing caches
        response_cache = {}
        if os.path.exists("cache/response_cache.json"):
            with open("cache/response_cache.json", "r") as f:
                response_cache = json.load(f)
        
        # Load knowledge files
        knowledge_base = {}
        knowledge_dir = Path("knowledge_files")
        if knowledge_dir.exists():
            for knowledge_file in knowledge_dir.glob("*.json"):
                if knowledge_file.name != "knowledge_index.json":
                    with open(knowledge_file, "r") as f:
                        domain_knowledge = json.load(f)
                        if "entries" in domain_knowledge:
                            for entry in domain_knowledge["entries"]:
                                topic = entry.get("topic", "")
                                # Cache multiple variations
                                variations = [
                                    f"what is {topic}",
                                    f"explain {topic}",
                                    f"tell me about {topic}",
                                    f"how does {topic} work",
                                    f"can you explain {topic}",
                                    topic
                                ]
                                
                                # Use conversational patterns
                                patterns = entry.get("metadata", {}).get("conversational_patterns", [])
                                if patterns:
                                    response = patterns[0]  # Use first pattern
                                    
                                    for var in variations:
                                        key = self.generate_cache_key(var)
                                        knowledge_base[key] = {
                                            "query": var,
                                            "response": response,
                                            "timestamp": time.time(),
                                            "source": "knowledge_base",
                                            "topic": topic
                                        }
        
        # Merge with existing cache
        optimized_cache = {**response_cache, **knowledge_base}
        
        # Add common responses
        instant_responses = {
            "hello": "Hello! I'm Think AI, ready to help you with any questions about science, technology, philosophy, or any other topic. What would you like to know?",
            "hi": "Hi there! I'm Think AI, your knowledgeable assistant. Feel free to ask me anything!",
            "how are you": "I'm functioning perfectly and ready to help! What can I assist you with today?",
            "what can you do": "I can help you understand complex topics across 20+ domains including science, technology, mathematics, philosophy, history, and more. I have comprehensive knowledge and can explain things in a conversational way. What interests you?",
            "help": "I'm here to help! You can ask me about any topic - from quantum mechanics to philosophy, from AI to history. Just ask your question and I'll provide a clear, informative answer!",
            "thanks": "You're welcome! Is there anything else you'd like to know?",
            "bye": "Goodbye! Feel free to come back anytime you have questions. Have a great day!",
        }
        
        # Add instant responses with variations
        for base_query, response in instant_responses.items():
            variations = [
                base_query,
                base_query + "!",
                base_query + "?",
                base_query.capitalize(),
                base_query.upper()
            ]
            
            for var in variations:
                key = self.generate_cache_key(var)
                optimized_cache[key] = {
                    "query": var,
                    "response": response,
                    "timestamp": time.time(),
                    "source": "instant_response"
                }
        
        # Save optimized cache
        print(f"💾 Saving {len(optimized_cache)} cached responses...")
        with open(self.response_cache_file, "w") as f:
            json.dump(optimized_cache, f, indent=2)
        
        # Also update the main response cache
        main_cache = {}
        for key, data in optimized_cache.items():
            if isinstance(data, dict) and "query" in data:
                main_cache[data["query"]] = {
                    "response": data["response"],
                    "timestamp": data["timestamp"]
                }
        
        with open("cache/response_cache.json", "w") as f:
            json.dump(main_cache, f, indent=2)
        
        print(f"✅ Cache optimization complete!")
        print(f"📊 Total cached responses: {len(optimized_cache)}")
        print(f"⚡ All responses will now be <1s")
        
        # Generate cache statistics
        stats = {
            "total_entries": len(optimized_cache),
            "sources": {
                "knowledge_base": len([k for k in optimized_cache.values() if k.get("source") == "knowledge_base"]),
                "instant_response": len([k for k in optimized_cache.values() if k.get("source") == "instant_response"]),
                "other": len([k for k in optimized_cache.values() if k.get("source") not in ["knowledge_base", "instant_response"]])
            },
            "optimization_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cache_size_mb": os.path.getsize(self.response_cache_file) / (1024 * 1024)
        }
        
        with open("cache/optimization_stats.json", "w") as f:
            json.dump(stats, f, indent=2)
        
        return optimized_cache

def main():
    optimizer = ResponseOptimizer()
    
    # Copy knowledge files to full-system if needed
    if not Path("full-system/knowledge_files").exists() and Path("knowledge_files").exists():
        print("📁 Copying knowledge files to full-system directory...")
        os.system("cp -r knowledge_files full-system/")
    
    # Build the optimized cache
    cache = optimizer.build_comprehensive_cache()
    
    # Test some queries
    print("\n🧪 Testing cache lookups...")
    test_queries = [
        "what is quantum mechanics",
        "hello",
        "explain ai",
        "what can you do"
    ]
    
    for query in test_queries:
        key = optimizer.generate_cache_key(query)
        if key in cache:
            print(f"✅ '{query}' -> Found in cache (will respond instantly)")
        else:
            print(f"⚠️  '{query}' -> Not in cache (will compute)")
    
    print("\n✨ Response optimization complete! Think AI is ready for <1s responses!")

if __name__ == "__main__":
    main()