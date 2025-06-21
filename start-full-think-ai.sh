#!/bin/bash
# Start the full Think AI system

echo "🚀 Starting Full Think AI System..."
echo "=================================="

# Kill any existing server on port 8080
echo "Stopping any existing services..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Set environment variables
export PYTHONUNBUFFERED=1
export PORT=8080

# Start the full system
echo "Starting think_ai_full.py on port 8080..."
python think_ai_full.py
