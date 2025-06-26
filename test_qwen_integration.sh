#!/bin/bash

# Test Think AI with Qwen integration

echo "🧠 Testing Think AI with Qwen Integration"
echo "========================================"
echo ""

# Test knowledge base hits
echo "1. Testing knowledge base queries (should be instant):"
echo "Query: 'what is the sun?'"
echo "what is the sun?" | ./target/release/think-ai chat 2>/dev/null | grep -A1 "Think AI:" | tail -2
echo ""

echo "Query: 'Gravity'"
echo "Gravity" | ./target/release/think-ai chat 2>/dev/null | grep -A1 "Think AI:" | tail -2
echo ""

# Test cache misses (should use Qwen)
echo "2. Testing cache misses (should use Qwen fallback):"
echo "Query: 'what is blockchain?'"
echo "what is blockchain?" | ./target/release/think-ai chat 2>/dev/null | grep -A1 "Think AI:" | tail -2
echo ""

echo "Query: 'how does cryptocurrency work?'"
echo "how does cryptocurrency work?" | ./target/release/think-ai chat 2>/dev/null | grep -A1 "Think AI:" | tail -2
echo ""

echo "✅ Test complete!"
echo ""
echo "To use Qwen API (instead of offline responses):"
echo "export QWEN_API_KEY=your_api_key"
echo "export QWEN_API_URL=https://api.qwen.ai/v1/chat/completions"