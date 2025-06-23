#!/bin/bash

# Setup script for Qwen models with Ollama

echo "Think AI - Qwen Models Setup"
echo "============================"
echo

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed."
    echo "Please install Ollama from: https://ollama.com/download"
    exit 1
fi

echo "✅ Ollama is installed"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running. Starting Ollama..."
    ollama serve &
    sleep 3
fi

echo "✅ Ollama is running"
echo

# Function to pull model with progress
pull_model() {
    local model=$1
    local description=$2
    echo "📥 Pulling $model - $description"
    ollama pull "$model"
    echo "✅ $model installed"
    echo
}

echo "Installing lightweight Qwen models..."
echo "====================================="
echo

# Minimal setup - Ultra fast responses
echo "1️⃣  Minimal Setup (Ultra Fast)"
echo "------------------------------"
pull_model "qwen2.5:0.5b" "Ultra-fast chat (0.5B parameters)"
pull_model "qwen2.5:1.5b" "Fast general chat (1.5B parameters)"
pull_model "qwen2.5-coder:1.5b" "Fast code generation (1.5B parameters)"

# Optional: Balanced setup
echo
echo "2️⃣  Optional: Balanced Setup (Better Quality)"
echo "--------------------------------------------"
echo "Install these for better quality responses:"
echo "  ollama pull qwen2.5:3b         # Better chat quality"
echo "  ollama pull qwen2.5-coder:7b   # Excellent code generation"
echo "  ollama pull qwen2.5-math:1.5b  # Math problem solving"
echo

# Optional: Quality setup
echo "3️⃣  Optional: Quality Setup (Best Results)"
echo "-----------------------------------------"
echo "Install these for best quality (requires more resources):"
echo "  ollama pull qwen2.5:7b          # High quality chat"
echo "  ollama pull qwen2.5-coder:32b   # Production-grade code"
echo "  ollama pull qwen2.5-math:7b     # Advanced mathematics"
echo "  ollama pull qwenvl2:7b          # Multimodal (vision+text)"
echo

# List installed models
echo "Installed Qwen models:"
echo "====================="
ollama list | grep -E "qwen|NAME" || echo "No Qwen models found"

echo
echo "✅ Setup complete!"
echo
echo "To test the models, run:"
echo "  python examples/qwen_models_demo.py"
echo
echo "To use a specific model:"
echo "  ollama run qwen2.5:0.5b"