#!/bin/bash

# Think AI Developer Script
# Usage: ./dev.sh [command]
# Commands: start, stop, restart, chat, train, logs, status

BLUE='\033[0;34m'
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Ensure we're in the right directory
cd "$(dirname "$0")"

case "$1" in
    start)
        echo -e "${GREEN}Starting Think AI...${NC}"
        
        # Kill existing processes
        ./dev.sh stop 2>/dev/null
        
        # Build if needed
        if [ ! -f "./target/release/think-ai" ]; then
            echo "Building project..."
            cargo build --release || exit 1
        fi
        
        # Start server
        nohup ./target/release/think-ai server > server.log 2>&1 &
        echo $! > .server.pid
        
        sleep 2
        echo -e "${GREEN}✓ Server running at http://localhost:8080${NC}"
        echo -e "${YELLOW}Run './dev.sh chat' to start chatting${NC}"
        ;;
        
    stop)
        echo -e "${RED}Stopping Think AI...${NC}"
        
        # Kill server
        if [ -f .server.pid ]; then
            kill $(cat .server.pid) 2>/dev/null
            rm .server.pid
        fi
        
        # Kill any other processes
        pkill -f "think-ai" 2>/dev/null
        lsof -ti:8080 | xargs kill -9 2>/dev/null || true
        
        echo -e "${GREEN}✓ All services stopped${NC}"
        ;;
        
    restart)
        ./dev.sh stop
        sleep 1
        ./dev.sh start
        ;;
        
    chat)
        if ! lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null; then
            echo -e "${YELLOW}Server not running. Starting it first...${NC}"
            ./dev.sh start
        fi
        
        echo -e "${BLUE}Starting Think AI Chat...${NC}"
        ./target/release/think-ai chat
        ;;
        
    train)
        echo -e "${BLUE}Starting knowledge training...${NC}"
        ./target/release/train-knowledge
        ;;
        
    logs)
        if [ -f server.log ]; then
            tail -f server.log
        else
            echo "No server logs found. Start the server first."
        fi
        ;;
        
    status)
        echo -e "${BLUE}Think AI Status:${NC}"
        
        if lsof -Pi :8080 -sTCP:LISTEN -t >/dev/null; then
            echo -e "  ${GREEN}✓${NC} Server: Running on port 8080"
            
            # Check health endpoint
            if curl -s http://localhost:8080/health > /dev/null; then
                echo -e "  ${GREEN}✓${NC} Health: OK"
            else
                echo -e "  ${RED}✗${NC} Health: Not responding"
            fi
        else
            echo -e "  ${RED}✗${NC} Server: Not running"
        fi
        
        # Check for training process
        if pgrep -f "train-knowledge" > /dev/null; then
            echo -e "  ${GREEN}✓${NC} Training: Running"
        else
            echo -e "  ${YELLOW}○${NC} Training: Not running"
        fi
        ;;
        
    build)
        echo -e "${BLUE}Building Think AI...${NC}"
        cargo build --release
        ;;
        
    clean)
        echo -e "${YELLOW}Cleaning up...${NC}"
        ./dev.sh stop
        rm -f server.log training.log .server.pid
        echo -e "${GREEN}✓ Cleanup complete${NC}"
        ;;
        
    *)
        echo -e "${BLUE}Think AI Developer Script${NC}"
        echo
        echo "Usage: ./dev.sh [command]"
        echo
        echo "Commands:"
        echo "  start    - Start the server and webapp"
        echo "  stop     - Stop all services"
        echo "  restart  - Restart all services"
        echo "  chat     - Start interactive chat (starts server if needed)"
        echo "  train    - Run knowledge training"
        echo "  logs     - Show server logs (tail -f)"
        echo "  status   - Show system status"
        echo "  build    - Build the project"
        echo "  clean    - Stop services and clean up logs"
        echo
        echo "Quick start: ./dev.sh chat"
        ;;
esac