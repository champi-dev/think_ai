#!/usr/bin/env python3

import subprocess
import time
import requests

def test_step3_caching():
    print("🔍 STEP 3: Testing Core Caching Functionality")
    print("=" * 55)
    
    server_process = None
    try:
        # Start server
        print("🚀 Starting server...")
        server_process = subprocess.Popen(
            ['./target/release/think-ai', 'server'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        time.sleep(3)
        
        # Test core caching functionality
        print("\n🧪 Testing MultiLevelCache functionality...")
        
        test_cases = [
            {
                "name": "Full Message Cache - Hello",
                "query": "hello",
                "should_hit": "MultiLevelCache",
                "description": "Should hit full message cache"
            },
            {
                "name": "Full Message Cache - Love", 
                "query": "what is love",
                "should_hit": "MultiLevelCache",
                "description": "Should hit full message cache"
            },
            {
                "name": "Word-Level Analysis",
                "query": "what is emotion",
                "should_hit": "MultiLevelCache", 
                "description": "Should trigger word/phrase analysis"
            },
            {
                "name": "Novel Query",
                "query": "what is quantum mechanics",
                "should_hit": "MultiLevelCache",
                "description": "Should generate dynamic response"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. {test_case['name']}")
            print(f"   Query: '{test_case['query']}'")
            print(f"   Expected: {test_case['description']}")
            
            try:
                response = requests.post(
                    "http://localhost:8080/chat",
                    headers={"Content-Type": "application/json"},
                    json={"query": test_case["query"]},
                    timeout=10
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data.get("response", "")
                    print(f"   📥 Response: {ai_response[:100]}{'...' if len(ai_response) > 100 else ''}")
                    
                    # Analyze response to see if it came from cache
                    if "SimpleCacheComponent" in ai_response:
                        print("   🎯 RESULT: SimpleCacheComponent used (basic cache working)")
                    elif len(ai_response) > 150 and ("?" in ai_response or "!" in ai_response):
                        print("   🎯 RESULT: Likely MultiLevelCache generated response")
                    elif "That's a really thoughtful question" in ai_response:
                        print("   ❌ RESULT: Generic fallback - cache not working")
                    else:
                        print("   ❓ RESULT: Unknown response source")
                        
                else:
                    print(f"   ❌ HTTP Error: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Request Error: {e}")
        
        # Check server logs
        print("\n📋 Analyzing server logs...")
        try:
            server_process.terminate()
            stdout, stderr = server_process.communicate(timeout=5)
            
            # Look for MultiLevelCache activity
            multilevel_lines = [line for line in stdout.split('\n') if 'MultiLevel' in line]
            cache_hit_lines = [line for line in stdout.split('\n') if 'CACHE HIT' in line]
            
            print(f"   Found {len(multilevel_lines)} MultiLevelCache log lines")
            print(f"   Found {len(cache_hit_lines)} cache hit lines")
            
            if multilevel_lines:
                print("   📋 MultiLevelCache activity detected:")
                for line in multilevel_lines[-5:]:  # Last 5 lines
                    print(f"      {line}")
            else:
                print("   ❌ No MultiLevelCache activity detected")
                
        except Exception as e:
            print(f"   ❌ Log analysis error: {e}")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        if server_process and server_process.poll() is None:
            server_process.terminate()
            time.sleep(1)
    
    print("\n📊 STEP 3 RESULTS:")
    print("✅ If you see 'MultiLevelCache generated response' - core caching works")
    print("❌ If you see 'Generic fallback' - cache needs debugging")
    print("📋 Check MultiLevelCache logs above for detailed analysis")

if __name__ == "__main__":
    test_step3_caching()