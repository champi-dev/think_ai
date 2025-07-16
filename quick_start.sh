#!/bin/bash

# Quick Start - Runs everything in parallel with minimal setup

# Kill any existing processes on port 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Build if needed
[ ! -f "./target/release/think-ai" ] && cargo build --release

# Start server in background
./target/release/think-ai server &

# Give server time to start
sleep 2

# Display info
echo "═══════════════════════════════════════════════════════════════"
echo "🧠 Think AI is running!"
echo "📡 API: http://localhost:8080"
echo "💬 Starting interactive chat..."
echo "═══════════════════════════════════════════════════════════════"
echo

# Start interactive chat
./target/release/think-ai chat

# Kill server when chat exits
pkill -f "think-ai server"