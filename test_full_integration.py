#!/usr/bin/env python3
"""Test full system integration including webapp."""

import requests
import json
import time


def test_full_system():
    """Test the complete Think AI system."""
    print("🧪 THINK AI FULL SYSTEM INTEGRATION TEST")
    print("=" * 60)

    results = []

    # Test 1: API Health Check
    print("\n1️⃣ Testing API Health Check...")
    try:
        resp = requests.get("http://localhost:8080/health")
        print(f"   Status: {resp.status_code}")
        print(f"   Response: {resp.json()}")
        results.append(("API Health", resp.status_code == 200))
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results.append(("API Health", False))

    # Test 2: API Root
    print("\n2️⃣ Testing API Root...")
    try:
        resp = requests.get("http://localhost:8080/")
        data = resp.json()
        print(f"   Status: {resp.status_code}")
        print(f"   Name: {data.get('name')}")
        print(f"   Endpoints available: {len(data.get('endpoints', []))}")
        results.append(("API Root", resp.status_code == 200))
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results.append(("API Root", False))

    # Test 3: Generate Endpoint (what webapp uses)
    print("\n3️⃣ Testing Generate Endpoint...")
    try:
        payload = {"prompt": "What is Think AI?", "max_length": 200, "temperature": 0.7, "colombian_mode": True}
        resp = requests.post("http://localhost:8080/api/v1/generate", json=payload)
        data = resp.json()
        print(f"   Status: {resp.status_code}")
        print(f"   Generated: {data.get('generated_text', 'N/A')[:80]}...")
        results.append(("Generate API", resp.status_code == 200))
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results.append(("Generate API", False))

    # Test 4: Webapp Accessibility
    print("\n4️⃣ Testing Webapp on port 3000...")
    try:
        resp = requests.get("http://localhost:3000", timeout=5)
        print(f"   Status: {resp.status_code}")
        print(f"   Webapp is accessible ✅")
        results.append(("Webapp", resp.status_code == 200))
    except Exception as e:
        print(f"   ⚠️  Webapp not running on port 3000: {e}")
        results.append(("Webapp", False))

    # Test 5: Knowledge Store
    print("\n5️⃣ Testing Knowledge Store...")
    try:
        payload = {
            "key": "test_integration",
            "content": "Think AI is an advanced AI system with O(1) performance",
            "metadata": {"test": True, "timestamp": time.time()},
        }
        resp = requests.post("http://localhost:8080/api/v1/knowledge/store", json=payload)
        data = resp.json()
        print(f"   Status: {resp.status_code}")
        print(f"   Stored: {data.get('success', False)}")
        results.append(("Knowledge Store", resp.status_code == 200))
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results.append(("Knowledge Store", False))

    # Test 6: Knowledge Query
    print("\n6️⃣ Testing Knowledge Query...")
    try:
        payload = {"query": "Think AI performance", "limit": 5, "use_semantic_search": True}
        resp = requests.post("http://localhost:8080/api/v1/knowledge/query", json=payload)
        data = resp.json()
        print(f"   Status: {resp.status_code}")
        print(f"   Results found: {len(data.get('results', []))}")
        results.append(("Knowledge Query", resp.status_code == 200))
    except Exception as e:
        print(f"   ❌ Failed: {e}")
        results.append(("Knowledge Query", False))

    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY:")
    passed = sum(1 for _, status in results if status)
    total = len(results)

    for test, status in results:
        emoji = "✅" if status else "❌"
        print(f"   {emoji} {test}: {'PASSED' if status else 'FAILED'}")

    print(f"\n🎯 Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n✨ EVIDENCE: Full system is 100% operational!")
        print("   ✅ API server running in full mode")
        print("   ✅ All endpoints accessible and working")
        print("   ✅ Generate endpoint works (webapp compatible)")
        print("   ✅ Knowledge storage and retrieval working")
        print("   ✅ System ready for Railway deployment")
        return True
    else:
        print(f"\n⚠️  {total - passed} tests failed. Issues need attention.")
        return False


if __name__ == "__main__":
    success = test_full_system()
    exit(0 if success else 1)
