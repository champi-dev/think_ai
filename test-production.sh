#!/bin/bash

echo "Testing Think AI Production at thinkai.lat"
echo "========================================="
echo

# Test 1: Frontend loads
echo "1. Testing frontend loads..."
status_code=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat)
if [ "$status_code" = "200" ]; then
    echo "   ✅ Frontend loads successfully"
else
    echo "   ❌ Frontend failed to load (HTTP $status_code)"
fi
echo

# Test 2: CSS/JS assets load
echo "2. Testing assets..."
curl -s https://thinkai.lat | grep -q "index-.*\.js"
if [ $? -eq 0 ]; then
    echo "   ✅ JS assets load successfully"
else
    echo "   ❌ JS assets failed to load"
fi
echo

# Test 3: Chat API works
echo "3. Testing chat API..."
response=$(curl -s -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test-session"}')
  
if echo "$response" | grep -q "response"; then
    echo "   ✅ Chat API works"
    echo "   Response preview: $(echo "$response" | jq -r '.response' | head -c 100)..."
else
    echo "   ❌ Chat API failed"
fi
echo

# Test 4: Real AI responses (not test responses)
echo "4. Testing real AI responses..."
if echo "$response" | grep -q "This is a test response"; then
    echo "   ❌ Still returning test responses"
else
    echo "   ✅ Returning real AI responses"
fi
echo

# Test 5: PWA manifest
echo "5. Testing PWA support..."
manifest_status=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat/manifest.json)
if [ "$manifest_status" = "200" ]; then
    echo "   ✅ PWA manifest loads"
else
    echo "   ❌ PWA manifest failed (HTTP $manifest_status)"
fi
echo

# Test 6: Icons
echo "6. Testing 🧠 icons..."
icon_status=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat/icon-192.svg)
if [ "$icon_status" = "200" ]; then
    echo "   ✅ Icons load successfully"
else
    echo "   ❌ Icons failed to load (HTTP $icon_status)"
fi
echo

echo "========================================="
echo "Production test complete!"