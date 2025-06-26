#!/bin/bash

# Think AI Full System Runner
# This script starts all Think AI components in parallel

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[Think AI]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Function to kill all Think AI processes on exit
cleanup() {
    print_warning "Shutting down Think AI services..."
    
    # Kill all Think AI processes
    pkill -f "think-ai" 2>/dev/null || true
    pkill -f "train-knowledge" 2>/dev/null || true
    
    # Kill processes on specific ports
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    
    print_success "All services stopped"
    exit 0
}

# Set trap to cleanup on exit
trap cleanup EXIT INT TERM

# Check if binaries exist
if [ ! -f "./target/release/think-ai" ]; then
    print_error "Think AI binary not found!"
    print_status "Building the project..."
    cargo build --release
    
    if [ $? -ne 0 ]; then
        print_error "Build failed!"
        exit 1
    fi
    print_success "Build completed"
fi

# Clear terminal for clean start
clear

# Display banner
echo -e "${BLUE}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════╗
║                     🧠 THINK AI SYSTEM LAUNCHER                      ║
╠══════════════════════════════════════════════════════════════════════╣
║  Starting all components: Server, WebApp, Knowledge Engine, and CLI  ║
╚══════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Check if port 8080 is already in use
if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null ; then
    print_warning "Port 8080 is already in use. Killing existing process..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# Start HTTP Server (includes webapp)
print_status "Starting HTTP server on http://localhost:8080..."
./target/release/think-ai server --host 0.0.0.0 --port 8080 > server.log 2>&1 &
SERVER_PID=$!
sleep 2

# Check if server started successfully
if kill -0 $SERVER_PID 2>/dev/null; then
    print_success "Server started (PID: $SERVER_PID)"
    print_success "Web interface available at: http://localhost:8080"
else
    print_error "Failed to start server. Check server.log for details"
    exit 1
fi

# Optional: Start knowledge training in background
read -p "Do you want to run knowledge training in background? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Starting knowledge training in background..."
    ./target/release/train-knowledge > training.log 2>&1 &
    TRAINING_PID=$!
    print_success "Training started (PID: $TRAINING_PID) - Check training.log for progress"
fi

# Display system status
echo
print_success "All systems operational!"
echo
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Available Services:${NC}"
echo -e "  ${BLUE}►${NC} Web Interface:    http://localhost:8080"
echo -e "  ${BLUE}►${NC} API Health Check: http://localhost:8080/health"
echo -e "  ${BLUE}►${NC} Server Logs:      tail -f server.log"
if [ ! -z "$TRAINING_PID" ]; then
    echo -e "  ${BLUE}►${NC} Training Logs:    tail -f training.log"
fi
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo

# Start interactive CLI
print_status "Starting Think AI Interactive Chat..."
echo -e "${YELLOW}Tip: Type 'help' for available commands${NC}"
echo

# Run the CLI (this will be interactive)
./target/release/think-ai chat

# This line will only be reached when user exits the chat
print_status "Chat session ended"