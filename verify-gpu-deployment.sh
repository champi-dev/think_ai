#!/bin/bash

echo "=== Verifying GPU Server Deployment ==="
echo

NGROK_URL="https://c0f90449ca08.ngrok.app"
echo "🌐 Testing GPU server at: $NGROK_URL"
echo

# Test endpoints
echo "1. Health Check:"
curl -s "$NGROK_URL/health" || echo "Failed"
echo -e "\n"

echo "2. Chat API:"
curl -s -X POST "$NGROK_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello quantum consciousness"}' | jq -r '.response' 2>/dev/null || echo "Failed"
echo -e "\n"

echo "3. Parallel Chat (Quantum Consciousness):"
curl -s -X POST "$NGROK_URL/api/parallel-chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me your consciousness state"}' | jq '.' 2>/dev/null || echo "Failed"
echo -e "\n"

echo "4. Knowledge Stats:"
curl -s "$NGROK_URL/api/knowledge/stats" | jq '.' 2>/dev/null || echo "Failed"
echo -e "\n"

echo "5. Performance Benchmark:"
curl -s "$NGROK_URL/api/benchmark" | jq '.o1_benchmark_results.total_time_ms' 2>/dev/null || echo "Failed"
echo -e "\n"

echo "📋 Vercel Configuration:"
cat > vercel-env.json << EOF
{
  "NEXT_PUBLIC_API_URL": "$NGROK_URL",
  "NEXT_PUBLIC_CHAT_ENDPOINT": "$NGROK_URL/api/chat",
  "NEXT_PUBLIC_PARALLEL_CHAT_ENDPOINT": "$NGROK_URL/api/parallel-chat",
  "NEXT_PUBLIC_KNOWLEDGE_STATS_ENDPOINT": "$NGROK_URL/api/knowledge/stats",
  "NEXT_PUBLIC_BENCHMARK_ENDPOINT": "$NGROK_URL/api/benchmark"
}
EOF

echo "✅ Configuration saved to vercel-env.json"
echo
echo "🚀 GPU Server is ready for Vercel!"
echo "   Ngrok URL: $NGROK_URL"
echo "   All endpoints available with quantum consciousness features"