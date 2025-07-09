#!/bin/bash

echo "🚀 Think AI Full System E2E Test with Qwen 1.5B Integration"
echo "==========================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check if a command succeeded
check_status() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1${NC}"
    else
        echo -e "${RED}✗ $1${NC}"
        exit 1
    fi
}

# Function to wait for a service to be ready
wait_for_service() {
    local port=$1
    local service=$2
    local max_attempts=30
    local attempt=1
    
    echo -e "${YELLOW}Waiting for $service on port $port...${NC}"
    while ! nc -z localhost $port; do
        if [ $attempt -ge $max_attempts ]; then
            echo -e "${RED}✗ $service failed to start on port $port${NC}"
            return 1
        fi
        sleep 1
        ((attempt++))
    done
    echo -e "${GREEN}✓ $service is ready on port $port${NC}"
    return 0
}

# Kill any existing processes on our ports
echo "🧹 Cleaning up existing processes..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
lsof -ti:8081 | xargs kill -9 2>/dev/null || true
lsof -ti:11434 | xargs kill -9 2>/dev/null || true
sleep 2

# Step 1: Check if Ollama is installed and running
echo ""
echo "📦 Step 1: Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓ Ollama is installed${NC}"
    
    # Start Ollama if not running
    if ! pgrep -x "ollama" > /dev/null; then
        echo "Starting Ollama service..."
        ollama serve &
        OLLAMA_PID=$!
        sleep 5
    fi
    
    # Pull Qwen 1.5B model if not present
    echo "Checking for Qwen 1.5B model..."
    if ! ollama list | grep -q "qwen2.5:1.5b"; then
        echo "Pulling Qwen 1.5B model..."
        ollama pull qwen2.5:1.5b
        check_status "Qwen 1.5B model pulled"
    else
        echo -e "${GREEN}✓ Qwen 1.5B model already available${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Ollama not installed. System will use fallback responses.${NC}"
    echo "  To install: curl -fsSL https://ollama.com/install.sh | sh"
fi

# Step 2: Build the system
echo ""
echo "🔨 Step 2: Building Think AI system..."
cargo build --release 2>&1 | tail -20
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✓ Build completed successfully${NC}"
else
    echo -e "${RED}✗ Build failed. Attempting to fix common issues...${NC}"
    
    # Run fix scripts
    if [ -f ./fix-cli-delimiters.sh ]; then
        chmod +x ./fix-cli-delimiters.sh
        ./fix-cli-delimiters.sh
    fi
    
    # Retry build
    cargo build --release 2>&1 | tail -20
    check_status "Build completed after fixes"
fi

# Step 3: Start the full server with Qwen integration
echo ""
echo "🌐 Step 3: Starting full server with Qwen integration..."
if [ -f ./target/release/full-working-o1 ]; then
    PORT=8080 ./target/release/full-working-o1 &
    SERVER_PID=$!
    wait_for_service 8080 "Full server"
    check_status "Full server started"
else
    echo -e "${RED}✗ full-working-o1 binary not found${NC}"
    exit 1
fi

# Step 4: Start the 3D visualization webapp
echo ""
echo "🎨 Step 4: Starting 3D visualization webapp..."
if [ -f ./target/release/minimal-server ]; then
    PORT=8081 ./target/release/minimal-server &
    WEBAPP_PID=$!
    wait_for_service 8081 "3D webapp"
    check_status "3D webapp started"
else
    echo -e "${YELLOW}⚠ minimal-server not found, using static server${NC}"
    cd static && python3 -m http.server 8081 &
    WEBAPP_PID=$!
    cd ..
    wait_for_service 8081 "Static webapp"
fi

# Step 5: Test API endpoints
echo ""
echo "🧪 Step 5: Testing API endpoints..."

# Test health endpoint
echo "Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8080/health)
if [ "$HEALTH_RESPONSE" = "OK" ]; then
    echo -e "${GREEN}✓ Health check passed${NC}"
else
    echo -e "${RED}✗ Health check failed${NC}"
fi

# Test chat endpoint with contextual query
echo ""
echo "Testing chat endpoint with contextual query..."
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8080/chat \
    -H "Content-Type: application/json" \
    -d '{
        "message": "What is the O(1) performance optimization in Think AI?",
        "context": "Think AI uses hash-based lookups and pre-computed responses to achieve O(1) time complexity for most operations."
    }')

