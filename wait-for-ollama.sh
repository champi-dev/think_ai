#!/bin/bash

# This script ensures Ollama is fully ready before serving requests

echo "🔍 Checking Ollama status..."

# Function to check if Ollama is ready with Qwen model
check_ollama() {
    # Check if Ollama is running
    if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        return 1
    fi
    
    # Check if Qwen model is available
    if ! curl -s http://localhost:11434/api/tags | grep -q "qwen2.5:1.5b"; then
        return 1
    fi
    
    # Try a test generation
    TEST=$(echo '{"model": "qwen2.5:1.5b", "prompt": "test", "stream": false}' | \
           curl -s -X POST http://localhost:11434/api/generate \
           -H "Content-Type: application/json" -d @- 2>/dev/null || echo "{}")
    
    if echo "$TEST" | grep -q "response"; then
        return 0
    else
        return 1
    fi
}

# Wait for Ollama to be ready
MAX_WAIT=300  # 5 minutes
WAITED=0

while [ $WAITED -lt $MAX_WAIT ]; do
    if check_ollama; then
        echo "✅ Ollama is ready with Qwen model!"
        exit 0
    fi
    
    echo "⏳ Waiting for Ollama... ($WAITED/$MAX_WAIT seconds)"
    sleep 5
    WAITED=$((WAITED + 5))
done

echo "❌ Ollama failed to start within $MAX_WAIT seconds"
exit 1