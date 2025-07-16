#!/bin/bash

# Stop Think AI services

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Stopping Think AI services...${NC}"

# Stop using PID files if they exist
if [[ -f /tmp/think-ai/http.pid ]]; then
    HTTP_PID=$(cat /tmp/think-ai/http.pid)
    if kill $HTTP_PID 2>/dev/null; then
        echo "Stopped HTTP server (PID: $HTTP_PID)"
    fi
    rm /tmp/think-ai/http.pid
fi

if [[ -f /tmp/think-ai/webapp.pid ]]; then
    WEBAPP_PID=$(cat /tmp/think-ai/webapp.pid)
    if kill $WEBAPP_PID 2>/dev/null; then
        echo "Stopped webapp (PID: $WEBAPP_PID)"
    fi
    rm /tmp/think-ai/webapp.pid
fi

# Kill any remaining processes
pkill -f "think-ai" || true

# Free up ports
sudo fuser -k 8080/tcp 2>/dev/null || true
sudo fuser -k 3000/tcp 2>/dev/null || true

echo -e "${GREEN}All services stopped.${NC}"