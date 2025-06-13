#!/bin/bash
# Start Think AI with checks

echo "🧠 Think AI Startup Checks"
echo "=========================="

# Check Ollama
echo -n "Checking Ollama... "
if ! command -v ollama &> /dev/null; then
    echo "❌ Not installed"
    echo "Please install: brew install ollama"
    exit 1
fi
echo "✅ Installed"

# Check if Ollama is running
echo -n "Checking Ollama service... "
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Not running"
    echo "Starting Ollama..."
    ollama serve > /dev/null 2>&1 &
    sleep 5
fi
echo "✅ Running"

# Check Phi-3.5 Mini
echo -n "Checking Phi-3.5 Mini model... "
if ! ollama list | grep -q "phi3:mini"; then
    echo "❌ Not found"
    echo "Downloading Phi-3.5 Mini (2.2GB)..."
    ollama pull phi3:mini
else
    echo "✅ Ready"
fi

# Pre-warm the model
echo -n "Pre-warming Phi-3.5 Mini... "
ollama run phi3:mini "Hello" > /dev/null 2>&1
echo "✅ Model loaded"

# Test Ollama response
echo ""
echo "Testing Ollama response..."
python3 test_ollama_simple.py

echo ""
echo "Press Enter to start Think AI with Infinite Consciousness, or Ctrl+C to cancel"
read

# Start the application
python3 infinite_mind_simple.py