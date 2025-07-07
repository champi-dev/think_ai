#!/bin/bash
set -e

echo "🌐 Quick Test for Think AI Real-Time Knowledge Components"
echo "========================================================"

# Build the libraries
echo -e "\n📦 Building knowledge library..."
cargo build --release --package think-ai-knowledge

# Run unit tests
echo -e "\n🧪 Running knowledge module tests..."
cargo test --package think-ai-knowledge --lib

# Check if binaries compile
echo -e "\n🔧 Checking if realtime knowledge binary compiles..."
cargo check --release --bin start-realtime-knowledge

echo -e "\n✅ All components compile successfully!"
echo "Note: Full network-based testing would require internet connectivity"