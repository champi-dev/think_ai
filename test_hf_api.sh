#!/bin/bash

echo "Testing Hugging Face API directly..."
echo ""

# Load the API key from .env
source .env

echo "Using model: microsoft/Phi-3.5-mini-instruct"
echo ""

# Test the API with curl
curl -X POST \
  "https://api-inference.huggingface.co/models/microsoft/Phi-3.5-mini-instruct" \
  -H "Authorization: Bearer $HUGGINGFACE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "You are Think AI. User asks: hi\n\nProvide a direct answer:",
    "parameters": {
      "max_new_tokens": 100,
      "temperature": 0.7,
      "return_full_text": false
    }
  }' \
  --max-time 10

echo ""
echo ""
echo "Test complete!"