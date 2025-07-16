#!/bin/bash
# Ollama monitoring script to ensure 100% uptime

while true; do
    # Check if Ollama is running
    if ! pgrep -f "ollama serve" > /dev/null; then
        echo "[$(date)] Ollama is not running, starting it..."
        /snap/bin/ollama serve &
        sleep 5
    fi
    
    # Health check - try to list models
    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "[$(date)] Ollama health check failed, restarting..."
        pkill -f "ollama serve"
        sleep 2
        /snap/bin/ollama serve &
        sleep 10
    fi
    
    # Check if Qwen models are available
    if ! curl -s http://localhost:11434/api/tags | grep -q "qwen"; then
        echo "[$(date)] Qwen models not found, pulling qwen2.5:3b..."
        /snap/bin/ollama pull qwen2.5:3b
    fi
    
    sleep 30
done