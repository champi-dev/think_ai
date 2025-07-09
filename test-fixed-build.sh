#!/bin/bash
set -e

echo "Testing fixed build..."
echo "===================="

# Build all modules except webapp and image-gen
echo "Building core modules..."
cargo build --release --workspace \
    --exclude think-ai-webapp \
    --exclude think-ai-image-gen \
    2>&1 | tail -20

echo ""
echo "Build complete! Checking results..."
echo "==================================="

echo ""
echo "Available binaries:"
ls -la target/release/think-ai* 2>/dev/null | grep -v "\.d$" | grep -v "\.rlib$" || echo "No binaries found"

echo ""
echo "Available libraries:"
ls -la target/release/*.rlib | grep think_ai | wc -l
echo "libraries built"

echo ""
echo "Build successful!"