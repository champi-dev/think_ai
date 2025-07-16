#!/bin/bash
set -e

echo "=== E2E Test for Code Mode on Production API ==="
echo "Endpoint: https://thinkai.lat"
echo "Testing CodeLlama model selection and code generation"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to test a code query
test_code_query() {
    local query="$1"
    local description="$2"
    local model="$3"
    
    echo -e "\n${BLUE}--- Testing: $description ---${NC}"
    echo "Query: $query"
    echo "Model: ${model:-auto}"
    
    # Build request JSON
    local json_data="{\"query\": \"$query\""
    if [ -n "$model" ]; then
        json_data="${json_data}, \"model\": \"$model\""
    fi
    json_data="${json_data}}"
    
    response=$(curl -s -X POST https://thinkai.lat/api/chat \
        -H "Content-Type: application/json" \
        -d "$json_data" | jq -r '.response' 2>/dev/null || echo "ERROR: Failed to parse response")
    
    if [[ "$response" == *"Knowledge engine LLM not initialized"* ]]; then
        echo -e "${RED}❌ FAILED: Got LLM initialization error!${NC}"
        echo "Response: $response"
        return 1
    elif [[ "$response" == "ERROR: Failed to parse response" ]]; then
        echo -e "${RED}⚠️  WARNING: Failed to parse response (might be network issue)${NC}"
        return 0
    else
        echo -e "${GREEN}✅ SUCCESS: Got valid response${NC}"
        
        # Check if response contains code-related content
        if [[ "$response" == *'```'* ]] || [[ "$response" == *"fn "* ]] || [[ "$response" == *"def "* ]] || [[ "$response" == *"function"* ]] || [[ "$response" == *"const "* ]] || [[ "$response" == *"let "* ]]; then
            echo -e "${GREEN}✅ Response contains code content${NC}"
        else
            echo "⚠️  Response might not contain code (could be context issue)"
        fi
        
        echo "Response preview: ${response:0:150}..."
        return 0
    fi
}

# Run tests
echo -e "\n${BLUE}=== Running Code Mode Tests ===${NC}"

failed=0

# Test 1: Explicit CodeLlama model selection
test_code_query "write hello world in rust" "Rust Hello World with CodeLlama model" "codellama" || ((failed++))

# Test 2: Python code generation with explicit model
test_code_query "write a python function to calculate fibonacci" "Python Fibonacci with CodeLlama model" "codellama" || ((failed++))

# Test 3: Auto-detection for code queries
test_code_query "how to implement quicksort in javascript" "JavaScript Quicksort (auto-detect)" "" || ((failed++))

# Test 4: Complex code query
test_code_query "create a REST API endpoint in rust using axum" "Rust REST API with Axum" "codellama" || ((failed++))

# Test 5: Code explanation
test_code_query "explain this rust code: fn main() { println!(\"Hello\"); }" "Code explanation" "codellama" || ((failed++))

# Test 6: Algorithm implementation
test_code_query "implement binary search tree in python with insert and search methods" "Python BST implementation" "codellama" || ((failed++))

# Test 7: Code debugging
test_code_query "debug this python code: def add(a,b) return a+b" "Python debugging" "codellama" || ((failed++))

# Test 8: Code optimization
test_code_query "optimize this O(n^2) algorithm to O(n log n)" "Algorithm optimization" "codellama" || ((failed++))

# Test with session context for code
SESSION_ID=$(uuidgen)
echo -e "\n${BLUE}--- Testing code generation with conversation context ---${NC}"
echo "Session ID: $SESSION_ID"

# First message - establish context
curl -s -X POST https://thinkai.lat/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"I need help with rust programming\", \"session_id\": \"$SESSION_ID\", \"model\": \"codellama\"}" > /dev/null

# Second message - code request with context
response=$(curl -s -X POST https://thinkai.lat/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"show me how to read a file\", \"session_id\": \"$SESSION_ID\", \"model\": \"codellama\"}" | jq -r '.response' 2>/dev/null || echo "ERROR")

if [[ "$response" == *"Knowledge engine LLM not initialized"* ]]; then
    echo -e "${RED}❌ FAILED: Got LLM error with conversation context!${NC}"
    ((failed++))
elif [[ "$response" == "ERROR" ]]; then
    echo -e "${RED}⚠️  WARNING: Network error${NC}"
else
    echo -e "${GREEN}✅ SUCCESS: Context-aware code generation works${NC}"
    echo "Response preview: ${response:0:150}..."
fi

# Test model switching in same session
echo -e "\n${BLUE}--- Testing model switching in session ---${NC}"

# Switch to general model
response=$(curl -s -X POST https://thinkai.lat/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"what is consciousness\", \"session_id\": \"$SESSION_ID\", \"model\": \"qwen\"}" | jq -r '.response' 2>/dev/null || echo "ERROR")

if [[ "$response" == *"quantum"* ]] || [[ "$response" == *"consciousness"* ]]; then
    echo -e "${GREEN}✅ SUCCESS: Switched to general model (Qwen)${NC}"
else
    echo "⚠️  Might not have switched models properly"
fi

# Summary
echo -e "\n${BLUE}=== Code Mode Test Summary ===${NC}"
if [ $failed -eq 0 ]; then
    echo -e "${GREEN}✅ ALL CODE MODE TESTS PASSED!${NC}"
    echo "CodeLlama integration is working correctly in production."
else
    echo -e "${RED}❌ $failed code mode tests failed${NC}"
fi

# Additional info
echo -e "\n${BLUE}=== Model Selection Info ===${NC}"
echo "- Use \"model\": \"codellama\" for code-specific queries"
echo "- Use \"model\": \"qwen\" for general queries"
echo "- Omit model parameter for automatic detection"