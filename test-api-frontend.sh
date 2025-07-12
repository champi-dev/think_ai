#!/bin/bash

echo "Testing API and Frontend Response Handling..."
echo "============================================="

# Test 1: Check if frontend is being served
echo -e "\n1. Testing if frontend is accessible..."
curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat > /tmp/status_code.txt
STATUS=$(cat /tmp/status_code.txt)
if [ "$STATUS" = "200" ]; then
    echo "✓ Frontend is accessible (HTTP $STATUS)"
else
    echo "✗ Frontend returned HTTP $STATUS"
fi

# Test 2: Test API streaming endpoint
echo -e "\n2. Testing API streaming endpoint..."
echo "Request: {\"message\": \"Hello\", \"session_id\": \"test123\"}"
echo "Response:"
curl -X POST https://thinkai.lat/api/chat/stream \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello", "session_id": "test123"}' \
    --no-buffer 2>/dev/null | head -20

# Test 3: Download and check frontend HTML
echo -e "\n3. Checking frontend JavaScript..."
curl -s https://thinkai.lat -o /tmp/frontend.html
if grep -q "data: {" /tmp/frontend.html && grep -q "JSON.parse" /tmp/frontend.html; then
    echo "✓ Frontend has updated JSON parsing code"
else
    echo "✗ Frontend might not have the updated code"
fi

# Test 4: Check for specific parsing logic
echo -e "\n4. Verifying response parsing logic..."
if grep -q "data.chunk !== undefined" /tmp/frontend.html; then
    echo "✓ Frontend checks for chunk property"
else
    echo "✗ Frontend missing chunk property check"
fi

if grep -q "data.done" /tmp/frontend.html; then
    echo "✓ Frontend checks for done property"
else
    echo "✗ Frontend missing done property check"
fi

echo -e "\nTest complete!"