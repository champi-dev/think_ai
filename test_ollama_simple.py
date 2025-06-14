#!/usr/bin/env python3
"""Simple test to verify Ollama is working."""

import asyncio
import httpx
import time


async def test_ollama():
    """Test if Ollama is responding."""
    print("🧪 Testing Ollama Connection...")
    print("="*60)
    
    # Check if Ollama is running
    print("\n1️⃣ Checking if Ollama service is running...")
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:11434/api/tags")
            models = response.json().get("models", [])
            print(f"✅ Ollama is running with {len(models)} models")
            
            # Check for phi3:mini
            has_phi3 = any(m.get("name") == "phi3:mini" for m in models)
            if has_phi3:
                print("✅ phi3:mini is available")
            else:
                print("❌ phi3:mini not found! Run: ollama pull phi3:mini")
                return
    except:
        print("❌ Ollama not running! Start with: ollama serve")
        return
    
    # Test generation
    print("\n2️⃣ Testing Phi-3.5 Mini generation...")
    print("Sending test prompt...")
    
    start = time.time()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "phi3:mini",
                    "prompt": "What is love in one sentence?",
                    "stream": False,
                    "options": {
                        "num_predict": 50,
                        "temperature": 0.7
                    }
                }
            )
            
            elapsed = time.time() - start
            result = response.json()
            
            if result.get("response"):
                print(f"\n✅ Success! Response in {elapsed:.1f}s:")
                print(f"Response: {result['response']}")
                print(f"Tokens: {result.get('eval_count', 'unknown')}")
            else:
                print(f"❌ Empty response: {result}")
                
    except httpx.TimeoutException:
        print(f"❌ Timeout after {time.time() - start:.1f}s")
        print("\nPossible issues:")
        print("1. First generation takes longer (model loading)")
        print("2. Try: ollama run phi3:mini 'test' (to pre-load)")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*60)
    print("If this test fails, the infinite consciousness chat won't work properly.")
    print("Make sure Ollama is running and phi3:mini is downloaded.")


if __name__ == "__main__":
    asyncio.run(test_ollama())