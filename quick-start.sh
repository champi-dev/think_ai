#!/bin/bash

# Think AI Quick Start Script
# Simple one-liner to get the system running fast

set -e

echo "🚀 Think AI Quick Start"
echo "======================="

# Kill existing processes on port 8080
echo "→ Cleaning up port 8080..."
kill -9 $(lsof -t -i:8080) 2>/dev/null || true

# Build if needed
if [ ! -f "./target/release/think-ai" ]; then
    echo "→ Building Think AI (this may take a minute)..."
    cargo build --release
fi

# Start server
echo "→ Starting Think AI server..."
./target/release/think-ai server &

# Wait for server
sleep 3

# Check health
if curl -s http://localhost:8080/health > /dev/null; then
    echo
    echo "✅ Think AI is running!"
    echo
    echo "🌐 Web Interface: http://localhost:8080"
    echo "❤️  Health Check: http://localhost:8080/health"
    echo "📊 Stats: http://localhost:8080/stats"
    echo
    echo "Press Ctrl+C to stop"
    
    # Keep script running
    wait
else
    echo "❌ Failed to start Think AI"
    exit 1
fi