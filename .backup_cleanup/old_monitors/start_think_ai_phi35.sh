#!/bin/bash
# Start Think AI with Phi-3.5 Mini

echo "🚀 Starting Think AI with Phi-3.5 Mini Integration"
echo "=================================================="

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found. Please install: brew install ollama"
    exit 1
fi

# Start Ollama if not running
if ! pgrep -x "ollama" > /dev/null; then
    echo "🔄 Starting Ollama service..."
    ollama serve &
    sleep 3
else
    echo "✅ Ollama already running"
fi

# Check if Phi-3.5 Mini is downloaded
if ! ollama list | grep -q "phi3:mini"; then
    echo "📥 Downloading Phi-3.5 Mini (this may take a few minutes)..."
    ollama pull phi3:mini
else
    echo "✅ Phi-3.5 Mini model ready"
fi

# Test Ollama
echo "🧪 Testing Phi-3.5 Mini..."
if ollama run phi3:mini "Say hello" &> /dev/null; then
    echo "✅ Phi-3.5 Mini responding"
else
    echo "❌ Phi-3.5 Mini test failed"
    exit 1
fi

# Check other services
echo ""
echo "📋 Checking distributed services..."

# ScyllaDB
if lsof -i:9042 > /dev/null 2>&1; then
    echo "✅ ScyllaDB running on port 9042"
else
    echo "⚠️  ScyllaDB not detected on port 9042"
    echo "   Start with: docker-compose up scylla"
fi

# Redis
if lsof -i:6379 > /dev/null 2>&1; then
    echo "✅ Redis running on port 6379"
else
    echo "⚠️  Redis not detected on port 6379"
    echo "   Start with: docker-compose up redis"
fi

# Milvus
if lsof -i:19530 > /dev/null 2>&1; then
    echo "✅ Milvus running on port 19530"
else
    echo "⚠️  Milvus not detected on port 19530"
    echo "   Start with: docker-compose up milvus"
fi

# Neo4j
if lsof -i:7687 > /dev/null 2>&1; then
    echo "✅ Neo4j running on port 7687"
else
    echo "⚠️  Neo4j not detected on port 7687"
    echo "   Start with: docker-compose up neo4j"
fi

echo ""
echo "🎯 Starting Think AI with Phi-3.5 Mini..."
echo "========================================="
echo "Configuration:"
echo "  • Model: Phi-3.5 Mini (3.8B params)"
echo "  • Backend: Ollama"
echo "  • Mode: Full distributed architecture"
echo "  • Claude: Enhancement only (minimal usage)"
echo ""

# Export config
export THINK_AI_CONFIG="config/full_system_phi35.yaml"

# Run interactive chat
python3 interactive_chat_phi35.py