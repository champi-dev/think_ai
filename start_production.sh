#!/bin/bash

# Start ThinkAI Production Server

cd /home/champi/Dev/think_ai

# Set environment variables
export DEEPGRAM_API_KEY="e31341c95ee93fd2c8fced1bf37636f042fe038b"
export ELEVENLABS_API_KEY="sk_aa595f99bc5842b5df837d4c47fe3a18ce00b9a39a0f2877"
export AUDIO_CACHE_DIR="./audio_cache"
export PORT="7777"
export RUST_LOG="info"

# Create audio cache directory if needed
mkdir -p audio_cache

# Start the production binary
echo "Starting ThinkAI Production Server..."
echo "Port: $PORT"
echo "Dashboard: http://localhost:$PORT/stats"

# Run in background and redirect output to log
nohup ./target/release/think-ai-full-production > think_ai_production.log 2>&1 &

echo "Server started with PID: $!"
echo "Logs: tail -f think_ai_production.log"