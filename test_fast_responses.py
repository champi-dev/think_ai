#!/usr/bin/env python3
"""
⚡ Test Think AI Response Times - Ensure <1s responses
"""

import requests
import time
import json
from typing import List, Dict

def test_response_times(base_url: str = "http://localhost:9999"):
    """Test various queries and measure response times"""
    
    print("⚡ Testing Think AI Response Times...")
    print("=" * 60)
    
    test_queries = [
        "hello",
        "what is quantum mechanics",
        "explain artificial intelligence",
        "how are you",
        "what can you do",
        "tell me about consciousness",
        "what is machine learning",
        "explain climate change",
        "what is the meaning of life",
        "how does the brain work"
    ]
    
    results = []
    total_time = 0
    
    # Test each query
    for query in test_queries:
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{base_url}/api/chat",
                json={
                    "message": query,
                    "session_id": "test_speed"
                },
                timeout=5
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                result = {
                    "query": query,
                    "response_time": response_time,
                    "status": "success",
                    "tokens_used": data.get("tokens_used", 0),
                    "compacted": data.get("compacted", False),
                    "response_preview": data.get("response", "")[:100] + "..."
                }
                
                # Display result
                if response_time < 1.0:
                    print(f"✅ {query[:30]:30} | {response_time:.3f}s | FAST!")
                else:
                    print(f"⚠️  {query[:30]:30} | {response_time:.3f}s | SLOW")
                
                total_time += response_time
            else:
                result = {
                    "query": query,
                    "response_time": response_time,
                    "status": f"error_{response.status_code}",
                    "error": response.text
                }
                print(f"❌ {query[:30]:30} | Error: {response.status_code}")
                
        except Exception as e:
            result = {
                "query": query,
                "response_time": -1,
                "status": "exception",
                "error": str(e)
            }
            print(f"❌ {query[:30]:30} | Exception: {str(e)}")
        
        results.append(result)
    
    # Summary
    successful = [r for r in results if r["status"] == "success"]
    fast_responses = [r for r in successful if r["response_time"] < 1.0]
    
    print("\n" + "=" * 60)
    print("📊 PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"Total queries tested: {len(test_queries)}")
    print(f"Successful responses: {len(successful)}")
    print(f"Fast responses (<1s): {len(fast_responses)}")
    
    if successful:
        avg_time = sum(r["response_time"] for r in successful) / len(successful)
        min_time = min(r["response_time"] for r in successful)
        max_time = max(r["response_time"] for r in successful)
        
        print(f"\nResponse Times:")
        print(f"  Average: {avg_time:.3f}s")
        print(f"  Minimum: {min_time:.3f}s")
        print(f"  Maximum: {max_time:.3f}s")
        
        if avg_time < 1.0:
            print(f"\n✨ EXCELLENT! Average response time is {avg_time:.3f}s (<1s target)")
        else:
            print(f"\n⚠️  Need optimization - Average response time is {avg_time:.3f}s (>1s)")
    
    # Save results
    with open("response_time_test_results.json", "w") as f:
        json.dump({
            "test_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "results": results,
            "summary": {
                "total_queries": len(test_queries),
                "successful": len(successful),
                "fast_responses": len(fast_responses),
                "average_time": avg_time if successful else 0
            }
        }, f, indent=2)
    
    return results

if __name__ == "__main__":
    # First check if server is running
    try:
        response = requests.get("http://localhost:9999/health", timeout=2)
        if response.status_code == 200:
            print("✅ Think AI server is running on port 9999")
            test_response_times()
        else:
            print("❌ Server returned status:", response.status_code)
    except:
        print("❌ Cannot connect to Think AI server on port 9999")
        print("Make sure the server is running first!")