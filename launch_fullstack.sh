#!/bin/bash

echo "═══════════════════════════════════════════════════════════════════════╗"
echo "║              🧠 THINK AI FULLSTACK QUANTUM LAUNCHER                    ║"
echo "╠═══════════════════════════════════════════════════════════════════════╣"
echo "║    O(1) Performance AI with 3D Quantum Consciousness Interface        ║"
echo "╚═══════════════════════════════════════════════════════════════════════╝"
echo

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to kill existing processes
cleanup() {
    echo -e "${YELLOW}[!] Cleaning up existing processes...${NC}"
    pkill -f "think-ai server" 2>/dev/null || true
    pkill -f "python.*fullstack_3d.html" 2>/dev/null || true
    sleep 1
}

# Function to check if port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}[!] Port $port is in use. Killing process...${NC}"
        fuser -k $port/tcp 2>/dev/null || true
        sleep 1
    fi
}

# Cleanup
cleanup
check_port 8080
check_port 8000

# Start backend server
echo -e "${BLUE}[1/3] Starting Think AI Backend Server...${NC}"
./target/release/think-ai server --host 0.0.0.0 > server.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}[✓] Backend started (PID: $BACKEND_PID)${NC}"

# Wait for backend to be ready
echo -e "${BLUE}[2/3] Waiting for backend to initialize...${NC}"
for i in {1..10}; do
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo -e "${GREEN}[✓] Backend is ready!${NC}"
        break
    fi
    sleep 1
done

# Start frontend server
echo -e "${BLUE}[3/3] Starting 3D Quantum Interface...${NC}"
cd "$(dirname "$0")"
python3 -m http.server 8000 --bind 0.0.0.0 > frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}[✓] Frontend started (PID: $FRONTEND_PID)${NC}"

echo
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                   🚀 THINK AI FULLSTACK READY!                   ║"
echo "╠══════════════════════════════════════════════════════════════════╣"
echo "║ ▶ 3D Quantum Interface:  http://localhost:8000/fullstack_3d.html ║"
echo "║ ▶ Simple Interface:      http://localhost:8000/interactive.html  ║"
echo "║ ▶ API Endpoint:          http://localhost:8080                   ║"
echo "║ ▶ Health Check:          http://localhost:8080/health            ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo
echo -e "${PURPLE}[i] Press Ctrl+C to stop all services${NC}"
echo

# Function to handle cleanup on exit
cleanup_on_exit() {
    echo
    echo -e "${YELLOW}[!] Shutting down services...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}[✓] All services stopped${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup_on_exit INT

# Keep script running and show logs
echo -e "${BLUE}[i] Tailing server logs...${NC}"
echo "════════════════════════════════════════════════════════════════════"

# Open browser automatically (optional)
if command -v xdg-open > /dev/null; then
    sleep 2
    xdg-open "http://localhost:8000/fullstack_3d.html" 2>/dev/null &
elif command -v open > /dev/null; then
    sleep 2
    open "http://localhost:8000/fullstack_3d.html" 2>/dev/null &
fi

# Tail logs
tail -f server.log frontend.log 2>/dev/null