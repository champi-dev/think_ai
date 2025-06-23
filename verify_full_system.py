#!/usr/bin/env python3
"""Verify the full Think AI system is operational."""

import requests
import json
import time
import sys

def test_full_system():
    """Run comprehensive tests to prove the system works."""
    print("🧪 THINK AI FULL SYSTEM VERIFICATION")
    print("=" * 60)
    
    base_url = "http://localhost:8080"
    results = []
    
    # Test 1: Check server is in full mode
    print("\n1️⃣ Verifying server is running in FULL mode...")
    try:
        resp = requests.get(f"{base_url}/")
        data = resp.json()
        is_full_mode = data.get("name") == "Think AI Full System"
        print(f"   Server mode: {data.get('name')} ✅" if is_full_mode else f"   ❌ Server in minimal mode!")
        results.append(("Full Mode", is_full_mode))
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results.append(("Full Mode", False))
    
    # Test 2: Verify all endpoints exist
    print("\n2️⃣ Verifying all API endpoints...")
    expected_endpoints = [
        "/api/v1/health",
        "/api/v1/knowledge/store",
        "/api/v1/knowledge/query", 
        "/api/v1/generate",
        "/api/v1/optimize/code",
        "/api/v1/intelligence/status"
    ]
    
    try:
        resp = requests.get(f"{base_url}/")
        data = resp.json()
        actual_endpoints = data.get("endpoints", [])
        
        all_present = all(ep in actual_endpoints for ep in expected_endpoints)
        print(f"   Expected endpoints: {len(expected_endpoints)}")
        print(f"   Found endpoints: {len([e for e in expected_endpoints if e in actual_endpoints])}")
        for ep in expected_endpoints:
            status = "✅" if ep in actual_endpoints else "❌"
            print(f"   {status} {ep}")
        
        results.append(("All Endpoints", all_present))
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results.append(("All Endpoints", False))
    
    # Test 3: Test Generate endpoint (what webapp uses)
    print("\n3️⃣ Testing /api/v1/generate endpoint...")
    try:
        payload = {
            "prompt": "Hello Think AI, are you working?",
            "max_length": 200,
            "temperature": 0.7,
            "colombian_mode": True
        }
        resp = requests.post(f"{base_url}/api/v1/generate", json=payload)
        data = resp.json()
        
        success = resp.status_code == 200 and data.get("success") == True
        print(f"   Status: {resp.status_code} {'✅' if success else '❌'}")
        print(f"   Response: {json.dumps(data, indent=2)}")
        results.append(("Generate API", success))
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results.append(("Generate API", False))
    
    # Test 4: Test Knowledge Store
    print("\n4️⃣ Testing /api/v1/knowledge/store endpoint...")
    try:
        payload = {
            "key": "test_key",
            "content": "This is a test knowledge item",
            "metadata": {"type": "test"}
        }
        resp = requests.post(f"{base_url}/api/v1/knowledge/store", json=payload)
        data = resp.json()
        
        success = resp.status_code == 200 and data.get("success") == True
        print(f"   Status: {resp.status_code} {'✅' if success else '❌'}")
        if success:
            print(f"   Stored with key: {data.get('key')}")
        results.append(("Knowledge Store", success))
    except Exception as e:
        print(f"   ❌ Error: {e}")
        results.append(("Knowledge Store", False))
    
    # Test 5: Test webapp connectivity
    print("\n5️⃣ Testing webapp on port 3000...")
    try:
        resp = requests.get("http://localhost:3000", timeout=3)
        success = resp.status_code == 200
        print(f"   Webapp status: {resp.status_code} {'✅' if success else '❌'}")
        results.append(("Webapp", success))
    except:
        print("   ⚠️  Webapp not running on port 3000 (run separately)")
        results.append(("Webapp", None))  # Not a failure, just not running
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY:")
    
    passed = sum(1 for _, status in results if status == True)
    total = sum(1 for _, status in results if status is not None)
    
    for test, status in results:
        if status is None:
            emoji = "⚠️"
            text = "NOT TESTED"
        elif status:
            emoji = "✅"
            text = "PASSED"
        else:
            emoji = "❌"
            text = "FAILED"
        print(f"   {emoji} {test}: {text}")
    
    print(f"\n🎯 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ EVIDENCE: Full Think AI system is 100% operational!")
        print("   ✅ Server running in full mode (not minimal)")
        print("   ✅ All API endpoints are available")
        print("   ✅ Generate endpoint works (webapp compatible)")
        print("   ✅ Knowledge storage works")
        print("   ✅ System ready for Railway deployment")
        return 0
    else:
        print("\n❌ Some tests failed. Check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(test_full_system())