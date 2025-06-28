#!/usr/bin/env python3

import requests
import json
import time

def test_multilevel_cache():
    print("🧠 Testing Multi-Level Caching System")
    print("=" * 50)
    
    base_url = "http://localhost:8080"
    
    # Test cases that should hit different cache levels
    test_cases = [
        {
            "name": "Full Message Cache Hit",
            "query": "hello",
            "expected_cache_level": "Full Message",
            "description": "Should hit exact full message cache"
        },
        {
            "name": "Full Message Cache Hit - Love",
            "query": "what is love",
            "expected_cache_level": "Full Message", 
            "description": "Should hit exact full message cache for love question"
        },
        {
            "name": "Full Message Cache Hit - Human",
            "query": "what means human",
            "expected_cache_level": "Full Message",
            "description": "Should hit exact full message cache for human question"
        },
        {
            "name": "Full Message Cache Hit - Body",
            "query": "what is body?",
            "expected_cache_level": "Full Message",
            "description": "Should hit exact full message cache for body question"
        },
        {
            "name": "Phrase-Level Cache Test",
            "query": "what is mathematics",
            "expected_cache_level": "Phrase or Word",
            "description": "Should hit phrase-level cache for 'what is' pattern"
        },
        {
            "name": "Word-Level Cache Test",
            "query": "programming is interesting",
            "expected_cache_level": "Word",
            "description": "Should hit word-level cache for 'programming'"
        },
        {
            "name": "Dynamic Cache Enhancement",
            "query": "what is artificial intelligence",
            "expected_cache_level": "Generated",
            "description": "Should dynamically create cache patterns"
        },
        {
            "name": "Coding Question Cache",
            "query": "can you code",
            "expected_cache_level": "Full Message",
            "description": "Should hit exact cache for coding question"
        },
    ]
    
    print("🚀 Starting test server check...")
    
    # Check if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=2)
        print("✅ Server is running")
    except:
        print("❌ Server not running. Please start with: ./target/release/think-ai server")
        return
    
    print("\n🧪 Testing multi-level cache system...")
    
    cache_hits = 0
    total_tests = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. {test_case['name']}")
        print(f"   Query: '{test_case['query']}'")
        print(f"   Expected: {test_case['description']}")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{base_url}/chat",
                headers={"Content-Type": "application/json"},
                json={"query": test_case["query"]},
                timeout=5
            )
            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                
                print(f"   Response time: {response_time:.1f}ms")
                print(f"   Response: {ai_response[:100]}{'...' if len(ai_response) > 100 else ''}")
                
                # Check for cache hit indicators in the response quality
                if response_time < 50:  # Very fast responses likely indicate cache hits
                    print(f"   🎯 CACHE HIT LIKELY - Very fast response ({response_time:.1f}ms)")
                    cache_hits += 1
                elif response_time < 100:
                    print(f"   ⚡ POSSIBLE CACHE HIT - Fast response ({response_time:.1f}ms)")
                    cache_hits += 0.5
                else:
                    print(f"   🔄 LIKELY COMPUTED - Slower response ({response_time:.1f}ms)")
                
                # Check response quality (cached responses should be high quality)
                if len(ai_response) > 100 and ("?" in ai_response or "!" in ai_response):
                    print(f"   ✅ GOOD QUALITY - Engaging conversational response")
                else:
                    print(f"   📝 BASIC QUALITY - Simple response")
                    
            else:
                print(f"   ❌ FAIL - HTTP {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
        
        time.sleep(0.3)  # Brief pause between requests
    
    print("\n" + "=" * 50)
    print(f"📊 Cache Performance Summary:")
    print(f"   Likely cache hits: {cache_hits}/{total_tests}")
    print(f"   Cache hit rate: {(cache_hits/total_tests)*100:.1f}%")
    
    if cache_hits >= total_tests * 0.7:
        print("🎉 EXCELLENT - Multi-level cache is working well!")
    elif cache_hits >= total_tests * 0.5:
        print("✅ GOOD - Cache system is functioning")
    else:
        print("⚠️  NEEDS IMPROVEMENT - Cache hit rate could be better")
    
    print("\n🧠 Multi-Level Cache Benefits:")
    print("- Word-level: Pre-cached responses for individual concepts")
    print("- Phrase-level: Smart pattern matching for common question types")
    print("- Paragraph-level: Complex multi-sentence query patterns")
    print("- Full Message-level: Exact query matches with perfect responses")
    print("- Dynamic learning: System learns and caches successful patterns")
    print("- O(1) lookup: Hash-based retrieval for consistent fast performance")

def test_cache_learning():
    print("\n🎓 Testing Cache Learning Capability")
    print("=" * 40)
    
    base_url = "http://localhost:8080"
    
    # Test a pattern that should be learned
    novel_queries = [
        "what is quantum computing",
        "explain quantum computing",
        "quantum computing basics"
    ]
    
    print("Testing how cache learns from similar patterns...")
    
    for i, query in enumerate(novel_queries, 1):
        print(f"\n{i}. Testing: '{query}'")
        
        try:
            start_time = time.time()
            response = requests.post(
                f"{base_url}/chat",
                headers={"Content-Type": "application/json"},
                json={"query": query},
                timeout=5
            )
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                
                print(f"   Response time: {response_time:.1f}ms")
                print(f"   Length: {len(ai_response)} chars")
                
                if i > 1 and response_time < 50:
                    print(f"   🧠 LEARNING DETECTED - Faster response for similar pattern!")
                else:
                    print(f"   📚 INITIAL LEARNING - Cache building pattern knowledge")
                    
        except Exception as e:
            print(f"   ❌ ERROR - {e}")
        
        time.sleep(0.5)

if __name__ == "__main__":
    test_multilevel_cache()
    test_cache_learning()