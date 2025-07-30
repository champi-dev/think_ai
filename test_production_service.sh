#\!/bin/bash
echo "🌐 Testing Production Think AI Service (thinkai.lat)"
echo "=================================================="

# Test 1: Health Check
echo -n "1. Health Check: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat/health)
if [ "$STATUS" = "200" ]; then
  echo "✅ PASSED"
else
  echo "❌ FAILED (Status: $STATUS)"
fi

# Test 2: Main Page
echo -n "2. Main Page: "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat/)
if [ "$STATUS" = "200" ]; then
  echo "✅ PASSED"
else
  echo "❌ FAILED (Status: $STATUS)"
fi

# Test 3: Basic Chat
echo -n "3. Chat API: "
RESPONSE=$(curl -s -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from production test", "session_id": "prod-test"}' 2>/dev/null)

if echo "$RESPONSE" | grep -q "response"; then
  echo "✅ PASSED"
  RESP_TIME=$(echo "$RESPONSE" | jq -r .response_time_ms 2>/dev/null || echo "N/A")
  echo "   Response time: ${RESP_TIME}ms"
else
  echo "❌ FAILED"
fi

# Test 4: HTTPS Security
echo -n "4. HTTPS Certificate: "
SSL_INFO=$(curl -s -I https://thinkai.lat 2>&1 | grep -i "SSL certificate" || echo "")
if curl -s -I https://thinkai.lat >/dev/null 2>&1; then
  echo "✅ Valid"
else
  echo "❌ Invalid"
fi

# Test 5: Response Time from Internet
echo -n "5. Internet Latency: "
START=$(date +%s.%N)
curl -s https://thinkai.lat/health > /dev/null
END=$(date +%s.%N)
LATENCY=$(echo "$END - $START" | bc)
echo "${LATENCY}s"

# Test 6: Cross-Origin Request
echo -n "6. CORS Support: "
HEADERS=$(curl -s -I -X OPTIONS https://thinkai.lat/api/chat \
  -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: POST" 2>/dev/null)

if echo "$HEADERS" | grep -qi "access-control-allow-origin"; then
  echo "✅ Enabled"
else
  echo "❌ Not configured"
fi

echo "=================================================="
echo "Production Testing Complete\!"
echo ""
echo "Service URL: https://thinkai.lat"
echo "Tunnel Status: $(curl -s http://localhost:4040/api/tunnels 2>/dev/null | jq -r '.tunnels[0].public_url' 2>/dev/null || echo 'Local API not available')"
