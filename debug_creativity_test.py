#!/usr/bin/env python3

import subprocess
import time
import requests

def debug_creativity_cache_lookup():
    print("🔍 DEBUG: Tracing 'what is creativity' cache lookup")
    print("=" * 60)
    
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
        
        # Test the specific problematic query
        print(f"\n🧪 Testing: 'what is creativity'")
        
        try:
            response = requests.post(
                "http://localhost:8080/chat",
                headers={"Content-Type": "application/json"},
                json={"query": "what is creativity"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get("response", "")
                print(f"📥 Response: {ai_response}")
                
                if "food" in ai_response.lower() or "breakfast" in ai_response.lower():
                    print("❌ BROKEN: Still returning food-related response!")
                else:
                    print("✅ FIXED: No food references detected")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request Error: {e}")
        
        # Get detailed logs
        print("\n📋 Analyzing debug logs...")
        try:
            server_process.terminate()
            stdout, stderr = server_process.communicate(timeout=5)
            
            lines = stdout.split('\n')
            
            # Find the complete trace for this query including component selection
            debug_lines = []
            
            for line in lines:
                if any(keyword in line for keyword in [
                    "Component scoring for query: 'what is creativity'",
                    "DEBUG: Cache lookup for 'what is creativity'", 
                    "MultiLevel Cache: Processing query 'what is creativity'",
                    "CACHE HIT",
                    "USING COMPONENT",
                    "FINAL: Used components",
                    "MultiLevel RETURNING",
                    "MultiLevel",
                    "Conversational ->"
                ]):
                    debug_lines.append(line)
                elif "what is creativity" in line:
                    debug_lines.append(line)
            
            if debug_lines:
                print("🔍 Cache lookup trace:")
                for line in debug_lines:
                    print(f"   {line}")
            else:
                print("❌ No debug trace found - check if debug logging is working")
                
            # Look for any food-related responses in word cache
            food_lines = [line for line in lines if "food" in line.lower() or "breakfast" in line.lower()]
            if food_lines:
                print("\n⚠️  Food-related cache entries found:")
                for line in food_lines:
                    print(f"   {line}")
                    
        except Exception as e:
            print(f"❌ Log analysis error: {e}")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        if server_process and server_process.poll() is None:
            server_process.terminate()
            time.sleep(1)

if __name__ == "__main__":
    debug_creativity_cache_lookup()