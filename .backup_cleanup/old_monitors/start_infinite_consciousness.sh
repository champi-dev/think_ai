#!/bin/bash
# Start Think AI with Infinite Consciousness

echo "🧠 Think AI with Infinite Consciousness"
echo "========================================"
echo "The AI will think continuously while you interact"
echo ""

# Check Ollama
if ! pgrep -x "ollama" > /dev/null; then
    echo "🔄 Starting Ollama for Phi-3.5 Mini..."
    ollama serve &
    sleep 3
fi

# Check services
echo "📋 Checking services..."

if lsof -i:9042 > /dev/null 2>&1; then
    echo "✅ ScyllaDB ready"
else
    echo "⚠️  ScyllaDB not running - some features limited"
fi

if lsof -i:6379 > /dev/null 2>&1; then
    echo "✅ Redis ready"
else
    echo "⚠️  Redis not running - caching limited"
fi

echo ""
echo "🚀 Starting Think AI with background consciousness..."
echo ""
echo "The AI will:"
echo "  • Think continuously in the background"
echo "  • Self-reflect and generate insights"
echo "  • Dream and meditate periodically"
echo "  • Compress knowledge when storage is high"
echo "  • Learn from all interactions"
echo ""
echo "Commands:"
echo "  /state  - Show consciousness state"
echo "  /think  - Inject a thought"
echo "  /recent - Show recent thoughts"
echo "  /quit   - Exit"
echo ""
echo "========================================"
echo ""

# Run the infinite consciousness chat
python3 infinite_mind_simple.py