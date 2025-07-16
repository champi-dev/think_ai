#!/bin/bash

echo "⏳ Waiting 2 minutes for deployment to complete..."
sleep 120

echo "🧪 Testing deployment..."
echo ""

# Test 1: Basic health
echo "1. Health check:"
curl -s "https://thinkai-production.up.railway.app/health"
echo -e "\n"

# Test 2: Simple chat
echo "2. Simple chat test:"
curl -s -X POST "https://thinkai-production.up.railway.app/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "What is 2+2?"}' | jq -r .response
echo ""

# Test 3: Check response time
echo "3. Response time test:"
time curl -s -X POST "https://thinkai-production.up.railway.app/chat" \
    -H "Content-Type: application/json" \
    -d '{"query": "hi"}' | jq -r .response

echo -e "\n✅ Tests complete!"