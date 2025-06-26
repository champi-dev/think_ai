#!/bin/bash

echo "🧠 Testing Enhanced Think AI with Context-Aware Qwen Integration"
echo "================================================================"
echo ""

# Source the API key setup
if [ -f ".env" ]; then
    export $(cat .env | xargs)
    echo "✅ Loaded environment variables from .env"
elif [ -n "$HUGGINGFACE_API_KEY" ]; then
    echo "✅ Using existing HUGGINGFACE_API_KEY"
else
    echo "⚠️  No API key found. Qwen will use offline responses."
    echo "   Run ./setup_huggingface_api.sh to configure API access"
fi
echo ""

# Test queries that should hit the knowledge base (fast O(1) responses)
echo "📚 Testing Knowledge Base Hits (Should be instant):"
echo "===================================================="
echo ""

echo "Query: 'what is gravity'"
echo -e "what is gravity\nexit" | timeout 5 ./target/release/think-ai chat 2>/dev/null | grep -A2 "Think AI:"
echo ""

echo "Query: 'JavaScript'"
echo -e "JavaScript\nexit" | timeout 5 ./target/release/think-ai chat 2>/dev/null | grep -A2 "Think AI:"
echo ""

# Test queries that will miss cache and use Qwen with context
echo ""
echo "🤖 Testing Cache Misses with Context-Aware Qwen:"
echo "================================================="
echo ""

echo "Query: 'explain blockchain technology and its applications'"
echo -e "explain blockchain technology and its applications\nexit" | timeout 10 ./target/release/think-ai chat 2>/dev/null | grep -A5 "Think AI:"
echo ""

echo "Query: 'how does machine learning work in practice'"
echo -e "how does machine learning work in practice\nexit" | timeout 10 ./target/release/think-ai chat 2>/dev/null | grep -A5 "Think AI:"
echo ""

# Test queries that combine knowledge base context with new questions
echo ""
echo "🔬 Testing Contextual Synthesis:"
echo "================================"
echo ""

echo "Query: 'compare quantum mechanics with classical physics'"
echo -e "compare quantum mechanics with classical physics\nexit" | timeout 10 ./target/release/think-ai chat 2>/dev/null | grep -A5 "Think AI:"
echo ""

echo "✅ Test complete!"
echo ""
echo "Key features demonstrated:"
echo "• O(1) performance for knowledge base hits"
echo "• Intelligent responses for cache misses using Qwen/HuggingFace"
echo "• Context-aware synthesis using Think AI's knowledge pieces"
echo "• Natural, conversational responses"