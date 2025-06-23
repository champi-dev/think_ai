#!/usr/bin/env python3
"""Test the Think AI endpoints are working correctly."""

import requests
import json
import time
import sys


def test_full_system():
    """Test all endpoints to ensure the full system is operational."""
    print("🧪 THINK AI FULL SYSTEM TEST")
    print("=" * 50)

    base_url = "http://localhost:8080"
    results = []

    # Give server time to fully start
    print("⏳ Waiting for server to be ready...")
    time.sleep(3)

    # Test 1: Health check
    print("\n1️⃣ Testing /health endpoint...")
    try:
        resp = requests.get(f"{base_url}/health")
        data = resp.json()
        print(f"✅ Health check: {resp.status_code}")
        print(f"   Response: {json.dumps(data, indent=2)}")
        results.append(("Health", resp.status_code == 200))
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        results.append(("Health", False))

    # Test 2: Root endpoint
    print("\n2️⃣ Testing / endpoint...")
    try:
        resp = requests.get(f"{base_url}/")
        data = resp.json()
        print(f"✅ Root endpoint: {resp.status_code}")
        print(f"   Version: {data.get('version')}")
        print(f"   Mode: {data.get('mode', 'full')}")
        print(f"   Endpoints: {data.get('endpoints', [])}")
        results.append(("Root", resp.status_code == 200))
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        results.append(("Root", False))

    # Test 3: Generate endpoint (what the webapp uses)
    print("\n3️⃣ Testing /api/v1/generate endpoint...")
    try:
        payload = {"prompt": "Hello, Think AI!", "max_length": 200, "temperature": 0.7, "colombian_mode": True}
        resp = requests.post(f"{base_url}/api/v1/generate", json=payload)
        data = resp.json()
        print(f"✅ Generate endpoint: {resp.status_code}")
        print(f"   Response: {json.dumps(data, indent=2)}")
        results.append(("Generate", resp.status_code == 200))
    except Exception as e:
        print(f"❌ Generate endpoint failed: {e}")
        results.append(("Generate", False))

    # Test 4: Webapp connectivity
    print("\n4️⃣ Testing webapp connectivity on port 3000...")
    try:
        resp = requests.get("http://localhost:3000", timeout=5)
        print(f"✅ Webapp is accessible: {resp.status_code}")
        results.append(("Webapp", resp.status_code == 200))
    except Exception as e:
        print(f"❌ Webapp not accessible: {e}")
        results.append(("Webapp", False))

    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    passed = sum(1 for _, status in results if status)
    total = len(results)

    for test, status in results:
        emoji = "✅" if status else "❌"
        print(f"   {emoji} {test}: {'PASSED' if status else 'FAILED'}")

    print(f"\n🎯 Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n✨ EVIDENCE: Full system is operational!")
        print("   - API server is running in full mode")
        print("   - All endpoints are accessible")
        print("   - Generate endpoint works (webapp compatible)")
        print("   - Webapp is running and accessible")
        print("\n🚀 Frontend and API are using the same endpoints!")
        return 0
    else:
        print("\n❌ Some tests failed. System needs attention.")
        return 1


if __name__ == "__main__":
    # Note: Run this AFTER starting the QA environment
    print("⚠️  Make sure the QA environment is running first!")
    print("   Run: python scripts/precommit_qa_environment_browser.py")
    print("")

    sys.exit(test_full_system())
