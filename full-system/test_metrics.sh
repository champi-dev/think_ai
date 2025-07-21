#!/bin/bash

echo "Testing ThinkAI Metrics Dashboard..."

# Check if server is running
if ! curl -s http://localhost:7777/health > /dev/null; then
    echo "Error: Server is not running on port 7777"
    echo "Please start the server first with: cargo run --package think-ai-full --bin think-ai-full"
    exit 1
fi

echo "✅ Server is running"

# Make some test requests to generate metrics
echo "Generating test metrics..."

# Test chat endpoint
curl -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: test-session-1" \
  -d '{"message": "Hello, ThinkAI!"}' &> /dev/null

# Test transcription endpoint (will fail but generate metrics)
curl -X POST http://localhost:7777/api/audio/transcribe \
  -H "Content-Type: audio/wav" \
  -H "X-Session-ID: test-session-2" \
  --data-binary "@/dev/null" &> /dev/null

# Test synthesis endpoint
curl -X POST http://localhost:7777/api/audio/synthesize \
  -H "Content-Type: application/json" \
  -H "X-Session-ID: test-session-3" \
  -d '{"text": "Hello world", "voice": "default"}' &> /dev/null

# Test WhatsApp webhook
curl -X POST http://localhost:7777/webhooks/whatsapp \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "Body=Test message&From=whatsapp:+1234567890&To=whatsapp:+0987654321&MessageSid=test123" &> /dev/null

echo "✅ Test requests sent"

# Check metrics endpoint
echo "Fetching metrics..."
METRICS=$(curl -s http://localhost:7777/api/metrics)

if [ -z "$METRICS" ]; then
    echo "Error: No metrics returned"
    exit 1
fi

# Check if metrics contain expected data
if echo "$METRICS" | grep -q "system_metrics"; then
    echo "✅ System metrics present"
else
    echo "❌ System metrics missing"
fi

if echo "$METRICS" | grep -q "endpoint_stats"; then
    echo "✅ Endpoint stats present"
else
    echo "❌ Endpoint stats missing"
fi

if echo "$METRICS" | grep -q "cpu_usage"; then
    echo "✅ CPU usage tracking working"
else
    echo "❌ CPU usage tracking not working"
fi

if echo "$METRICS" | grep -q "memory_usage"; then
    echo "✅ Memory usage tracking working"
else
    echo "❌ Memory usage tracking not working"
fi

# Display current metrics summary
echo -e "\n📊 Current Metrics Summary:"
echo "$METRICS" | jq -r '.system_metrics | "CPU: \(.cpu_usage)%, Memory: \(.memory_usage)%, Requests: \(.total_requests)"' 2>/dev/null || echo "Install jq for formatted output"

echo -e "\n🌐 Dashboard URL: http://localhost:7777/stats"
echo "Open this URL in your browser to see the live metrics dashboard"