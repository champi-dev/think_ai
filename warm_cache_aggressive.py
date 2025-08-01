#!/usr/bin/env python3
"""
Aggressive cache warming script for Think AI
Trades disk space for ultra-fast responses by pre-computing and caching responses
"""

import json
import hashlib
import asyncio
import aiohttp
import time
from pathlib import Path
from typing import Dict, List, Tuple
import re
from itertools import product

# Configuration
API_URL = "http://localhost:7777/api/chat"
CACHE_DIR = Path("cache/precomputed_responses")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Common question patterns with variations
QUESTION_TEMPLATES = {
    "math": [
        "what is {} + {}",
        "calculate {} plus {}",
        "{} + {} equals",
        "add {} and {}",
        "sum of {} and {}"
    ],
    "definition": [
        "what is {}",
        "define {}",
        "explain {}",
        "tell me about {}",
        "describe {}"
    ],
    "how_to": [
        "how do I {}",
        "how to {}",
        "steps to {}",
        "guide for {}",
        "tutorial on {}"
    ],
    "comparison": [
        "difference between {} and {}",
        "{} vs {}",
        "compare {} and {}",
        "{} versus {}",
        "which is better {} or {}"
    ]
}

# Common topics for each category
TOPICS = {
    "math": [(i, j) for i in range(1, 11) for j in range(1, 11)],  # Basic math up to 10
    "definition": [
        "artificial intelligence", "machine learning", "quantum computing",
        "blockchain", "cryptocurrency", "neural networks", "deep learning",
        "consciousness", "philosophy", "psychology", "biology", "physics",
        "chemistry", "mathematics", "computer science", "engineering",
        "climate change", "global warming", "renewable energy", "democracy",
        "capitalism", "socialism", "economics", "history", "literature"
    ],
    "how_to": [
        "code", "program", "learn python", "use git", "build a website",
        "learn machine learning", "start a business", "invest money",
        "stay healthy", "lose weight", "build muscle", "meditate",
        "reduce stress", "be productive", "manage time", "study effectively"
    ],
    "comparison": [
        ("python", "java"), ("react", "angular"), ("tensorflow", "pytorch"),
        ("aws", "azure"), ("docker", "kubernetes"), ("sql", "nosql"),
        ("rest", "graphql"), ("tcp", "udp"), ("http", "https"),
        ("classical computing", "quantum computing")
    ]
}

def generate_cache_key(query: str) -> str:
    """Generate a consistent cache key for a query"""
    normalized = query.lower().strip()
    # Remove extra spaces and punctuation
    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    return hashlib.sha256(normalized.encode()).hexdigest()[:16]

async def fetch_response(session: aiohttp.ClientSession, query: str) -> Tuple[str, str]:
    """Fetch response from API"""
    try:
        async with session.post(API_URL, json={"message": query}, timeout=30) as resp:
            if resp.status == 200:
                data = await resp.json()
                return query, data.get("response", "")
    except Exception as e:
        print(f"Error fetching '{query}': {e}")
    return query, ""

async def warm_cache_batch(queries: List[str], session: aiohttp.ClientSession) -> Dict[str, str]:
    """Fetch responses for a batch of queries"""
    tasks = [fetch_response(session, query) for query in queries]
    results = await asyncio.gather(*tasks)
    return {query: response for query, response in results if response}

def save_cache_batch(cache_data: Dict[str, str]):
    """Save cache data to disk"""
    for query, response in cache_data.items():
        if response:  # Only save non-empty responses
            cache_key = generate_cache_key(query)
            cache_file = CACHE_DIR / f"{cache_key}.json"
            
            cache_entry = {
                "query": query,
                "response": response,
                "timestamp": time.time(),
                "normalized_query": query.lower().strip()
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_entry, f, indent=2)

