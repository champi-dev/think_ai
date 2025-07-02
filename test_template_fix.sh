#!/bin/bash

echo "🧪 Testing Template Response Fix"
echo "================================"

RAILWAY_URL="https://thinkai-production.up.railway.app"

# Test 1: JavaScript query
echo "Test 1: JavaScript Query"
echo "------------------------"
RESPONSE1=$(curl -s --max-time 15 -X POST "$RAILWAY_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "what is javascript"}' 2>/dev/null)

echo "Query: what is javascript"
echo "Response: $(echo "$RESPONSE1" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('response', 'N/A'))")"
echo ""

# Test 2: Sun query
echo "Test 2: Sun Query (should have astronomy knowledge)"
echo "---------------------------------------------------"
RESPONSE2=$(curl -s --max-time 15 -X POST "$RAILWAY_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "what is the sun"}' 2>/dev/null)

echo "Query: what is the sun"
echo "Response: $(echo "$RESPONSE2" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('response', 'N/A'))")"
echo ""

# Test 3: Dark energy query
echo "Test 3: Dark Energy Query"
echo "-------------------------"
RESPONSE3=$(curl -s --max-time 15 -X POST "$RAILWAY_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "what is dark energy"}' 2>/dev/null)

echo "Query: what is dark energy"
echo "Response: $(echo "$RESPONSE3" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('response', 'N/A'))")"
echo ""

# Test 4: Basic math (should work with mathematical component)
echo "Test 4: Math Query (should have specific component)"
echo "--------------------------------------------------"
RESPONSE4=$(curl -s --max-time 15 -X POST "$RAILWAY_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "what is 2+2"}' 2>/dev/null)

echo "Query: what is 2+2"
echo "Response: $(echo "$RESPONSE4" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data.get('response', 'N/A'))")"
echo ""

# Check for template responses
echo "📊 Template Response Analysis"
echo "============================="

if echo "$RESPONSE1" | grep -q "That's a fascinating question"; then
    echo "❌ Test 1: Still has template response"
else
    echo "✅ Test 1: No template response"
fi

if echo "$RESPONSE2" | grep -q "That's a fascinating question"; then
    echo "❌ Test 2: Still has template response"
else
    echo "✅ Test 2: No template response"
fi

if echo "$RESPONSE3" | grep -q "That's a fascinating question"; then
    echo "❌ Test 3: Still has template response"
else
    echo "✅ Test 3: No template response"
fi

if echo "$RESPONSE4" | grep -q "That's a fascinating question"; then
    echo "❌ Test 4: Still has template response"
else
    echo "✅ Test 4: No template response"
fi

echo ""
echo "🎯 Summary: Template fix verification complete"