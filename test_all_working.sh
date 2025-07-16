#!/bin/bash

echo "=========================================="
echo "Think AI - Complete System Test"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Testing Qwen (General AI) on Production${NC}"
echo "Query: What is the meaning of life?"
curl -s -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the meaning of life?",
    "model": "qwen",
    "session_id": "demo_qwen"
  }' | jq -r '.response'

echo ""
echo -e "${BLUE}2. Testing CodeLlama (Code AI) on Production${NC}"
echo "Query: Write a function to calculate fibonacci numbers"
curl -s -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Write a function to calculate fibonacci numbers",
    "model": "codellama",
    "session_id": "demo_codellama"
  }' | jq -r '.response' | head -30

echo ""
echo -e "${BLUE}3. Testing Auto Model Selection${NC}"
echo "Query: Explain how to optimize database queries"
curl -s -X POST https://thinkai.lat/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explain how to optimize database queries",
    "session_id": "demo_auto"
  }' | jq -r '.response' | head -20

echo ""
echo -e "${GREEN}✅ All tests completed!${NC}"
echo "Production site: https://thinkai.lat"
echo ""