#!/bin/bash

echo "=== Ollama Health Check ==="
echo "=========================="

# Test 1: Check if Ollama is running
echo -e "\n1. Checking Ollama process..."
if pgrep -f "ollama serve" > /dev/null; then
    echo "✓ Ollama is running"
else
    echo "✗ Ollama is not running"
fi

# Test 2: API health check
echo -e "\n2. Testing Ollama API..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama API is responding"
else
    echo "✗ Ollama API is not responding"
fi

# Test 3: Check available models
echo -e "\n3. Available models:"
curl -s http://localhost:11434/api/tags | jq -r '.models[].name' 2>/dev/null || echo "Failed to get models"

# Test 4: Test Qwen model
echo -e "\n4. Testing Qwen model..."
RESPONSE=$(curl -s http://localhost:11434/api/generate \
  -d '{
    "model": "qwen2.5:3b",
    "prompt": "What is 2+2?",
    "stream": false
  }' | jq -r '.response' 2>/dev/null)

if [ -n "$RESPONSE" ]; then
    echo "✓ Qwen responded: $RESPONSE"
else
    echo "✗ Qwen test failed"
fi

# Test 5: Check service status
echo -e "\n5. Systemd service status:"
systemctl is-active ollama.service

echo -e "\n=== End of Health Check ==="