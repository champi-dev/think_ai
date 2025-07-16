#!/bin/bash
set -e

# For Railway deployment
export RUST_LOG=info

# Use PORT from environment or default to 8080
PORT=${PORT:-8080}

echo "🚀 Starting Think AI Server on port $PORT"

# Run the server command
exec ./target/release/think-ai server --port $PORT --host 0.0.0.0