async def generate_all_queries() -> List[str]:
    """Generate all query variations"""
    queries = []
    
    # Math queries
    for template in QUESTION_TEMPLATES["math"]:
        for (a, b) in TOPICS["math"]:
            queries.append(template.format(a, b))
    
    # Definition queries
    for template in QUESTION_TEMPLATES["definition"]:
        for topic in TOPICS["definition"]:
            queries.append(template.format(topic))
    
    # How-to queries
    for template in QUESTION_TEMPLATES["how_to"]:
        for topic in TOPICS["how_to"]:
            queries.append(template.format(topic))
    
    # Comparison queries
    for template in QUESTION_TEMPLATES["comparison"]:
        for (a, b) in TOPICS["comparison"]:
            queries.append(template.format(a, b))
    
    # Add common conversational queries
    queries.extend([
        "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
        "how are you", "how are you doing", "what's up", "how's it going",
        "thank you", "thanks", "thank you so much", "thanks a lot",
        "goodbye", "bye", "see you later", "talk to you later",
        "yes", "no", "okay", "ok", "sure", "alright",
        "i don't understand", "can you explain", "what do you mean",
        "can you help me", "i need help", "help me please",
        "tell me a joke", "make me laugh", "say something funny",
        "what's your name", "who are you", "what are you"
    ])
    
    return list(set(queries))  # Remove duplicates

async def main():
    """Main cache warming function"""
    print("🔥 Starting aggressive cache warming for Think AI...")
    
    # Check if Think AI is running
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:7777/health") as resp:
                if resp.status != 200:
                    print("❌ Think AI is not running on port 7777!")
                    return
    except:
        print("❌ Cannot connect to Think AI on port 7777!")
        return
    
    # Generate all queries
    all_queries = await generate_all_queries()
    print(f"📝 Generated {len(all_queries)} unique queries to cache")
    
    # Load existing cache to avoid re-fetching
    existing_cache = set()
    for cache_file in CACHE_DIR.glob("*.json"):
        existing_cache.add(cache_file.stem)
    
    # Filter out already cached queries
    queries_to_fetch = [q for q in all_queries if generate_cache_key(q) not in existing_cache]
    print(f"🔍 Found {len(existing_cache)} existing cached responses")
    print(f"📥 Need to fetch {len(queries_to_fetch)} new responses")
    
    if not queries_to_fetch:
        print("✅ Cache is already fully warmed!")
        return
    
    # Warm cache in batches
    batch_size = 10
    async with aiohttp.ClientSession() as session:
        for i in range(0, len(queries_to_fetch), batch_size):
            batch = queries_to_fetch[i:i+batch_size]
            print(f"🔄 Processing batch {i//batch_size + 1}/{(len(queries_to_fetch) + batch_size - 1)//batch_size}...")
            
            cache_data = await warm_cache_batch(batch, session)
            save_cache_batch(cache_data)
            
            # Brief pause to avoid overwhelming the server
            await asyncio.sleep(1)
    
    # Generate summary
    total_cached = len(list(CACHE_DIR.glob("*.json")))
    total_size_mb = sum(f.stat().st_size for f in CACHE_DIR.glob("*.json")) / (1024 * 1024)
    
    print("\n✅ Cache warming complete!")
    print(f"📊 Total cached responses: {total_cached}")
    print(f"💾 Total cache size: {total_size_mb:.2f} MB")
    print(f"⚡ Average size per response: {(total_size_mb * 1024 / total_cached):.2f} KB")
    
    # Save cache statistics
    stats = {
        "total_responses": total_cached,
        "cache_size_mb": total_size_mb,
        "queries_generated": len(all_queries),
        "timestamp": time.time(),
        "categories": {
            "math": len(QUESTION_TEMPLATES["math"]) * len(TOPICS["math"]),
            "definition": len(QUESTION_TEMPLATES["definition"]) * len(TOPICS["definition"]),
            "how_to": len(QUESTION_TEMPLATES["how_to"]) * len(TOPICS["how_to"]),
            "comparison": len(QUESTION_TEMPLATES["comparison"]) * len(TOPICS["comparison"])
        }
    }
    
    with open("cache/cache_warming_stats.json", "w") as f:
        json.dump(stats, f, indent=2)

if __name__ == "__main__":
    asyncio.run(main())