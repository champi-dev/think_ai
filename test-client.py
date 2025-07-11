#!/usr/bin/env python3
"""Think AI Test Client - Test from local machine"""

import requests
import json
import sys
import time
from typing import Optional

class ThinkAIClient:
    def __init__(self, base_url: str = "http://localhost:7777"):
        self.base_url = base_url.rstrip('/')
        
    def health_check(self) -> bool:
        """Check if server is healthy"""
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=5)
            return resp.status_code == 200
        except:
            return False
    
    def chat(self, message: str) -> Optional[str]:
        """Send chat message"""
        try:
            resp = requests.post(
                f"{self.base_url}/api/chat",
                json={"message": message},
                timeout=10
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")
            else:
                print(f"Error: {resp.status_code} - {resp.text}")
                return None
        except Exception as e:
            print(f"Connection error: {e}")
            return None
    
    def benchmark(self, iterations: int = 10):
        """Run performance benchmark"""
        print(f"Running {iterations} requests...")
        times = []
        
        for i in range(iterations):
            start = time.time()
            self.chat(f"Test message {i}")
            times.append(time.time() - start)
        
        avg_time = sum(times) / len(times)
        print(f"Average response time: {avg_time*1000:.2f}ms")
        print(f"Min: {min(times)*1000:.2f}ms, Max: {max(times)*1000:.2f}ms")

def main():
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    else:
        base_url = "http://localhost:7777"
    
    client = ThinkAIClient(base_url)
    
    print(f"Testing Think AI at: {base_url}")
    
    # Health check
    if client.health_check():
        print("✓ Server is healthy")
    else:
        print("✗ Server is not responding")
        return
    
    # Interactive mode
    print("\nEntering interactive mode (type 'exit' to quit, 'bench' to benchmark)")
    
    while True:
        try:
            message = input("\nYou: ").strip()
            
            if message.lower() == 'exit':
                break
            elif message.lower() == 'bench':
                client.benchmark()
                continue
            
            response = client.chat(message)
            if response:
                print(f"AI: {response}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
