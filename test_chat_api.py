#!/usr/bin/env python3
"""Test Think AI chat API functionality."""

import requests
import json
import time


def test_think_ai_chat():
    """Test the Think AI chat API endpoints."""
    print("🧪 TESTING THINK AI CHAT FUNCTIONALITY")
    print("=" * 60)

    base_url = "http://localhost:8080"

    # Test 1: Health check
    print("\n1️⃣ Testing health endpoint...")
    try:
        resp = requests.get(f"{base_url}/health")
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {json.dumps(resp.json(), indent=2)}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 2: Root endpoint
    print("\n2️⃣ Testing root endpoint...")
    try:
        resp = requests.get(f"{base_url}/")
        print(f"   Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            print(f"   Mode: {data.get('mode', 'N/A')}")
    except Exception as e:
        print(f"   Error: {e}")

    # Test 3: Generate endpoint (main chat functionality)
    print("\n3️⃣ Testing chat generation...")
    test_prompts = [
        "Hello Think AI! What are your capabilities?",
        "Can you help me code in Python?",
        "What makes you different from other AI systems?",
        "Tell me about your O(1) performance optimization",
    ]

    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n   Test {i}: {prompt}")
        try:
            payload = {"prompt": prompt, "max_length": 200, "temperature": 0.7, "colombian_mode": True}

            start_time = time.time()
            resp = requests.post(f"{base_url}/api/v1/generate", json=payload)
            response_time = (time.time() - start_time) * 1000

            if resp.status_code == 200:
                data = resp.json()
                print(f"   ✅ Success! Response time: {response_time:.2f}ms")
                print(f"   Generated text: {data.get('generated_text', 'N/A')[:150]}...")
                if "performance_metrics" in data:
                    metrics = data["performance_metrics"]
                    print(f"   Performance: {metrics}")
            else:
                print(f"   ❌ Failed with status {resp.status_code}")
                print(f"   Error: {resp.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")

        time.sleep(0.5)  # Small delay between requests

    print("\n" + "=" * 60)
    print("✨ CHAT API TESTING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    test_think_ai_chat()
