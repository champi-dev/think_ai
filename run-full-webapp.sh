#!/bin/bash

echo "🚀 Starting Think AI Full System with 3D Web Interface..."
echo
echo "The full system includes:"
echo "  • 3D consciousness visualization"
echo "  • O(1) knowledge engine"
echo "  • WebSocket real-time chat"
echo "  • Interactive quantum field animation"
echo
echo "Building and running..."

cd /home/champi/Dev/think_ai

# Kill any existing processes
pkill -f "think-ai" || true

# Ensure static directory exists
mkdir -p static
cp minimal_3d.html static/index.html 2>/dev/null || true

# Run the full system
echo
echo "🌐 Server starting on http://localhost:8080"
echo "🖥️  Open your browser to: http://localhost:8080"
echo
echo "Features available:"
echo "  • Chat with AI using O(1) performance"
echo "  • Watch real-time 3D consciousness visualization"
echo "  • Experience quantum field animations"
echo "  • Search knowledge base instantly"
echo

cargo run --bin think-ai-full