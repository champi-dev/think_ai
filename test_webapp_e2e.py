import urllib.request
import json
import time

print("🧪 E2E Test for Think AI Webapp")
print("=" * 50)

BASE_URL = "http://69.197.178.37:7777"

# Test 1: Load webapp
print("\n1. Testing webapp loading...")
try:
    with urllib.request.urlopen(f"{BASE_URL}/") as resp:
        html = resp.read().decode()
        if "Think AI" in html and "minimal_3d" in resp.headers.get('Content-Type', ''):
            print("✅ Webapp loads successfully")
        else:
            print("❌ Webapp content issue")
except Exception as e:
    print(f"❌ Failed to load webapp: {e}")

# Test 2: Health check
print("\n2. Testing health endpoint...")
try:
    with urllib.request.urlopen(f"{BASE_URL}/health") as resp:
        if resp.read().decode().strip() == "OK - Stable Server Running":
            print("✅ Health check passed")
        else:
            print("❌ Health check failed")
except Exception as e:
    print(f"❌ Health endpoint error: {e}")

# Test 3: Chat API
print("\n3. Testing chat functionality...")
test_messages = [
    "Hello",
    "What is physics?",
    "Explain quantum computing"
]

for msg in test_messages:
    print(f"\n   Testing message: '{msg}'")
    try:
        data = json.dumps({"message": msg}).encode('utf-8')
        req = urllib.request.Request(
            f"{BASE_URL}/api/chat",
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        
        start = time.time()
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode())
            elapsed = (time.time() - start) * 1000
            
            if result.get("response"):
                print(f"   ✅ Got response in {elapsed:.0f}ms")
                print(f"   Response preview: {result['response'][:100]}...")
            else:
                print("   ❌ No response received")
    except Exception as e:
        print(f"   ❌ Chat error: {e}")

# Test 4: Check streaming endpoint
print("\n4. Testing streaming endpoint fallback...")
try:
    data = json.dumps({"message": "test"}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/chat/stream",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    with urllib.request.urlopen(req) as resp:
        if resp.status == 200:
            print("✅ Streaming endpoint falls back correctly")
        else:
            print("❌ Streaming endpoint issue")
except Exception as e:
    print(f"❌ Streaming endpoint error: {e}")

print("\n" + "=" * 50)
print("🎉 E2E Test Complete\!")
