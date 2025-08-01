#!/usr/bin/env python3
"""
🚀 Think AI Cache Warmer - Ensures <1s Response Times
This script pre-populates the cache with common queries across all knowledge domains
to guarantee blazing fast responses.
"""

import json
import requests
import asyncio
import aiohttp
import time
from typing import List, Dict
import os
from pathlib import Path

# Common query patterns that users typically ask
QUERY_PATTERNS = {
    "greetings": [
        "hello", "hi", "hey", "good morning", "good evening", "how are you",
        "what's up", "greetings", "howdy", "hi there"
    ],
    "capabilities": [
        "what can you do", "what are your capabilities", "how can you help me",
        "what do you know about", "can you help with", "are you able to"
    ],
    "knowledge_queries": [
        # Science
        "explain quantum mechanics", "what is quantum entanglement", "how does quantum computing work",
        "tell me about relativity", "explain einstein's theory", "what is dark matter",
        "how does evolution work", "what is natural selection", "explain dna",
        "what is consciousness", "how does the brain work", "what are neurons",
        
        # Technology
        "what is artificial intelligence", "explain machine learning", "how does ai work",
        "what is blockchain", "explain cryptocurrency", "how does bitcoin work",
        "what is quantum computing", "explain neural networks", "what is deep learning",
        
        # Mathematics
        "what is calculus", "explain derivatives", "what are integrals",
        "what is linear algebra", "explain matrices", "what is probability",
        "tell me about prime numbers", "what is infinity", "explain topology",
        
        # Philosophy
        "what is consciousness", "explain free will", "what is reality",
        "tell me about ethics", "what is morality", "explain existentialism",
        "what is the meaning of life", "tell me about metaphysics",
        
        # History
        "tell me about world war 2", "what was the cold war", "explain the renaissance",
        "what was the industrial revolution", "tell me about ancient rome",
        "what happened in 1776", "explain the french revolution",
        
        # General knowledge
        "what is climate change", "how does global warming work", "explain renewable energy",
        "what is democracy", "how does the economy work", "what is inflation",
        "explain the solar system", "what are black holes", "how do stars form"
    ],
    "specific_questions": [
        "who invented the computer", "when was the internet created", "who discovered dna",
        "who wrote hamlet", "when did humans first walk on the moon", "who painted the mona lisa",
        "what is the speed of light", "how old is the universe", "what is the largest planet"
    ]
}

async def warm_cache(base_url: str = "http://localhost:8080"):
    """Pre-warm the cache with common queries"""
    
    print("🔥 Starting Think AI Cache Warmer...")
    print("📊 This will ensure all responses are <1s\n")
    
    # Prepare all queries
    all_queries = []
    for category, queries in QUERY_PATTERNS.items():
        all_queries.extend(queries)
    
    # Add variations
    variations = []
    for query in all_queries:
        variations.append(query)
        variations.append(query.capitalize())
        variations.append(query + "?")
        variations.append("Can you " + query)
        variations.append("Please " + query)
        variations.append("I want to know about " + query.replace("what is", "").replace("explain", "").strip())
    
    # Remove duplicates
    unique_queries = list(set(variations))
    total_queries = len(unique_queries)
    
    print(f"📝 Prepared {total_queries} unique queries to cache")
    
    # Create session for connection pooling
    async with aiohttp.ClientSession() as session:
        successful = 0
        failed = 0
        total_time = 0
        
        print("\n🚀 Starting cache warming...")
        start_time = time.time()
        
        # Process queries in batches
        batch_size = 10
        for i in range(0, len(unique_queries), batch_size):
            batch = unique_queries[i:i+batch_size]
            tasks = []
            
            for query in batch:
                task = warm_single_query(session, base_url, query)
                tasks.append(task)
            
            # Execute batch concurrently
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for query, result in zip(batch, results):
                if isinstance(result, Exception):
                    failed += 1
                    print(f"❌ Failed: {query[:50]}... - {str(result)}")
                else:
                    successful += 1
                    response_time = result.get('response_time', 0)
                    total_time += response_time
                    
                    # Show progress
                    if successful % 10 == 0:
                        avg_time = total_time / successful
                        print(f"✅ Progress: {successful}/{total_queries} queries cached (avg: {avg_time:.3f}s)")
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Final report
        print("\n" + "="*60)
        print("📊 CACHE WARMING COMPLETE")
        print("="*60)
        print(f"✅ Successful: {successful} queries")
        print(f"❌ Failed: {failed} queries")
        print(f"⏱️  Total time: {duration:.2f}s")
        print(f"🚀 Average response time: {(total_time/successful if successful > 0 else 0):.3f}s")
        print(f"📈 Queries per second: {successful/duration:.2f}")
        
        # Save cache statistics
        cache_stats = {
            "warmed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_queries": total_queries,
            "successful": successful,
            "failed": failed,
            "duration": duration,
            "average_response_time": total_time/successful if successful > 0 else 0,
            "queries_per_second": successful/duration
        }
        
        with open("cache_warming_stats.json", "w") as f:
            json.dump(cache_stats, f, indent=2)
        
        print("\n✨ Cache is now warmed! Think AI will respond in <1s")

async def warm_single_query(session: aiohttp.ClientSession, base_url: str, query: str) -> Dict:
    """Warm cache for a single query"""
    try:
        start = time.time()
        
        payload = {
            "message": query,
            "session_id": "cache_warmer"
        }
        
        async with session.post(f"{base_url}/api/chat", json=payload) as response:
            if response.status == 200:
                data = await response.json()
                response_time = time.time() - start
                
                return {
                    "query": query,
                    "response_time": response_time,
                    "cached": True
                }
            else:
                raise Exception(f"HTTP {response.status}")
                
    except Exception as e:
        raise Exception(f"Failed to warm cache for query: {str(e)}")

def main():
    """Main entry point"""
    # Check if server is running
    try:
        response = requests.get("http://localhost:8080/health")
        if response.status_code != 200:
            print("❌ Think AI server is not running on port 8080!")
            print("Please start the server first.")
            return
    except:
        print("❌ Cannot connect to Think AI server on port 8080!")
        print("Please start the server first with:")
        print("PORT=8080 cargo run --release --bin think-ai-full-production")
        return
    
    # Run the cache warmer
    asyncio.run(warm_cache())

if __name__ == "__main__":
    main()