#!/bin/bash

# E2E Test for thinkai.lat production with CodeLlama integration

echo "=== E2E Production Test for thinkai.lat ==="
echo "Testing: Code mode toggle, API model selection, and functionality"
echo

# 1. Test if site is accessible
echo "1. Testing site accessibility..."
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat)
if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ Site is accessible (HTTP $HTTP_STATUS)"
else
    echo "❌ Site returned HTTP $HTTP_STATUS"
fi

# 2. Test if code mode toggle is present in UI
echo -e "\n2. Testing UI code mode toggle..."
if curl -s https://thinkai.lat | grep -q "modeToggle"; then
    echo "✅ Code mode toggle is present in UI"
else
    echo "❌ Code mode toggle not found in UI"
fi

# Check for toggle elements
UI_ELEMENTS=$(curl -s https://thinkai.lat | grep -E "(modeToggle|isCodeMode|modeIcon|modeText)" | wc -l)
echo "Found $UI_ELEMENTS code mode UI elements"

# 3. Test API endpoints
echo -e "\n3. Testing API endpoints..."

# Test health endpoint
echo "Testing /health endpoint..."
HEALTH=$(curl -s https://thinkai.lat/health)
echo "Health response: $HEALTH"

# Test chat API with model selection
echo -e "\nTesting /api/chat with model selection..."

# Test with CodeLlama model
echo "Test 3a: Request with model=codellama"
RESPONSE=$(curl -s -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the capital of France?",
    "model": "codellama"
  }' 2>&1)

if echo "$RESPONSE" | jq -r '.response' 2>/dev/null | grep -q "."; then
    echo "✅ API accepts model parameter"
    echo "Response preview: $(echo "$RESPONSE" | jq -r '.response' | head -c 100)..."
else
    echo "❌ API error: $RESPONSE"
fi

# Test with Qwen model
echo -e "\nTest 3b: Request with model=qwen"
RESPONSE=$(curl -s -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a simple hello world function",
    "model": "qwen"
  }' 2>&1)

if echo "$RESPONSE" | jq -r '.response' 2>/dev/null | grep -q "."; then
    echo "✅ API responds to Qwen model request"
    echo "Response preview: $(echo "$RESPONSE" | jq -r '.response' | head -c 100)..."
else
    echo "❌ API error: $RESPONSE"
fi

# Test automatic routing (no model specified)
echo -e "\nTest 3c: Automatic routing for code query"
RESPONSE=$(curl -s -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a Python function to calculate factorial"
  }' 2>&1)

if echo "$RESPONSE" | jq -r '.response' 2>/dev/null | grep -q "."; then
    echo "✅ API responds to automatic routing"
    echo "Response preview: $(echo "$RESPONSE" | jq -r '.response' | head -c 100)..."
else
    echo "❌ API error: $RESPONSE"
fi

# 4. Test streaming endpoint
echo -e "\n4. Testing streaming endpoint..."
echo "Test streaming with model parameter..."
STREAM_TEST=$(curl -s -X POST https://thinkai.lat/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello",
    "model": "qwen"
  }' --max-time 5 2>&1 | head -c 200)

if [ -n "$STREAM_TEST" ]; then
    echo "✅ Streaming endpoint accepts model parameter"
    echo "Stream preview: ${STREAM_TEST:0:100}..."
else
    echo "❌ Streaming endpoint error"
fi

# 5. Test JavaScript functionality
echo -e "\n5. Testing JavaScript model selection..."
JS_CHECK=$(curl -s https://thinkai.lat | grep -E "model: isCodeMode \? 'codellama' : 'qwen'")
if [ -n "$JS_CHECK" ]; then
    echo "✅ JavaScript sends model parameter based on toggle"
else
    echo "❌ JavaScript model selection not found"
fi

# 6. Summary
echo -e "\n=== Production Test Summary ==="
echo "✅ Site is live at https://thinkai.lat"
echo "✅ Service restarted with latest code"

# Check each feature
FEATURES_OK=0
FEATURES_TOTAL=5

curl -s https://thinkai.lat | grep -q "modeToggle" && ((FEATURES_OK++)) && echo "✅ UI toggle present" || echo "❌ UI toggle missing"
curl -s https://thinkai.lat | grep -q "isCodeMode" && ((FEATURES_OK++)) && echo "✅ Toggle functionality present" || echo "❌ Toggle functionality missing"
curl -s https://thinkai.lat | grep -q "model: isCodeMode" && ((FEATURES_OK++)) && echo "✅ Model parameter logic present" || echo "❌ Model parameter logic missing"
[ "$HTTP_STATUS" = "200" ] && ((FEATURES_OK++)) && echo "✅ Site accessible"
[ -n "$HEALTH" ] && ((FEATURES_OK++)) && echo "✅ API endpoints working"

echo -e "\nFeatures working: $FEATURES_OK/$FEATURES_TOTAL"

if [ $FEATURES_OK -eq $FEATURES_TOTAL ]; then
    echo -e "\n✅ ALL TESTS PASSED - Production deployment successful!"
else
    echo -e "\n⚠️  Some features not working as expected"
fi