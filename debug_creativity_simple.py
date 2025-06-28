#!/usr/bin/env python3

import subprocess
import time
import requests

def test_creativity_only():
    print("🔍 DEBUG: Testing 'what is creativity' specifically")
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
        
        time.sleep(3)
        
        # Test the specific query
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
                print(f"📥 Full Response: '{ai_response}'")
                print(f"📏 Length: {len(ai_response)} characters")
                
                # Check for forbidden terms character by character
                forbidden_terms = ["food", "breakfast", "eat"]
                for term in forbidden_terms:
                    if term.lower() in ai_response.lower():
                        print(f"❌ Found forbidden term '{term}' in response")
                        # Find where it appears
                        start_idx = ai_response.lower().find(term.lower())
                        context = ai_response[max(0, start_idx-20):start_idx+len(term)+20]
                        print(f"   Context: '...{context}...'")
                    else:
                        print(f"✅ No '{term}' found")
                        
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request Error: {e}")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
    finally:
        if server_process and server_process.poll() is None:
            server_process.terminate()
            time.sleep(1)

if __name__ == "__main__":
    test_creativity_only()