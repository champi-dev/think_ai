#!/bin/bash

# Think AI Response Time Optimization Script
# Goal: Achieve sub-1s response times

set -euo pipefail

echo "🚀 Think AI Performance Optimization"
echo "===================================="

# 1. Enable GPU acceleration for Ollama
echo "1️⃣ Configuring GPU acceleration..."
export CUDA_VISIBLE_DEVICES=0
export OLLAMA_GPU_LAYERS=50
export OLLAMA_NUM_GPU=1

# 2. Configure Ollama for performance
echo "2️⃣ Optimizing Ollama settings..."
cat > ~/.ollama/config.json << EOF
{
  "gpu": true,
  "num_thread": 8,
  "num_gpu": 1,
  "main_gpu": 0,
  "low_vram": false,
  "f16_kv": true,
  "use_mmap": true,
  "use_mlock": false
}
EOF

# 3. Pull optimized model (smaller = faster)
echo "3️⃣ Loading optimized Qwen model..."
ollama pull qwen2.5:0.5b

# 4. Pre-warm the model
echo "4️⃣ Pre-warming model..."
curl -s -X POST http://localhost:11434/api/generate \
  -d '{
    "model": "qwen2.5:0.5b",
    "prompt": "Hello",
    "stream": false,
    "options": {
      "num_predict": 1,
      "temperature": 0.1
    }
  }' > /dev/null

echo "✅ Ollama optimized for GPU acceleration"