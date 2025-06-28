#!/usr/bin/env python3

import subprocess
import time
import requests
import os
import signal

def test_step1_registration():
    print("🔍 STEP 1: Testing Component Registration")
    print("=" * 50)
    
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
        
        # Give server time to start
        time.sleep(3)
        
        # Test if server is responding
        print("🌐 Testing server connectivity...")
        try:
            health_response = requests.get("http://localhost:8080/health", timeout=2)
            print(f"✅ Server responding: {health_response.status_code}")
        except:
            print("❌ Server not responding")
            return
        
        # Test the simple cache component
        print("\n🧪 Testing SimpleCacheComponent...")
        test_queries = [
            "hello",  # Should hit exact cache
            "test",   # Should hit exact cache  
            "random", # Should get dynamic response
        ]
        
        for query in test_queries:
            print(f"\n📤 Testing: '{query}'")
            try:
                response = requests.post(
                    "http://localhost:8080/chat",
                    headers={"Content-Type": "application/json"},
                    json={"query": query},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    ai_response = data.get("response", "")
                    print(f"📥 Response: {ai_response}")
                    
                    # Check if response came from SimpleCacheComponent
                    if "SimpleCacheComponent" in ai_response:
                        print("✅ SUCCESS: SimpleCacheComponent is working!")
                    elif query == "hello" and "Hello from SimpleCacheComponent" in ai_response:
                        print("✅ SUCCESS: Exact cache hit!")
                    else:
                        print("❌ FAIL: Response didn't come from SimpleCacheComponent")
                        print("   This means component registration failed")
                else:
                    print(f"❌ HTTP Error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Request Error: {e}")
                
        # Try to read server logs
        print("\n📋 Checking server logs...")
        try:
            if server_process.poll() is None:  # Process still running
                server_process.terminate()
                stdout, stderr = server_process.communicate(timeout=5)
                
                if "SimpleCacheComponent: INITIALIZING" in stdout:
                    print("✅ FOUND: SimpleCacheComponent initialization log")
                else:
                    print("❌ MISSING: SimpleCacheComponent initialization log")
                
                if "SimpleCache: Checking if I can handle" in stdout:
                    print("✅ FOUND: Component scoring logs")
                else:
                    print("❌ MISSING: Component scoring logs")
                    
                if "SimpleCache: GENERATE called" in stdout:
                    print("✅ FOUND: Component generation logs")
                else:
                    print("❌ MISSING: Component generation logs")
                    
                # Show relevant log lines
                lines = stdout.split('\n')
                relevant_lines = [line for line in lines if 'SimpleCache' in line or 'Component' in line]
                if relevant_lines:
                    print("\n📋 Relevant log lines:")
                    for line in relevant_lines[-10:]:  # Last 10 relevant lines
                        print(f"   {line}")
                        
        except Exception as e:
            print(f"❌ Log reading error: {e}")
            
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        # Cleanup
        if server_process and server_process.poll() is None:
            print("\n🧹 Cleaning up server...")
            server_process.terminate()
            time.sleep(1)
    
    print("\n📊 STEP 1 RESULTS:")
    print("If you see 'SUCCESS: SimpleCacheComponent is working!' above,")
    print("then component registration is working correctly.")
    print("If not, there's a fundamental issue with component loading.")

if __name__ == "__main__":
    test_step1_registration()