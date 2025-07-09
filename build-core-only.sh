#!/bin/bash
set -e

echo "Building core Think AI components only..."
echo "Excluding: image-gen, knowledge (due to compilation issues)"

# Build individual crates that compile cleanly
echo "Building think-ai-core..."
cd think-ai-core && cargo build --release && cd ..

echo "Building think-ai-vector..."
cd think-ai-vector && cargo build --release && cd ..

echo "Building think-ai-cache..."
cd think-ai-cache && cargo build --release && cd ..

echo "Building think-ai-utils..."
cd think-ai-utils && cargo build --release && cd ..

echo "Building think-ai-storage..."
cd think-ai-storage && cargo build --release && cd ..

echo "Building think-ai-consciousness..."
cd think-ai-consciousness && cargo build --release && cd ..

echo "Building think-ai-cli..."
cd think-ai-cli && cargo build --release --no-default-features && cd ..

echo ""
echo "Core components built successfully!"
echo "Binaries available in target/release/"
echo ""
echo "Available CLI commands:"
ls -la target/release/think-ai* | grep -v "\.d$" | grep -v "\.rlib$"