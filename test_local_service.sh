#\!/bin/bash
echo "🧪 Testing Local Think AI Service (localhost:7777)"
echo "================================================"

# Test 1: Basic Chat
echo -n "1. Basic Chat Test: "
RESPONSE=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, testing local service", "session_id": "local-test"}')

if echo "$RESPONSE" | grep -q "response"; then
  echo "✅ PASSED"
  echo "   Response time: $(echo "$RESPONSE" | jq -r .response_time_ms)ms"
else
  echo "❌ FAILED"
fi

# Test 2: Session Persistence
echo -n "2. Session Persistence: "
curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My name is LocalTestUser", "session_id": "local-persist"}' > /dev/null

sleep 1

RESPONSE2=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is my name?", "session_id": "local-persist"}')

if echo "$RESPONSE2" | grep -qi "LocalTestUser"; then
  echo "✅ PASSED"
else
  echo "❌ FAILED"
fi

# Test 3: Audio Endpoint
echo -n "3. Audio Service: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:7777/api/audio/synthesize \
  -H "Content-Type: application/json" \
  -d '{"text": "Testing audio service"}')

if [ "$STATUS" = "200" ]; then
  echo "✅ PASSED"
elif [ "$STATUS" = "404" ]; then
  echo "⚠️  Not Implemented"
else
  echo "❌ FAILED (Status: $STATUS)"
fi

# Test 4: Security
echo -n "4. Security (XSS): "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "<script>alert(\"xss\")</script>"}')

if [ "$STATUS" = "400" ]; then
  echo "✅ PASSED"
else
  echo "❌ FAILED (Status: $STATUS)"
fi

# Test 5: Performance
echo -n "5. Performance (<1s avg): "
TOTAL=0
for i in {1..5}; do
  START=$(date +%s.%N)
  curl -s -X POST http://localhost:7777/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Quick test $i\"}" > /dev/null
  END=$(date +%s.%N)
  TIME=$(echo "$END - $START" | bc)
  TOTAL=$(echo "$TOTAL + $TIME" | bc)
done
AVG=$(echo "scale=3; $TOTAL / 5" | bc)

if (( $(echo "$AVG < 1" | bc -l) )); then
  echo "✅ PASSED (${AVG}s avg)"
else
  echo "❌ FAILED (${AVG}s avg)"
fi

echo "================================================"
echo "Local Testing Complete\!"
