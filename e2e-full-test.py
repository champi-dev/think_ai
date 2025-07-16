#!/usr/bin/env python3
import requests
import json
import time
import asyncio
import websockets
from datetime import datetime

BASE_URL = "https://thinkai.lat"
API_BASE = f"{BASE_URL}/api"


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def add_pass(self, test_name):
        self.passed += 1
        print(f"✓ {test_name}")

    def add_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"✗ {test_name}: {error}")

    def summary(self):
        total = self.passed + self.failed
        success_rate = (self.passed / total * 100) if total > 0 else 0
        print(f"\n{'='*50}")
        print(f"Test Results: {self.passed}/{total} passed ({success_rate:.1f}%)")
        if self.errors:
            print("\nFailed tests:")
            for test, error in self.errors:
                print(f"  - {test}: {error}")
        return success_rate == 100


results = TestResults()

print("Starting comprehensive E2E tests for thinkai.lat...\n")

# Test 1: Basic page load
try:
    resp = requests.get(BASE_URL, timeout=10)
    if resp.status_code == 200 and '<div id="root">' in resp.text:
        results.add_pass("Page loads successfully")
    else:
        results.add_fail("Page load", f"Status {resp.status_code}")
except Exception as e:
    results.add_fail("Page load", str(e))

# Test 2: Static assets
try:
    page = requests.get(BASE_URL).text
    # Extract CSS and JS files
    import re

    css_match = re.search(r'href="/assets/(index-[a-z0-9]+\.css)"', page)
    js_match = re.search(r'src="/assets/(index-[a-z0-9]+\.js)"', page)

    if css_match:
        css_url = f"{BASE_URL}/assets/{css_match.group(1)}"
        css_resp = requests.get(css_url)
        if css_resp.status_code == 200 and len(css_resp.text) > 1000:
            results.add_pass("CSS loaded successfully")
        else:
            results.add_fail("CSS load", f"Size: {len(css_resp.text)}")
    else:
        results.add_fail("CSS load", "CSS file not found in HTML")

    if js_match:
        js_url = f"{BASE_URL}/assets/{js_match.group(1)}"
        js_resp = requests.get(js_url)
        if js_resp.status_code == 200 and "React" in js_resp.text:
            results.add_pass("JavaScript loaded successfully")
        else:
            results.add_fail("JS load", "React not found in JS")
    else:
        results.add_fail("JS load", "JS file not found in HTML")
except Exception as e:
    results.add_fail("Static assets", str(e))

# Test 3: API Health
try:
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if resp.status_code == 200 and resp.text.strip() == "OK":
        results.add_pass("Health endpoint working")
    else:
        results.add_fail("Health endpoint", f"Response: {resp.text}")
except Exception as e:
    results.add_fail("Health endpoint", str(e))

# Test 4: Chat API
try:
    chat_data = {
        "message": "Hello, this is a test message",
        "session_id": "test-session-123",
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(
        f"{API_BASE}/chat", json=chat_data, headers=headers, timeout=10
    )
    if resp.status_code == 200:
        data = resp.json()
        if "response" in data and "session_id" in data:
            results.add_pass("Chat API working")
        else:
            results.add_fail("Chat API", f"Missing fields: {data}")
    else:
        results.add_fail("Chat API", f"Status {resp.status_code}: {resp.text}")
except Exception as e:
    results.add_fail("Chat API", str(e))

# Test 5: SSE streaming
try:
    print("\nTesting SSE streaming...")
    # Using requests with stream=True for SSE
    sse_data = {"message": "Test SSE streaming", "session_id": "test-sse-123"}
    resp = requests.post(
        f"{API_BASE}/chat/stream",
        json=sse_data,
        headers={"Accept": "text/event-stream"},
        stream=True,
        timeout=5,
    )
    if resp.status_code == 200:
        # Read first few chunks
        chunks_received = 0
        for line in resp.iter_lines(decode_unicode=True):
            if line:
                chunks_received += 1
                if chunks_received >= 3:  # Just check we get some data
                    break
        if chunks_received > 0:
            results.add_pass("SSE streaming working")
        else:
            results.add_fail("SSE streaming", "No data received")
    else:
        results.add_fail("SSE streaming", f"Status {resp.status_code}")
except Exception as e:
    results.add_fail("SSE streaming", str(e))

# Test 6: Knowledge API endpoints
try:
    resp = requests.get(f"{API_BASE}/knowledge/stats", timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        if "total_knowledge_items" in data:
            results.add_pass("Knowledge stats API working")
        else:
            results.add_fail("Knowledge stats", "Missing expected fields")
    else:
        results.add_fail("Knowledge stats", f"Status {resp.status_code}")
except Exception as e:
    results.add_fail("Knowledge stats", str(e))

# Test 7: Search API
try:
    search_params = {"q": "test", "limit": 5}
    resp = requests.get(f"{API_BASE}/search", params=search_params, timeout=5)
    if resp.status_code == 200:
        data = resp.json()
        if "results" in data and "total" in data:
            results.add_pass("Search API working")
        else:
            results.add_fail("Search API", "Missing expected fields")
    else:
        results.add_fail("Search API", f"Status {resp.status_code}")
except Exception as e:
    results.add_fail("Search API", str(e))

# Test 8: CORS headers
try:
    resp = requests.options(
        f"{API_BASE}/chat",
        headers={
            "Origin": "https://thinkai.lat",
            "Access-Control-Request-Method": "POST",
        },
    )
    cors_headers = resp.headers.get("Access-Control-Allow-Origin")
    if cors_headers:
        results.add_pass("CORS headers present")
    else:
        results.add_fail("CORS", "No Access-Control-Allow-Origin header")
except Exception as e:
    results.add_fail("CORS", str(e))

# Test 9: Mode switching (Code mode)
try:
    code_data = {
        "message": "Write a hello world in Python",
        "session_id": "test-code-mode",
        "mode": "code",
    }
    resp = requests.post(
        f"{API_BASE}/chat", json=code_data, headers=headers, timeout=10
    )
    if resp.status_code == 200:
        results.add_pass("Code mode API working")
    else:
        results.add_fail("Code mode", f"Status {resp.status_code}")
except Exception as e:
    results.add_fail("Code mode", str(e))


# Test 10: WebSocket connection
async def test_websocket():
    try:
        ws_url = BASE_URL.replace("https://", "wss://") + "/ws"
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps({"type": "ping"}))
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            results.add_pass("WebSocket connection working")
    except Exception as e:
        results.add_fail("WebSocket", str(e))


# Run WebSocket test
try:
    asyncio.run(test_websocket())
except:
    results.add_fail("WebSocket", "Could not test WebSocket")

# Summary
success = results.summary()
if not success:
    print("\nIssues detected! Need to fix the failing components.")
else:
    print("\nAll tests passed! 100% functionality achieved.")
