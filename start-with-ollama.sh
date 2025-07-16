#!/bin/bash

# Start Ollama in the background
echo "🚀 Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to start..."
for i in {1..30}; do
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        echo "✅ Ollama is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Ollama failed to start"
        exit 1
    fi
    sleep 1
done

# Check if Qwen model exists, pull if not
echo "🔍 Checking for Qwen 2.5 1.5B model..."
if ! ollama list | grep -q "qwen2.5:1.5b"; then
    echo "📥 Pulling Qwen 2.5 1.5B model (this may take a few minutes)..."
    ollama pull qwen2.5:1.5b
else
    echo "✅ Qwen 2.5 1.5B model already available"
fi

# Start the main application
echo "🌐 Starting Think AI server with full Qwen integration..."
exec ./full-working-o1