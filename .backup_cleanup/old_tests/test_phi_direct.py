#!/usr/bin/env python3
"""Test Phi-3.5 Mini directly."""

import requests
import time


def test_phi(prompt, max_tokens=50):
    """Test Phi-3.5 with a prompt."""
    print(f"\n📤 Testing: '{prompt}'")
    print("-" * 50)
    
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7,
                    "top_k": 40,
                    "top_p": 0.9
                }
            },
            timeout=15
        )
        
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            result = response.json()
            text = result.get("response", "")
            print(f"✅ Response ({elapsed:.1f}s): {text}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"⏱️  Timeout after {time.time() - start_time:.1f}s")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🧪 Testing Phi-3.5 Mini Direct Calls")
    print("=" * 50)
    
    # Test queries
    test_phi("Hello", max_tokens=20)
    test_phi("What is love?", max_tokens=50)
    test_phi("Question: What is 2+2?\nAnswer:", max_tokens=10)
    
    print("\n✅ Test complete!")