#!/bin/bash

# Test script to demonstrate the response generation issue

echo "🧪 Testing Think AI Response Generation Issue"
echo "==========================================="
echo ""
echo "This test will demonstrate that responses are being selected from hardcoded"
echo "templates in the MultiLevelCache rather than using contextual knowledge."
echo ""

# Build the project first
echo "📦 Building project..."
cargo build --release 2>/dev/null

# Start the server in the background
echo "🚀 Starting server..."
./target/release/think-ai server &
SERVER_PID=$!

# Wait for server to start
sleep 2

echo ""
echo "🔍 Testing various queries to show non-contextual responses..."
echo ""

# Test 1: Basic knowledge question
echo "Test 1: Basic knowledge question"
echo "Query: \"What is quantum computing?\""
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is quantum computing?"}' | jq -r '.response'
echo ""

# Test 2: Another knowledge question
echo "Test 2: Another knowledge question"
echo "Query: \"What is photosynthesis?\""
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is photosynthesis?"}' | jq -r '.response'
echo ""

# Test 3: Word-based cache hit
echo "Test 3: Word-based cache hit (should return hardcoded response)"
echo "Query: \"love\""
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "love"}' | jq -r '.response'
echo ""

# Test 4: Full message cache hit
echo "Test 4: Full message cache hit (should return exact hardcoded response)"
echo "Query: \"what is love\""
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "what is love"}' | jq -r '.response'
echo ""

# Test 5: Knowledge base test
echo "Test 5: Testing if knowledge base has actual content"
echo "Checking knowledge stats..."
curl -s http://localhost:8080/stats | jq -r '.knowledge_stats'
echo ""

# Clean up
echo "🧹 Cleaning up..."
kill $SERVER_PID 2>/dev/null

echo ""
echo "📊 Analysis Summary:"
echo "==================="
echo "The issue is that the MultiLevelResponseComponent has:"
echo "1. Hardcoded template responses for common words/phrases"
echo "2. Very high priority (0.995) that overrides the KnowledgeBase component"
echo "3. No integration with actual knowledge from the knowledge base"
echo ""
echo "This causes Think AI to return generic, non-contextual responses"
echo "instead of using its knowledge base to provide informative answers."