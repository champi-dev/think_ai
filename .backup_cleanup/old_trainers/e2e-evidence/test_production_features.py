import requests
import json
from datetime import datetime

# Test 1: Check if the page loads correctly
print("🔍 Testing https://thinkai.lat...")
response = requests.get("https://thinkai.lat")
print(f"✅ Page status: {response.status_code}")

# Test 2: Check HTML structure
html_content = response.text

# Check header - should NOT have web search/fact check in feature-toggles class
header_has_feature_toggles = (
    'class="feature-toggles"' in html_content
    and "<header" in html_content.split('class="feature-toggles"')[0]
)
print(
    f"❌ Feature toggles in header: {header_has_feature_toggles}"
    if header_has_feature_toggles
    else "✅ No feature toggles in header"
)

# Check input area - SHOULD have web search/fact check
input_has_web_search = 'id="webSearchBtn"' in html_content
input_has_fact_check = 'id="factCheckBtn"' in html_content
print(f"✅ Web Search in input area: {input_has_web_search}")
print(f"✅ Fact Check in input area: {input_has_fact_check}")

# Test 3: Check API endpoints
print("\n🔍 Testing API endpoints...")

# Test chat endpoint
chat_test = {
    "query": "Hello, this is a test",
    "sessionId": "test-session-123",
    "model": "qwen",
}

try:
    chat_response = requests.post(
        "https://thinkai.lat/api/chat",
        json=chat_test,
        headers={"Content-Type": "application/json"},
        timeout=10,
    )
    print(f"✅ Chat API status: {chat_response.status_code}")
    if chat_response.status_code == 200:
        print(
            f"✅ Chat response received: {len(chat_response.json().get('response', ''))} characters"
        )
except Exception as e:
    print(f"❌ Chat API error: {str(e)}")

# Test streaming with web search
print("\n🔍 Testing streaming with features...")
stream_test = {
    "query": "What is the weather today?",
    "sessionId": "test-session-456",
    "webSearchEnabled": True,
    "factCheckEnabled": True,
}

try:
    stream_response = requests.post(
        "https://thinkai.lat/api/stream",
        json=stream_test,
        headers={"Content-Type": "application/json"},
        stream=True,
        timeout=10,
    )
    print(f"✅ Stream API status: {stream_response.status_code}")

    # Read first few chunks
    chunks_received = 0
    for chunk in stream_response.iter_content(chunk_size=1024):
        if chunk:
            chunks_received += 1
            if chunks_received >= 3:  # Just read first 3 chunks
                break
    print(f"✅ Stream chunks received: {chunks_received}")
except Exception as e:
    print(f"❌ Stream API error: {str(e)}")

# Generate test report
report = {
    "test_time": datetime.now().isoformat(),
    "url": "https://thinkai.lat",
    "results": {
        "page_loads": response.status_code == 200,
        "header_clean": not header_has_feature_toggles,
        "web_search_in_input": input_has_web_search,
        "fact_check_in_input": input_has_fact_check,
        "chat_api_works": (
            chat_response.status_code == 200 if "chat_response" in locals() else False
        ),
        "stream_api_works": (
            stream_response.status_code == 200
            if "stream_response" in locals()
            else False
        ),
    },
    "test_status": (
        "PASSED"
        if all(
            [
                response.status_code == 200,
                not header_has_feature_toggles,
                input_has_web_search,
                input_has_fact_check,
            ]
        )
        else "FAILED"
    ),
}

with open("production_test_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"\n📊 Test Status: {report['test_status']}")
print(f"📄 Full report saved to: production_test_report.json")
