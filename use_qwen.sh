#!/bin/bash

# Quick script to use Qwen models with Think AI

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Start Ollama if not running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Pull lightweight Qwen models if not already installed
echo "Setting up Qwen models..."
ollama pull qwen2.5:0.5b 2>/dev/null || true
ollama pull qwen2.5:1.5b 2>/dev/null || true
ollama pull qwen2.5-coder:1.5b 2>/dev/null || true

# Run the demo
echo "Running Qwen models demo..."
python examples/qwen_models_demo.py

# Optional: Interactive mode
echo -e "\nWant to chat with a specific model? Try:"
echo "  ollama run qwen2.5:0.5b    # Ultra fast"
echo "  ollama run qwen2.5:1.5b    # Balanced"
echo "  ollama run qwen2.5-coder:1.5b  # For coding"