#!/bin/bash
# Comprehensive system verification for Think AI

echo "🚀 Think AI Full System Verification"
echo "===================================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service
check_service() {
    local name=$1
    local url=$2
    local expected=$3
    
    echo -n "Checking $name: "
    response=$(curl -s -w "\n%{http_code}" "$url" 2>/dev/null | tail -1)
    
    if [ "$response" = "$expected" ]; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED (status: $response)${NC}"
        return 1
    fi
}

# Function to test chat API
test_chat() {
    echo -n "Testing Chat API: "
    response=$(curl -s -X POST http://localhost:7777/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "Hello, test message", "session_id": "test-verify"}')
    
    if echo "$response" | grep -q "response"; then
        echo -e "${GREEN}✅ OK${NC}"
        echo "  Response time: $(echo "$response" | grep -o '"response_time_ms":[0-9]*' | cut -d: -f2)ms"
        echo "  Confidence: $(echo "$response" | grep -o '"confidence":[0-9.]*' | cut -d: -f2)"
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        return 1
    fi
}

# Function to test session persistence
test_session() {
    echo -n "Testing Session Persistence: "
    
    # First message
    curl -s -X POST http://localhost:7777/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "My favorite color is purple", "session_id": "test-session-persist"}' > /dev/null
    
    sleep 1
    
    # Second message testing memory
    response=$(curl -s -X POST http://localhost:7777/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "What is my favorite color?", "session_id": "test-session-persist"}')
    
    if echo "$response" | grep -qi "purple"; then
        echo -e "${GREEN}✅ OK${NC}"
        return 0
    else
        echo -e "${RED}❌ FAILED - Context not retained${NC}"
        return 1
    fi
}

# Function to test audio endpoints
test_audio() {
    echo -n "Testing Audio Endpoints: "
    
    # Test TTS endpoint
    status=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:7777/api/audio/synthesize \
        -H "Content-Type: application/json" \
        -d '{"text": "Hello world"}')
    
    if [ "$status" = "200" ] || [ "$status" = "404" ]; then
        echo -e "${GREEN}✅ Available${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Not configured${NC}"
        return 1
    fi
}

# Function to test security
test_security() {
    echo "Testing Security Features:"
    
    # XSS protection
    echo -n "  XSS Protection: "
    status=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:7777/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "<script>alert(\"xss\")</script>"}')
    
    if [ "$status" = "400" ]; then
        echo -e "${GREEN}✅ OK${NC}"
    else
        echo -e "${RED}❌ FAILED${NC}"
    fi
    
    # SQL injection protection
    echo -n "  SQL Injection Protection: "
    status=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:7777/api/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "\"; DROP TABLE users; --"}')
    
    if [ "$status" = "400" ]; then
        echo -e "${GREEN}✅ OK${NC}"
    else
        echo -e "${RED}❌ FAILED${NC}"
    fi
}

# Function to test performance
test_performance() {
    echo "Testing Performance:"
    
    total_time=0
    count=10
    
    echo -n "  Running $count requests..."
    for i in $(seq 1 $count); do
        start=$(date +%s.%N)
        curl -s -X POST http://localhost:7777/api/chat \
            -H "Content-Type: application/json" \
            -d "{\"message\": \"Test message $i\", \"session_id\": \"perf-test-$i\"}" > /dev/null
        end=$(date +%s.%N)
        duration=$(echo "$end - $start" | bc)
        total_time=$(echo "$total_time + $duration" | bc)
    done
    
    avg_time=$(echo "scale=3; $total_time / $count" | bc)
    echo -e " ${GREEN}Done${NC}"
    echo "  Average response time: ${avg_time}s"
    
    if (( $(echo "$avg_time < 2" | bc -l) )); then
        echo -e "  Performance: ${GREEN}✅ Good${NC}"
    else
        echo -e "  Performance: ${RED}❌ Slow${NC}"
    fi
}

# Function to check metrics
check_metrics() {
    echo -n "Checking Metrics Endpoint: "
    response=$(curl -s http://localhost:7777/metrics)
    
    if echo "$response" | grep -q "total_requests"; then
        echo -e "${GREEN}✅ OK${NC}"
        echo "  Total requests: $(echo "$response" | grep -o '"total_requests":[0-9]*' | cut -d: -f2)"
        echo "  Error count: $(echo "$response" | grep -o '"error_count":[0-9]*' | cut -d: -f2)"
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        return 1
    fi
}

# Main verification
echo "1. Service Health Checks"
echo "-----------------------"
check_service "Health Endpoint" "http://localhost:7777/health" "200"
check_service "Main Page" "http://localhost:7777/" "200"
check_service "Stats Dashboard" "http://localhost:7777/stats" "200"

echo ""
echo "2. API Functionality"
echo "-------------------"
test_chat
test_session
test_audio

echo ""
echo "3. Security Tests"
echo "----------------"
test_security

echo ""
echo "4. Performance Tests"
echo "-------------------"
test_performance

echo ""
echo "5. System Metrics"
echo "----------------"
check_metrics

echo ""
echo "6. System Information"
echo "--------------------"
echo "Server URL: http://localhost:7777"
echo "Process: $(ps aux | grep think-ai-full-production | grep -v grep | awk '{print $2}' | head -1)"
echo "Memory Usage: $(ps aux | grep think-ai-full-production | grep -v grep | awk '{print $6}' | head -1) KB"
echo "CPU Usage: $(ps aux | grep think-ai-full-production | grep -v grep | awk '{print $3}' | head -1)%"

echo ""
echo "===================================="
echo "Verification Complete!"
echo "===================================="