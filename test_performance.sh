#!/bin/bash

# Performance test script for Think AI server optimizations

echo "🔧 Think AI Server Performance Test"
echo "==================================="

# Test greeting endpoint (should be very fast)
echo "🧪 Testing Greeting Performance (O(1) expected):"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}' \
  -s > /dev/null

echo "🧪 Testing Greeting Caching (second request):"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hello"}' \
  -s > /dev/null

# Test simple knowledge query
echo "🧪 Testing Simple Knowledge Query:"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is physics?"}' \
  --max-time 10 \
  -s > /dev/null

# Test same query for caching
echo "🧪 Testing Cache Hit for Knowledge Query:"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is physics?"}' \
  --max-time 5 \
  -s > /dev/null

# Test concurrent requests
echo "🧪 Testing Concurrent Performance (5 parallel greetings):"
time (
  for i in {1..5}; do
    curl -X POST http://localhost:8080/api/chat \
      -H "Content-Type: application/json" \
      -d '{"query": "hello"}' \
      -s > /dev/null &
  done
  wait
)

# Test API availability
echo "🧪 Testing API Health:"
curl -X GET http://localhost:8080/health -s

echo ""
echo "✅ Performance test completed!"
echo "📊 Expected improvements:"
echo "   - Greeting: ~1ms (down from ~10+ seconds)"
echo "   - Cache hits: <5ms"
echo "   - Simple queries: 5-10s with timeout protection"
echo "   - Concurrent requests: No blocking from write locks"