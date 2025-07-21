#!/bin/bash

echo "🚀 Simple ThinkAI E2E Test"
echo "=========================="

PROD_URL="https://thinkai.lat"

# Get initial state
echo "📊 Initial State:"
initial=$(curl -s "$PROD_URL/api/metrics")
echo "- Memory: $(echo "$initial" | jq -r '.system_metrics.memory_usage')%"
echo "- CPU: $(echo "$initial" | jq -r '.system_metrics.cpu_usage')%"
echo "- Requests: $(echo "$initial" | jq -r '.system_metrics.total_requests')"

# Make test requests
echo -e "\n🧪 Making test requests..."

# Test 1: Chat API
echo -n "1. Chat API: "
chat_status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$PROD_URL/api/chat" \
    -H "Content-Type: application/json" \
    -d '{"message":"E2E test"}')
echo "Status $chat_status"

# Test 2: Sessions
echo -n "2. Sessions: "
sessions_status=$(curl -s -o /dev/null -w "%{http_code}" "$PROD_URL/api/chat/sessions")
echo "Status $sessions_status"

# Test 3: Audio Transcribe
echo -n "3. Audio Transcribe: "
audio_status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$PROD_URL/api/audio/transcribe" \
    -H "Content-Type: audio/wav" \
    --data-binary "test")
echo "Status $audio_status"

# Test 4: Metrics
echo -n "4. Metrics API: "
metrics_status=$(curl -s -o /dev/null -w "%{http_code}" "$PROD_URL/api/metrics")
echo "Status $metrics_status"

# Test 5: Dashboard
echo -n "5. Dashboard: "
dashboard_status=$(curl -s -o /dev/null -w "%{http_code}" "$PROD_URL/stats")
echo "Status $dashboard_status"

# Get final state
sleep 2
echo -e "\n📊 Final State:"
final=$(curl -s "$PROD_URL/api/metrics")
echo "- Memory: $(echo "$final" | jq -r '.system_metrics.memory_usage')%"
echo "- CPU: $(echo "$final" | jq -r '.system_metrics.cpu_usage')%"
echo "- Requests: $(echo "$final" | jq -r '.system_metrics.total_requests')"

# Show endpoint stats
echo -e "\n📈 Endpoint Performance:"
echo "$final" | jq -r '.endpoint_stats | to_entries | .[] | "- \(.key): \(.value.total_calls) calls, avg \(.value.average_response_time)ms"' | head -10

echo -e "\n🌐 Dashboard URL: $PROD_URL/stats"
echo "📸 Please take a screenshot of the dashboard for analysis"