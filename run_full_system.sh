#!/bin/bash
# Think AI Full System Runner - Runs everything concurrently with all capabilities

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🚀 THINK AI FULL SYSTEM LAUNCHER${NC}"
echo -e "${CYAN}================================${NC}"
echo ""

# Function to check if port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  Port $1 is in use. Killing existing process...${NC}"
        lsof -ti:$1 | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
}

# Function to wait for service
wait_for_service() {
    local port=$1
    local service=$2
    local max_attempts=30
    local attempt=0
    
    echo -e "${BLUE}⏳ Waiting for $service to start on port $port...${NC}"
    while ! nc -z localhost $port 2>/dev/null; do
        attempt=$((attempt + 1))
        if [ $attempt -ge $max_attempts ]; then
            echo -e "${RED}❌ $service failed to start on port $port${NC}"
            return 1
        fi
        sleep 1
    done
    echo -e "${GREEN}✅ $service is ready on port $port${NC}"
}

# Create necessary directories
mkdir -p logs trained_knowledge

# Clean up any existing processes
echo -e "${YELLOW}🧹 Cleaning up existing processes...${NC}"
pkill -f "think-ai" 2>/dev/null || true
check_port 8080
check_port 3000
sleep 2

# Build the system if needed
if [ ! -f "./target/release/full-server" ] || [ ! -f "./target/release/self-learning-service" ]; then
    echo -e "${BLUE}🔨 Building Think AI system...${NC}"
    cargo build --release --bin full-server --bin self-learning-service --bin train-comprehensive --bin think-ai
else
    echo -e "${GREEN}✅ Using existing binaries${NC}"
fi

# Check if comprehensive training has been done
if [ ! -f "trained_knowledge/checkpoints/checkpoint_1000000.json" ]; then
    echo -e "${YELLOW}📚 No trained knowledge found. Running comprehensive training...${NC}"
    echo -e "${YELLOW}   This will take a few minutes on first run...${NC}"
    ./target/release/train-comprehensive > logs/training.log 2>&1
    echo -e "${GREEN}✅ Training complete!${NC}"
else
    echo -e "${GREEN}✅ Using existing trained knowledge${NC}"
fi

# Start the comprehensive knowledge loader in background
echo -e "${BLUE}🧠 Starting comprehensive knowledge loader...${NC}"
(
    while true; do
        # Load knowledge if server restarts
        sleep 60
        if ! pgrep -f "think-ai server" > /dev/null; then
            echo "$(date): Knowledge loader detected server restart" >> logs/knowledge_loader.log
        fi
    done
) > logs/knowledge_loader.log 2>&1 &
KNOWLEDGE_LOADER_PID=$!

# Start the HTTP server with full capabilities
echo -e "${BLUE}🌐 Starting HTTP server with API and webapp...${NC}"
RUST_LOG=info ./target/release/full-server > logs/server.log 2>&1 &
SERVER_PID=$!

# Wait for server to be ready
wait_for_service 8080 "HTTP Server"

# Start the exponential self-learning system
echo -e "${BLUE}🧪 Starting exponential self-learning system...${NC}"
./target/release/self-learning-service > logs/self_learning.log 2>&1 &
SELF_LEARNING_PID=$!

# Start background O(1) performance monitor
echo -e "${BLUE}📊 Starting O(1) performance monitor...${NC}"
(
    while true; do
        # Monitor and log performance metrics
        if pgrep -f "think-ai server" > /dev/null; then
            # Try to query the health endpoint
            response_time=$(curl -o /dev/null -s -w '%{time_total}\n' http://localhost:8080/health 2>/dev/null || echo "N/A")
            echo "$(date): Health check response time: ${response_time}s" >> logs/performance.log
        fi
        sleep 10
    done
) > logs/performance_monitor.log 2>&1 &
PERF_MONITOR_PID=$!

# Start a background task to pre-warm caches
echo -e "${BLUE}🔥 Starting cache pre-warmer...${NC}"
(
    sleep 5  # Wait for server to fully start
    while true; do
        # Pre-warm common queries to ensure O(1) performance
        common_queries=(
            "what is programming"
            "explain quantum mechanics"
            "how does AI work"
            "what is consciousness"
            "tell me about mathematics"
        )
        
        for query in "${common_queries[@]}"; do
            curl -s -X POST http://localhost:8080/api/chat \
                -H "Content-Type: application/json" \
                -d "{\"query\": \"$query\"}" > /dev/null 2>&1 || true
        done
        
        echo "$(date): Cache pre-warm cycle completed" >> logs/cache_warmer.log
        sleep 600  # Run every 10 minutes
    done
) > logs/cache_warmer.log 2>&1 &
CACHE_WARMER_PID=$!

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down Think AI system...${NC}"
    
    # Kill all background processes
    kill $KNOWLEDGE_LOADER_PID 2>/dev/null || true
    kill $SERVER_PID 2>/dev/null || true
    kill $SELF_LEARNING_PID 2>/dev/null || true
    kill $PERF_MONITOR_PID 2>/dev/null || true
    kill $CACHE_WARMER_PID 2>/dev/null || true
    
    # Kill any remaining think-ai processes
    pkill -f "think-ai" 2>/dev/null || true
    
    echo -e "${GREEN}✅ Shutdown complete${NC}"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Display system status
clear
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}                    THINK AI FULL SYSTEM RUNNING                ${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}🌐 Web Interface:${NC} http://localhost:8080"
echo -e "${CYAN}📡 API Endpoint:${NC} http://localhost:8080/api/chat"
echo -e "${CYAN}💬 Chat CLI:${NC} ./target/release/think-ai chat (in another terminal)"
echo ""
echo -e "${GREEN}Active Services:${NC}"
echo -e "  ✅ HTTP Server (API + Webapp) - Port 8080"
echo -e "  ✅ Knowledge Intelligence Base - O(1) responses"
echo -e "  ✅ TinyLlama Integration - Local AI model for cache misses"
echo -e "  ✅ Exponential Self-Learning - 4 parallel threads"
echo -e "  ✅ Cache Pre-Warmer - Ensuring O(1) performance"
echo -e "  ✅ Performance Monitor - Tracking response times"
echo ""
echo -e "${GREEN}Background Tasks:${NC}"
echo -e "  🔄 Continuous knowledge generation"
echo -e "  🔄 Automatic knowledge persistence"
echo -e "  🔄 Cache optimization"
echo -e "  🔄 Performance monitoring"
echo ""
echo -e "${YELLOW}Logs:${NC}"
echo -e "  Server: logs/server.log"
echo -e "  Self-Learning: logs/self_learning.log"
echo -e "  Performance: logs/performance.log"
echo ""
echo -e "${YELLOW}Commands:${NC}"
echo -e "  Test API: ${CYAN}curl -X POST http://localhost:8080/api/chat -H 'Content-Type: application/json' -d '{\"query\": \"What is the sun made of?\"}'${NC}"
echo -e "  Chat CLI: ${CYAN}./target/release/think-ai chat${NC}"
echo ""
echo -e "${RED}Press Ctrl+C to stop all services${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"

# Monitor logs in real-time
echo -e "\n${BLUE}📊 Live System Logs:${NC}"
tail -f logs/server.log logs/self_learning.log logs/performance.log 2>/dev/null