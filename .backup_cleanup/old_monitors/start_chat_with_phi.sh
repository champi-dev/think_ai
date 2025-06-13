#!/bin/bash
# Start chat with Phi-3.5 as primary model

echo "🚀 Starting Think AI Chat with Phi-3.5 Mini..."
echo ""

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama not running. Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Check if Phi-3.5 is available
if ! ollama list | grep -q "phi3:mini"; then
    echo "📥 Loading Phi-3.5 Mini model..."
    ollama pull phi3:mini
fi

echo "✅ Phi-3.5 Mini ready!"
echo ""

# Warm up Phi-3.5
python ensure_phi_ready.py

echo ""
echo "Starting chat interface..."
echo "================================"
echo ""

# Run the chat
python chat_while_training.py