#!/bin/bash

echo "Testing Gemini fallback mechanism..."

# First, check if Ollama is running
echo -e "\nChecking Ollama status:"
curl -s http://localhost:11434/api/tags | jq . 2>/dev/null || echo "Ollama not responding"

# Stop Ollama to test fallback
echo -e "\n\nStopping Ollama to test fallback..."
sudo systemctl stop ollama

sleep 2

# Test with Ollama stopped (should fallback to Gemini)
echo -e "\nTesting with Ollama stopped (expecting Gemini fallback):"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, are you using Gemini?"}' \
  -w "\nTotal time: %{time_total}s\n"

# Restart Ollama
echo -e "\n\nRestarting Ollama..."
sudo systemctl start ollama

sleep 5

# Test with Ollama running
echo -e "\nTesting with Ollama running (expecting Qwen):"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, are you using Qwen?"}' \
  -w "\nTotal time: %{time_total}s\n"

echo -e "\n\nFallback test completed!"