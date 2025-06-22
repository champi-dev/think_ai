#!/usr/bin/env python3
"""Test script for Think AI v3.1.0"""

import asyncio
import httpx
import json

async def test_api():
    """Test various API endpoints."""
    base_url = "http://localhost:8082"
    
    async with httpx.AsyncClient() as client:
        # Test root endpoint
        print("Testing root endpoint...")
        try:
            resp = await client.get(f"{base_url}/")
            print(f"Root: {resp.status_code}")
            if resp.status_code == 200:
                print(json.dumps(resp.json(), indent=2))
        except Exception as e:
            print(f"Root failed: {e}")
        
        # Test health endpoint
        print("\nTesting health endpoint...")
        try:
            resp = await client.get(f"{base_url}/health")
            print(f"Health: {resp.status_code}")
            if resp.status_code == 200:
                print(json.dumps(resp.json(), indent=2))
        except Exception as e:
            print(f"Health failed: {e}")
        
        # Test generation endpoint
        print("\nTesting text generation...")
        try:
            data = {
                "prompt": "Hello Think AI! What is consciousness?",
                "max_tokens": 100,
                "temperature": 0.7
            }
            resp = await client.post(f"{base_url}/api/v1/generate", json=data)
            print(f"Generate: {resp.status_code}")
            if resp.status_code == 200:
                result = resp.json()
                print(f"Response: {result['response']}")
                print(f"Consciousness state: {result['consciousness']['state']}")
                print(f"Ethics score: {result['ethics']['score']}")
        except Exception as e:
            print(f"Generate failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_api())