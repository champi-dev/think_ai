#!/bin/bash

echo "🚀 Think AI GPU Server Deployment Script"
echo "========================================"
echo ""

# Kill any existing server on port 8080
echo "1. Killing existing processes on port 8080..."
sudo lsof -ti:8080 | xargs -r sudo kill -9 2>/dev/null || true

# Build the server
echo ""
echo "2. Building the server in release mode..."
cargo build --release --bin stable-server

# Start the server
echo ""
echo "3. Starting the server..."
echo "Server will be available at http://69.197.178.37:8080"
echo ""

# Export environment variables
export RUST_LOG=info
export PORT=8080

# Run the server
./target/release/stable-server