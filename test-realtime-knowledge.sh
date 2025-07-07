#!/bin/bash
set -e

echo "🌐 Testing Think AI Real-Time Knowledge Gathering"
echo "=============================================="

# Build the binary
echo -e "\n📦 Building real-time knowledge binary..."
cargo build --release --bin start-realtime-knowledge

# Run the knowledge gatherer
echo -e "\n🚀 Starting real-time knowledge gathering..."
echo "This will gather data from public sources like:"
echo "  - Hacker News"
echo "  - Dev.to"
echo "  - Medium (Tech)"
echo "  - TechCrunch"
echo "  - Reddit Technology"
echo ""
echo "Press Ctrl+C to stop"
echo ""

./target/release/start-realtime-knowledge