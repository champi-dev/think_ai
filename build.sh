#!/bin/bash
# Railway build script for Think AI Rust server

echo "🚀 Building Think AI Rust Server"
echo "================================"

# Ensure we're building Rust, not Node.js
if [ -f "package.json" ]; then
    echo "❌ ERROR: package.json found - this is a Rust project!"
    echo "Make sure you're deploying the correct repository."
    exit 1
fi

if [ ! -f "Cargo.toml" ]; then
    echo "❌ ERROR: Cargo.toml not found!"
    echo "This doesn't look like the Think AI Rust repository."
    exit 1
fi

echo "✅ Correct repository detected"
echo "📦 Building with cargo..."

# Build the Rust binaries
cargo build --release --bin full-server

if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo ""
echo "Binary location: ./target/release/full-server"
echo "To run: ./target/release/full-server"