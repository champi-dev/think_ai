#!/bin/bash

echo "🔄 Testing Streaming API Fix"
echo "============================"
echo ""

PROD_URL="https://thinkai.lat"
SESSION_ID="streaming-test-$(date +%s)"

# Test 1: Test streaming endpoint directly
echo "1. Testing streaming endpoint with correct parameters..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $PROD_URL/api/chat/stream \
    -H "Content-Type: application/json" \
    -d "{\"message\":\"Hello world\",\"session_id\":\"$SESSION_ID\",\"model\":\"qwen\"}")

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Streaming endpoint: SUCCESS (HTTP $HTTP_CODE)"
    echo "Response preview: $(echo "$BODY" | head -50)..."
else
    echo "❌ Streaming endpoint: FAILED (HTTP $HTTP_CODE)"
    echo "Response: $BODY"
fi

echo ""

# Test 2: Test regular chat endpoint (for comparison)
echo "2. Testing regular chat endpoint..."
RESPONSE2=$(curl -s -w "\n%{http_code}" -X POST $PROD_URL/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\":\"Hello world\",\"session_id\":\"$SESSION_ID\"}")

HTTP_CODE2=$(echo "$RESPONSE2" | tail -1)
BODY2=$(echo "$RESPONSE2" | head -n -1)

if [ "$HTTP_CODE2" = "200" ]; then
    echo "✅ Regular chat endpoint: SUCCESS (HTTP $HTTP_CODE2)"
else
    echo "❌ Regular chat endpoint: FAILED (HTTP $HTTP_CODE2)"
fi

echo ""

# Test 3: Browser test instructions
echo "🌐 Browser Test Instructions:"
echo "1. Open https://thinkai.lat"
echo "2. Open browser console (F12)"
echo "3. Type any message and send"
echo "4. Check console - should NOT see '422 error' anymore"
echo "5. Should see streaming response appear progressively"

echo ""
echo "📊 Summary:"
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Streaming API is now working correctly!"
    echo "The 422 error has been fixed by using 'message' instead of 'query'"
else
    echo "⚠️  Streaming API still has issues"
fi