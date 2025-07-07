#!/bin/bash

echo "=== Think AI E2E Test Script ==="
echo "Testing response quality improvements"
echo "=================================="

# Test queries
queries=(
    "what is the sun"
    "what is the universe" 
    "what is love"
    "what is programming"
)

# Create a temporary test script
cat > /tmp/test_queries.txt << EOF
what is the sun
exit
EOF

echo -e "\n1. Testing query: 'what is the sun'"
echo "-----------------------------------"
timeout 10s ./target/release/think-ai chat < /tmp/test_queries.txt 2>&1 | grep -A 5 "what is the sun" | grep -v "You:" | grep -v "exit" | grep -v "self-evaluation" | head -20

# Check for template patterns
echo -e "\n2. Checking for template patterns..."
echo "-----------------------------------"
response=$(timeout 10s ./target/release/think-ai chat < /tmp/test_queries.txt 2>&1 | grep -A 5 "what is the sun")

# Template patterns to check
if echo "$response" | grep -q "Your question about"; then
    echo "❌ Found: 'Your question about'"
fi

if echo "$response" | grep -q "Regarding your inquiry about"; then
    echo "❌ Found: 'Regarding your inquiry about'"
fi

if echo "$response" | grep -q "Throughout history"; then
    echo "❌ Found: 'Throughout history'"
fi

if echo "$response" | grep -q "continues to evolve with new discoveries"; then
    echo "❌ Found: 'continues to evolve with new discoveries'"
fi

if echo "$response" | grep -q "Practically, this allows"; then
    echo "❌ Found: 'Practically, this allows'"
fi

if echo "$response" | grep -q "Important features are"; then
    echo "❌ Found: 'Important features are'"
fi

# If none found
if ! echo "$response" | grep -qE "Your question about|Regarding your inquiry|Throughout history|continues to evolve|Practically, this allows|Important features are"; then
    echo "✅ No template patterns detected!"
fi

echo -e "\n3. Raw response content:"
echo "------------------------"
echo "$response"

# Cleanup
rm /tmp/test_queries.txt