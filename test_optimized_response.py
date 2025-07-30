#!/usr/bin/env python3
"""Test script to verify sub-1s response times"""

import requests
import time
import json
import statistics

API_URL = "http://localhost:7777/api/chat"

# Test queries
test_queries = [
    "Hello",
    "What is quantum physics?",
    "Explain quantum physics like I'm 5",
    "How are you today?",
    "What can you help me with?",
    "ping",
    "Tell me about artificial intelligence",
    "What is 2+2?",
]

def test_response_time():
    print("🚀 Testing Think AI Response Times")
    print("=" * 50)
    
    response_times = []
    
    for query in test_queries:
        payload = {
            "message": query,
            "session_id": "test-session"
        }
        
        start_time = time.time()
        
        try:
            response = requests.post(API_URL, json=payload, timeout=5)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            response_times.append(response_time)
            
            if response.status_code == 200:
                data = response.json()
                status = "✅" if response_time < 1000 else "⚠️"
                print(f"{status} Query: '{query[:30]}...' - {response_time:.0f}ms")
                
                # Print first 100 chars of response
                response_text = data.get('response', '')[:100]
                print(f"   Response: {response_text}...")
            else:
                print(f"❌ Query: '{query}' - Failed with status {response.status_code}")
                
        except Exception as e:
            print(f"❌ Query: '{query}' - Error: {e}")
        
        print()
    
    # Calculate statistics
    if response_times:
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        median_time = statistics.median(response_times)
        
        print("\n📊 Performance Statistics:")
        print("=" * 50)
        print(f"Average response time: {avg_time:.0f}ms")
        print(f"Median response time: {median_time:.0f}ms")
        print(f"Fastest response: {min_time:.0f}ms")
        print(f"Slowest response: {max_time:.0f}ms")
        
        under_1s = sum(1 for t in response_times if t < 1000)
        print(f"\n🎯 Responses under 1s: {under_1s}/{len(response_times)} ({under_1s/len(response_times)*100:.0f}%)")
    
    # Check optimization metrics
    print("\n🔧 Checking Optimization Metrics...")
    try:
        metrics_response = requests.get("http://localhost:7777/api/optimization")
        if metrics_response.status_code == 200:
            metrics = metrics_response.json()
            print(json.dumps(metrics, indent=2))
    except Exception as e:
        print(f"Could not fetch optimization metrics: {e}")

if __name__ == "__main__":
    test_response_time()