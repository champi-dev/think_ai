#!/bin/bash
# Run Think AI v3.1.0 with Railway-compatible settings

echo "🚀 Starting Think AI v3.1.0..."
echo "Port: ${PORT:-8080}"
echo "Colombian mode: ${THINK_AI_COLOMBIAN:-true}"

# Change to the v3 directory
cd "$(dirname "$0")/think_ai_v3"

# Set default environment variables
export THINK_AI_COLOMBIAN="${THINK_AI_COLOMBIAN:-true}"
export THINK_AI_MODEL="${THINK_AI_MODEL:-Qwen/Qwen2.5-Coder-1.5B}"

# Run the application
python app.py