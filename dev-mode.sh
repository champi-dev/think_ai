#!/bin/bash

# Think AI Development Script
# Runs system in development mode with auto-reload

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🔧 Think AI Development Mode"
echo "============================"

# Check for cargo-watch
if ! command -v cargo-watch &> /dev/null; then
    echo -e "${YELLOW}Installing cargo-watch for auto-reload...${NC}"
    cargo install cargo-watch
fi

# Kill port 8080
echo "→ Cleaning up port 8080..."
kill -9 $(lsof -t -i:8080) 2>/dev/null || true

# Run with auto-reload
echo -e "${GREEN}Starting with auto-reload...${NC}"
echo "→ Watching for file changes..."
echo

cargo watch -x "run --bin think-ai -- server" \
    -w think-ai-core \
    -w think-ai-http \
    -w think-ai-vector \
    -w think-ai-consciousness \
    -w think-ai-cli