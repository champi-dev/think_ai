#\!/bin/bash
echo "🧪 Testing Think AI Chat API..."

# Test 1: Basic chat
echo -n "Test 1 - Basic chat: "
RESPONSE=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AI", "session_id": "test-001"}')

if echo "$RESPONSE" | grep -q "response"; then
  echo "✅ PASSED"
else
  echo "❌ FAILED"
fi

# Test 2: Session persistence
echo -n "Test 2 - Session persistence: "
curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My name is Bob", "session_id": "test-002"}' > /dev/null

RESPONSE2=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is my name?", "session_id": "test-002"}')

if echo "$RESPONSE2" | grep -qi "bob"; then
  echo "✅ PASSED"
else
  echo "❌ FAILED"
fi

# Test 3: Security - XSS protection
echo -n "Test 3 - XSS protection: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "<script>alert(\"xss\")</script>"}')

if [ "$STATUS" = "400" ]; then
  echo "✅ PASSED"
else
  echo "❌ FAILED (status: $STATUS)"
fi

# Test 4: Performance
echo -n "Test 4 - Performance (<2s): "
START=$(date +%s.%N)
curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quick test"}' > /dev/null
END=$(date +%s.%N)
DURATION=$(echo "$END - $START" | bc)

if (( $(echo "$DURATION < 2" | bc -l) )); then
  echo "✅ PASSED (${DURATION}s)"
else
  echo "❌ FAILED (${DURATION}s)"
fi

echo "🏁 Tests complete\!"
