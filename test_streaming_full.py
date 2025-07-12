#\!/usr/bin/env python3
import urllib.request
import json
import time

print("🧪 Testing Think AI Streaming Server at http://69.197.178.37:7777")
print("=" * 60)

# Test 1: Health check
print("\n1️⃣ Testing health endpoint...")
try:
    req = urllib.request.Request('http://69.197.178.37:7777/health')
    with urllib.request.urlopen(req) as resp:
        print(f"✅ Health: {resp.read().decode()}")
except Exception as e:
    print(f"❌ Health check failed: {e}")

# Test 2: Regular chat
print("\n2️⃣ Testing regular chat endpoint...")
try:
    data = json.dumps({"message": "What is 2+2?"}).encode()
    req = urllib.request.Request(
        'http://69.197.178.37:7777/api/chat',
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        print(f"✅ Response: {result.get('response', 'No response')[:100]}...")
except Exception as e:
    print(f"❌ Chat failed: {e}")

# Test 3: Streaming
print("\n3️⃣ Testing streaming endpoint...")
try:
    data = json.dumps({"message": "Count to 5"}).encode()
    req = urllib.request.Request(
        'http://69.197.178.37:7777/api/chat/stream',
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    
    print("📡 Streaming response:")
    with urllib.request.urlopen(req) as resp:
        # Check headers
        content_type = resp.headers.get('Content-Type', '')
        print(f"   Content-Type: {content_type}")
        
        if 'text/event-stream' in content_type:
            print("   ✅ SSE headers correct\!")
            
            # Read streaming response
            chunk_count = 0
            for line in resp:
                decoded = line.decode().strip()
                if decoded.startswith('data:'):
                    chunk_count += 1
                    print(f"   Chunk {chunk_count}: {decoded}")
                    if '[DONE]' in decoded:
                        break
                if chunk_count > 10:  # Limit output
                    print("   ... (truncated)")
                    break
        else:
            print(f"   ❌ Wrong content type: {content_type}")
            print(f"   Response: {resp.read().decode()[:200]}")
            
except Exception as e:
    print(f"❌ Streaming failed: {e}")

print("\n✅ Testing complete\!")
