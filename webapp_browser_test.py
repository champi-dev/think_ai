#\!/usr/bin/env python3
import urllib.request
import json
import re

print("\n🌐 Simulating browser interaction with Think AI webapp")
print("=" * 60)

BASE_URL = "http://69.197.178.37:7777"

# Step 1: Load the webapp
print("\n1. Loading webapp...")
with urllib.request.urlopen(f"{BASE_URL}/") as resp:
    html = resp.read().decode()
    print("✅ Webapp loaded successfully")

# Step 2: Extract API endpoints from HTML
print("\n2. Checking API endpoints in webapp...")
health_endpoints = re.findall(r"fetch\(['\"]([^'\"]*health[^'\"]*)['\"]", html)
chat_endpoints = re.findall(r"fetch\(['\"]([^'\"]*chat[^'\"]*)['\"]", html)

print(f"   Health endpoints found: {health_endpoints[:3]}")
print(f"   Chat endpoints found: {chat_endpoints[:3]}")

# Step 3: Simulate webapp health check
print("\n3. Simulating webapp health check...")
try:
    with urllib.request.urlopen(f"{BASE_URL}/health") as resp:
        if resp.status == 200:
            print("✅ Health check successful")
        else:
            print(f"❌ Health check returned status {resp.status}")
except Exception as e:
    print(f"❌ Health check failed: {e}")

# Step 4: Simulate user sending a message
print("\n4. Simulating user interaction...")
print("   User types: 'Hello'")
print("   Webapp sends request to /api/chat...")

try:
    # Check what the webapp expects
    request_body_pattern = re.search(r'requestBody\s*=\s*{([^}]+)}', html)
    if request_body_pattern:
        print(f"   Request body format: {{{request_body_pattern.group(1)}}}")
    
    # Send the request
    data = json.dumps({"message": "Hello"}).encode('utf-8')
    req = urllib.request.Request(
        f"{BASE_URL}/api/chat",
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        if result.get("response"):
            print("✅ Got AI response successfully")
            print(f"   AI says: {result['response']}")
        else:
            print("❌ No response in result")
            print(f"   Result: {result}")
except Exception as e:
    print(f"❌ Chat request failed: {e}")

# Step 5: Check for any console errors in the HTML
print("\n5. Checking for potential issues...")
console_errors = re.findall(r'console\.error\([^)]+\)', html)
if console_errors:
    print(f"   Found {len(console_errors)} console.error calls in code")
    for err in console_errors[:3]:
        print(f"   - {err[:80]}...")

print("\n" + "=" * 60)
print("✅ Browser simulation complete\!")
print("\nThe webapp should work correctly. If stuck at 'Thinking...', check:")
print("1. Browser console for errors (F12)")
print("2. Network tab to see if requests are being made")
print("3. CORS headers are properly set")
