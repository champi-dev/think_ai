#!/usr/bin/env python3

import subprocess
import time
import requests
import threading
import queue

def capture_server_logs():
    """Capture server logs in real time"""
    process = subprocess.Popen(
        ['./target/release/think-ai', 'server'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # Wait for server to start
    time.sleep(3)
    return process

def test_with_logs():
    print("🧪 Testing Multi-Level Cache with Server Log Capture")
    print("=" * 60)
    
    # Start server and capture logs
    print("🚀 Starting server...")
    server_process = capture_server_logs()
    
    try:
        # Test query
        test_query = "what is emotion"
        print(f"\n📤 Sending query: '{test_query}'")
        
        response = requests.post(
            "http://localhost:8080/chat",
            headers={"Content-Type": "application/json"},
            json={"query": test_query},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            ai_response = data.get("response", "")
            print(f"📥 Response: {ai_response}")
            
            # Check server logs
            print("\n📋 Server logs (last few lines):")
            # Try to read some output
            try:
                output, errors = server_process.communicate(timeout=1)
                if output:
                    print("STDOUT:", output[-500:])  # Last 500 chars
                if errors:
                    print("STDERR:", errors[-500:])  # Last 500 chars
            except subprocess.TimeoutExpired:
                # Process still running, that's okay
                pass
                
        else:
            print(f"❌ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        # Cleanup
        print("\n🧹 Cleaning up...")
        server_process.terminate()
        time.sleep(1)
        
    print("\n🔍 Analysis:")
    print("If you don't see logs like:")
    print("- '🧠 MultiLevel Cache: Processing query'")
    print("- '🔍 Component scoring for query'") 
    print("- '🎯 USING COMPONENT: MultiLevelCache'")
    print("Then the component is not being used!")

if __name__ == "__main__":
    test_with_logs()