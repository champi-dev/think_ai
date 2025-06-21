#!/usr/bin/env python3
"""Verify Railway deployment is working correctly."""

import requests
import sys
import time
from datetime import datetime


def check_deployment(base_url):
    """Check if the deployment is working correctly."""
    print(f"🔍 Verifying deployment at: {base_url}")
    print("=" * 50)

    results = []

    # Check root endpoint
    print("\n1. Checking root endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        data = response.json()
        if response.status_code == 200:
            print(f"   ✅ Root endpoint: OK")
            print(f"   - Version: {data.get('version', 'Unknown')}")
            print(f"   - Status: {data.get('status', 'Unknown')}")
            if "features" in data:
                print(f"   - Features enabled: {sum(1 for v in data['features'].values() if v)}")
            results.append(True)
        else:
            print(f"   ❌ Root endpoint: Failed (Status: {response.status_code})")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Root endpoint: Error - {e}")
        results.append(False)

    # Check health endpoint
    print("\n2. Checking health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        data = response.json()
        if response.status_code == 200 and data.get("status") == "healthy":
            print(f"   ✅ Health endpoint: OK")
            print(f"   - Service: {data.get('service', 'Unknown')}")
            if "memory_usage_mb" in data:
                print(f"   - Memory usage: {data['memory_usage_mb']} MB")
            results.append(True)
        else:
            print(f"   ❌ Health endpoint: Failed")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Health endpoint: Error - {e}")
        results.append(False)

    # Check if it's running full system or minimal
    print("\n3. Checking system mode...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        data = response.json()
        if "Full System" in data.get("name", "") or data.get("version") == "2.0.0":
            print(f"   ✅ Running FULL Think AI system")
            results.append(True)
        elif "Minimal" in data.get("name", ""):
            print(f"   ⚠️  Running in minimal mode (import issues)")
            results.append(False)
        else:
            print(f"   ❓ Unknown mode")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Mode check: Error - {e}")
        results.append(False)

    # Test chat endpoint
    print("\n4. Testing chat endpoint...")
    try:
        response = requests.post(f"{base_url}/api/v1/chat", json={"message": "Hello, Think AI!"}, timeout=10)
        if response.status_code == 200:
            print(f"   ✅ Chat endpoint: OK")
            data = response.json()
            print(f"   - Response received: {len(data.get('response', ''))} chars")
            results.append(True)
        else:
            print(f"   ❌ Chat endpoint: Failed (Status: {response.status_code})")
            results.append(False)
    except Exception as e:
        print(f"   ❌ Chat endpoint: Error - {e}")
        results.append(False)

    # Summary
    print("\n" + "=" * 50)
    success_rate = sum(results) / len(results) * 100
    print(f"📊 Summary: {sum(results)}/{len(results)} checks passed ({success_rate:.0f}%)")

    if success_rate == 100:
        print("🎉 Deployment is fully operational!")
        return True
    elif success_rate >= 50:
        print("⚠️  Deployment is partially working")
        return True
    else:
        print("❌ Deployment has critical issues")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        print("Usage: python verify_deployment.py <deployment-url>")
        print("Example: python verify_deployment.py https://your-app.railway.app")
        sys.exit(1)

    # Remove trailing slash
    url = url.rstrip("/")

    # Run verification
    success = check_deployment(url)
    sys.exit(0 if success else 1)
