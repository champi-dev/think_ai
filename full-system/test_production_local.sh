#!/bin/bash

echo "🧪 Testing Production Build Locally"
echo "==================================="

# Set environment variables
export DEEPGRAM_API_KEY="e31341c95ee93fd2c8fced1bf37636f042fe038b"
export ELEVENLABS_API_KEY="sk_aa595f99bc5842b5df837d4c47fe3a18ce00b9a39a0f2877"
export AUDIO_CACHE_DIR="./audio_cache"
export PORT="8888"  # Different port for local testing
export RUST_LOG="info"

# Create audio cache directory
mkdir -p audio_cache

# Check if binary exists
if [ ! -f target/release/think-ai-full-production ]; then
    echo "❌ Production binary not found!"
    echo "   Run: cargo build --release --bin think-ai-full-production"
    exit 1
fi

echo "✅ Binary found"
echo "🚀 Starting server on port $PORT..."
echo ""
echo "Test URLs:"
echo "- Health: http://localhost:$PORT/health"
echo "- Metrics: http://localhost:$PORT/api/metrics" 
echo "- Dashboard: http://localhost:$PORT/stats"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run the server
./target/release/think-ai-full-production