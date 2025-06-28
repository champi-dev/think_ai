#!/bin/bash

echo "🧠 Think AI Conversation Flow Demo"
echo "=================================="
echo ""

echo "Testing the conversation flow that was previously broken:"
echo ""

echo "1. hello"
curl -s -X POST http://localhost:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "hello"}' | jq -r '.response'

echo ""
echo "2. what is love"
curl -s -X POST http://localhost:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "what is love"}' | jq -r '.response'

echo ""
echo "3. what is care (this was broken before)"
curl -s -X POST http://localhost:8080/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "what is care"}' | jq -r '.response'

echo ""
echo "=================================="
echo "✅ All responses should now be thoughtful and conversational!"
echo "✅ Notice how 'what is care' references the previous love discussion!"