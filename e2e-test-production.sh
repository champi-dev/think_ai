#!/bin/bash

echo "=== E2E Production Test ==="
echo "Testing Think AI at https://thinkai.lat"
echo "=========================="

# Test 1: Check if site is accessible
echo -e "\n1. Testing site accessibility..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat)
if [ "$STATUS" = "200" ]; then
    echo "✓ Site is accessible (HTTP $STATUS)"
else
    echo "✗ Site returned HTTP $STATUS"
    exit 1
fi

# Test 2: Check if frontend has updated code
echo -e "\n2. Checking frontend code..."
curl -s https://thinkai.lat -o /tmp/prod-frontend.html
if grep -q "data\.chunk" /tmp/prod-frontend.html && grep -q "data\.done" /tmp/prod-frontend.html; then
    echo "✓ Frontend has updated JSON parsing code"
else
    echo "✗ Frontend is missing updated code"
fi

# Test 3: Test API streaming endpoint
echo -e "\n3. Testing API streaming endpoint..."
echo "Request: POST /api/chat/stream"
RESPONSE=$(curl -s -X POST https://thinkai.lat/api/chat/stream \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello", "session_id": "test123"}' \
    --max-time 10 2>&1)

if echo "$RESPONSE" | grep -q "data: {" && echo "$RESPONSE" | grep -q '"chunk"'; then
    echo "✓ API streaming endpoint is working"
    echo "Sample response:"
    echo "$RESPONSE" | head -5
else
    echo "✗ API streaming endpoint not working properly"
    echo "Response: $RESPONSE" | head -20
fi

# Test 4: Test regular chat endpoint
echo -e "\n4. Testing regular chat endpoint..."
echo "Request: POST /api/chat"
CHAT_RESPONSE=$(curl -s -X POST https://thinkai.lat/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "test", "session_id": "test123"}' \
    --max-time 10 2>&1)

if echo "$CHAT_RESPONSE" | grep -q "response"; then
    echo "✓ Chat endpoint is working"
else
    echo "✗ Chat endpoint not working"
    echo "Response: $CHAT_RESPONSE" | head -20
fi

# Test 5: Check services
echo -e "\n5. Checking services..."
if systemctl is-active --quiet think-ai.service; then
    echo "✓ think-ai.service is running"
else
    echo "✗ think-ai.service is not running"
fi

if pgrep -f "ngrok" > /dev/null; then
    echo "✓ ngrok is running"
else
    echo "✗ ngrok is not running"
fi

# Test 6: Check server binding
echo -e "\n6. Checking server binding..."
BIND_LOG=$(tail -5 /home/administrator/think_ai/webapp_server.log | grep "Server listening")
if echo "$BIND_LOG" | grep -q "0.0.0.0:8080"; then
    echo "✓ Server is binding to 0.0.0.0 (all interfaces)"
else
    echo "⚠ Server may be binding to localhost only"
    echo "$BIND_LOG"
fi

echo -e "\n=== Test Summary ==="
echo "Production URL: https://thinkai.lat"
echo "All core functionality should be working!"