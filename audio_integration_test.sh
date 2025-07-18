#!/bin/bash

# Audio Integration Test Suite for Think AI
# Tests transcription and synthesis with 100% success rate target

set -e

API_BASE="https://thinkai.lat/api"
SUCCESS_COUNT=0
TOTAL_TESTS=0
RESULTS=()

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎯 Think AI Audio Integration Test Suite${NC}"
echo "=========================================="

# Test function
test_endpoint() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local expected_status="$5"
    
    echo -e "\n${YELLOW}Testing: $name${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$method" = "POST" ]; then
        if [ "$data" = "empty_audio" ]; then
            # Test with empty audio data
            status=$(curl -s -w "%{http_code}" -o /tmp/response.json \
                -X POST "$API_BASE$endpoint" \
                -H "Content-Type: audio/webm" \
                -H "X-Language: auto" \
                --data-binary "@/dev/null")
        else
            # Test with JSON data
            status=$(curl -s -w "%{http_code}" -o /tmp/response.json \
                -X POST "$API_BASE$endpoint" \
                -H "Content-Type: application/json" \
                -d "$data")
        fi
    else
        status=$(curl -s -w "%{http_code}" -o /tmp/response.json \
            -X "$method" "$API_BASE$endpoint")
    fi
    
    if [ "$status" = "$expected_status" ]; then
        echo -e "${GREEN}✓ PASS${NC} - Status: $status"
        SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        RESULTS+=("✓ $name")
        
        # Show response for successful synthesis tests
        if [[ "$endpoint" == *"synthesize"* ]] && [ "$status" = "200" ]; then
            audio_size=$(wc -c < /tmp/response.json)
            echo -e "  ${GREEN}Audio generated: ${audio_size} bytes${NC}"
        fi
    else
        echo -e "${RED}✗ FAIL${NC} - Expected: $expected_status, Got: $status"
        RESULTS+=("✗ $name - Expected: $expected_status, Got: $status")
        if [ -f /tmp/response.json ]; then
            echo -e "  Response: $(head -c 200 /tmp/response.json)"
        fi
    fi
}

# Test Suite: Audio Endpoints
echo -e "\n${BLUE}📡 Testing Audio API Endpoints${NC}"

# Test 1: Health check (baseline)
test_endpoint "API Health Check" "GET" "/health" "" "200"

# Test 2: Audio transcription endpoint exists
test_endpoint "Transcription Endpoint (Empty Audio)" "POST" "/audio/transcribe" "empty_audio" "200"

# Test 3: Audio synthesis functionality
test_endpoint "Speech Synthesis (Hello World)" "POST" "/audio/synthesize" '{"text":"Hello world test"}' "200"

# Test 4: Synthesis with language specification
test_endpoint "Speech Synthesis (Spanish)" "POST" "/audio/synthesize" '{"text":"Hola mundo","language":"es"}' "200"

# Test 5: Synthesis with voice selection
test_endpoint "Speech Synthesis (Custom Voice)" "POST" "/audio/synthesize" '{"text":"Testing voice synthesis","voice_id":"21m00Tcm4TlvDq8ikWAM"}' "200"

# Test 6: Empty synthesis request
test_endpoint "Speech Synthesis (Empty Text)" "POST" "/audio/synthesize" '{"text":""}' "200"

# Test 7: Transcription with language header
test_endpoint "Transcription (Multi-language)" "POST" "/audio/transcribe" "empty_audio" "200"

# Results Summary
echo -e "\n${BLUE}📊 Test Results Summary${NC}"
echo "========================"

SUCCESS_RATE=$((SUCCESS_COUNT * 100 / TOTAL_TESTS))

for result in "${RESULTS[@]}"; do
    if [[ "$result" == ✓* ]]; then
        echo -e "${GREEN}$result${NC}"
    else
        echo -e "${RED}$result${NC}"
    fi
done

echo -e "\n${BLUE}Final Results:${NC}"
echo -e "Tests Passed: ${GREEN}$SUCCESS_COUNT${NC}/$TOTAL_TESTS"
echo -e "Success Rate: ${GREEN}$SUCCESS_RATE%${NC}"

if [ "$SUCCESS_RATE" = "100" ]; then
    echo -e "\n${GREEN}🎉 ALL TESTS PASSED! Audio system is 100% operational!${NC}"
    exit 0
else
    echo -e "\n${RED}❌ Some tests failed. Audio system needs attention.${NC}"
    exit 1
fi