#!/bin/bash

# Test local API directly on port 8080
echo "=== Testing Local Think AI API ==="
echo

# Test basic chat endpoint
echo "1. Testing basic chat endpoint..."
curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "What is consciousness?"}' | jq .

echo
echo "2. Testing with session ID..."
curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Tell me more", "session_id": "test-123"}' | jq .

echo
echo "3. Testing code query (should trigger CodeLlama)..."
curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Write a Python function to sort a list"}' | jq .

echo
echo "4. Testing explicit model selection..."
curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Explain recursion", "model": "codellama"}' | jq .

echo
echo "5. Testing error handling..."
curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"message": ""}' | jq .

echo
echo "6. Testing SSE streaming endpoint..."
curl -s -X POST http://localhost:8080/api/stream/chat \
    -H "Content-Type: application/json" \
    -d '{"message": "Hello"}' \
    --max-time 2

echo
echo
echo "=== Tests Complete ==="