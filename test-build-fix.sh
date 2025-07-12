#!/bin/bash

echo "Testing Think AI build fix..."

# Build the project
echo "Building project..."
cargo build --release

# Check if build succeeded
if [ $? -eq 0 ]; then
    echo "✅ Build succeeded!"
    
    # Test the main binary
    echo "Testing main binary..."
    ./target/release/stable-server-streaming --help
    
    echo "Build artifacts available at:"
    ls -la target/release/ | grep -E "think-ai|stable-server"
else
    echo "❌ Build failed!"
    exit 1
fi