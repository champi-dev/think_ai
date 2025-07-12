#!/bin/bash

echo "🧪 Testing Think AI Stable Server on port 7777"
echo "============================================"

# Test health endpoint
echo -e "\n1. Testing health endpoint:"
curl -s http://localhost:7777/health

# Test stats endpoint
echo -e "\n\n2. Testing stats endpoint:"
curl -s http://localhost:7777/stats | jq '.'

# Test chat endpoint
echo -e "\n\n3. Testing chat endpoint:"
curl -s -X POST http://localhost:7777/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is O(1) performance?"}' | jq '.'

echo -e "\n\n✅ All tests completed!"