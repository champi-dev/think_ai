#!/bin/bash

echo "=== Full System Integration Test ==="
echo "===================================="

# Test 1: Direct Ollama/Qwen
echo -e "\n1. Testing Ollama/Qwen directly..."
DIRECT_RESPONSE=$(curl -s http://localhost:11434/api/generate \
  -d '{
    "model": "qwen2.5:3b",
    "prompt": "What is the capital of France? Give a short answer.",
    "stream": false
  }' | jq -r '.response' 2>/dev/null)
echo "Direct Qwen: $DIRECT_RESPONSE"

# Test 2: Local stable-server API
echo -e "\n2. Testing local stable-server API..."
LOCAL_RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}' | jq -r '.response' 2>/dev/null)
echo "Local API: $LOCAL_RESPONSE"

# Test 3: Production through ngrok
echo -e "\n3. Testing production via ngrok..."
PROD_RESPONSE=$(curl -s -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}' | jq -r '.response' 2>/dev/null)
echo "Production: $PROD_RESPONSE"

# Test 4: Check services
echo -e "\n4. Service Status:"
echo "Ollama: $(systemctl is-active ollama.service)"
echo "Stable Server: $(ps aux | grep stable-server-streaming | grep -v grep | wc -l)"
echo "Ngrok: $(ps aux | grep ngrok | grep -v grep | wc -l)"

echo -e "\n=== End of Test ==="