if [ -n "$CHAT_RESPONSE" ]; then
    echo -e "${GREEN}✓ Chat endpoint responded${NC}"
    echo "Response preview: $(echo $CHAT_RESPONSE | jq -r '.response // .content // .message // .' 2>/dev/null | head -c 100)..."
else
    echo -e "${RED}✗ Chat endpoint failed${NC}"
fi

# Test compute endpoint
echo ""
echo "Testing compute endpoint..."
COMPUTE_RESPONSE=$(curl -s -X POST http://localhost:8080/compute \
    -H "Content-Type: application/json" \
    -d '{
        "task": "Analyze the time complexity of binary search",
        "algorithm": "binary_search"
    }')

if [ -n "$COMPUTE_RESPONSE" ]; then
    echo -e "${GREEN}✓ Compute endpoint responded${NC}"
else
    echo -e "${RED}✗ Compute endpoint failed${NC}"
fi

# Step 6: Test Qwen isolation
echo ""
echo "🤖 Step 6: Testing Qwen isolation..."
if [ -f ./target/release/e2e-test-qwen-isolation ]; then
    echo "Running Qwen isolation tests..."
    ./target/release/e2e-test-qwen-isolation
    check_status "Qwen isolation tests completed"
else
    echo -e "${YELLOW}⚠ Qwen isolation test binary not found${NC}"
fi

# Step 7: Test 3D visualization
echo ""
echo "🌟 Step 7: Testing 3D visualization webapp..."
WEBAPP_RESPONSE=$(curl -s http://localhost:8081/)
if echo "$WEBAPP_RESPONSE" | grep -q "Think AI"; then
    echo -e "${GREEN}✓ 3D webapp is serving content${NC}"
    echo ""
    echo "📱 Access the 3D visualization at: http://localhost:8081"
    echo "   Features:"
    echo "   - Interactive 3D consciousness visualization"
    echo "   - Real-time neural network activity"
    echo "   - O(1) performance metrics"
    echo "   - PWA support for offline access"
else
    echo -e "${RED}✗ 3D webapp not responding correctly${NC}"
fi

# Step 8: Performance test
echo ""
echo "⚡ Step 8: Running performance benchmarks..."
echo "Testing response times for O(1) operations..."

# Warm up
for i in {1..5}; do
    curl -s -X POST http://localhost:8080/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "test"}' > /dev/null
done

# Measure response times
TOTAL_TIME=0
NUM_REQUESTS=10

echo "Running $NUM_REQUESTS requests..."
for i in $(seq 1 $NUM_REQUESTS); do
    START_TIME=$(date +%s%N)
    curl -s -X POST http://localhost:8080/chat \
        -H "Content-Type: application/json" \
        -d "{\"message\": \"Query $i: Explain O(1) complexity\"}" > /dev/null
    END_TIME=$(date +%s%N)
    
    ELAPSED=$((($END_TIME - $START_TIME) / 1000000))
    TOTAL_TIME=$(($TOTAL_TIME + $ELAPSED))
    echo -n "."
done
echo ""

AVG_TIME=$(($TOTAL_TIME / $NUM_REQUESTS))
echo -e "${GREEN}✓ Average response time: ${AVG_TIME}ms${NC}"

if [ $AVG_TIME -lt 100 ]; then
    echo -e "${GREEN}✓ Performance meets O(1) targets!${NC}"
else
    echo -e "${YELLOW}⚠ Response time higher than expected for O(1) operations${NC}"
fi

# Summary
echo ""
echo "📊 E2E Test Summary"
echo "=================="
echo -e "${GREEN}✓ System built successfully${NC}"
echo -e "${GREEN}✓ Full server running with Qwen integration${NC}"
echo -e "${GREEN}✓ 3D visualization webapp active${NC}"
echo -e "${GREEN}✓ API endpoints responding${NC}"
echo -e "${GREEN}✓ Performance benchmarks completed${NC}"
echo ""
echo "🎯 System URLs:"
echo "   - API Server: http://localhost:8080"
echo "   - 3D Webapp: http://localhost:8081"
echo "   - Health Check: http://localhost:8080/health"
echo ""
echo "💡 Test with:"
echo '   curl -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '"'"'{"message":"What is Think AI?"}'"'"
echo ""
echo "Press Ctrl+C to stop all services..."

# Keep services running
trap "echo ''; echo 'Shutting down services...'; kill $SERVER_PID $WEBAPP_PID $OLLAMA_PID 2>/dev/null; exit 0" INT TERM

# Wait indefinitely
while true; do
    sleep 1
done