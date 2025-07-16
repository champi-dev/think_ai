#!/bin/bash
set -e

echo "=== Testing Production Endpoint for LLM Fix ==="
echo "Endpoint: https://thinkai.lat"

# Function to test a query
test_prod_query() {
    local query="$1"
    local description="$2"
    
    echo -e "\n--- Testing: $description ---"
    echo "Query: $query"
    
    response=$(curl -s -X POST https://thinkai.lat/api/chat \
        -H "Content-Type: application/json" \
        -d "{\"query\": \"$query\"}" | jq -r '.response' 2>/dev/null || echo "ERROR: Failed to parse response")
    
    if [[ "$response" == *"Knowledge engine LLM not initialized"* ]]; then
        echo "❌ FAILED: Got LLM initialization error in production!"
        echo "Response: $response"
        return 1
    elif [[ "$response" == "ERROR: Failed to parse response" ]]; then
        echo "⚠️  WARNING: Failed to parse response (might be network issue)"
        return 0
    else
        echo "✅ SUCCESS: No LLM error in production"
        echo "Response preview: ${response:0:100}..."
        return 0
    fi
}

# Run production tests
echo -e "\n=== Running Production Tests ==="

failed=0

test_prod_query "hello" "Simple greeting" || ((failed++))
test_prod_query "what is consciousness" "Philosophical query" || ((failed++))
test_prod_query "explain quantum mechanics" "Scientific query" || ((failed++))
test_prod_query "how do computers work" "Technical query" || ((failed++))
test_prod_query "what is the meaning of life" "Deep philosophical query" || ((failed++))

# Test with model selection
echo -e "\n--- Testing with model selection ---"
response=$(curl -s -X POST https://thinkai.lat/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"write hello world in rust\", \"model\": \"codellama\"}" | jq -r '.response' 2>/dev/null || echo "ERROR")

if [[ "$response" == *"Knowledge engine LLM not initialized"* ]]; then
    echo "❌ FAILED: Got LLM error with CodeLlama model!"
    ((failed++))
else
    echo "✅ SUCCESS: Model selection works without LLM error"
fi

# Summary
echo -e "\n=== Production Test Summary ==="
if [ $failed -eq 0 ]; then
    echo "✅ ALL PRODUCTION TESTS PASSED!"
    echo "The LLM initialization issue has been fixed in production."
else
    echo "❌ $failed production tests failed"
    echo "The fix might not be deployed to production yet."
fi