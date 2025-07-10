#!/bin/bash

echo "🔧 Verifying Think AI Qwen Integration Build"
echo "==========================================="

cd /home/administrator/think_ai

# Check if the code compiles
echo "Checking if the code compiles..."
if cargo check --package think-ai-full 2>&1 | grep -E "(error|cannot find|unresolved)" ; then
    echo "❌ Build verification failed!"
    exit 1
else
    echo "✅ Code compiles successfully!"
fi

echo ""
echo "Next steps:"
echo "1. Ensure Ollama is running: ollama serve"
echo "2. Ensure Qwen model is installed: ollama pull qwen2.5:1.5b"
echo "3. Run the test script: ./test-qwen-integration.sh"