#!/bin/bash
echo "🧪 Testing Intelligent Token Scaling"
echo "===================================="

# Test 1: Very short greeting (should be fast)
echo -e "\n1. Testing short greeting:"
START=$(date +%s%3N)
RESPONSE=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hi", "session_id": "test-short"}' | jq -r '.response')
END=$(date +%s%3N)
DURATION=$((END - START))
WORD_COUNT=$(echo "$RESPONSE" | wc -w)
echo "Query: 'Hi' (2 chars)"
echo "Response time: ${DURATION}ms"
echo "Response length: $WORD_COUNT words"
echo "Response: $RESPONSE" | head -c 150

# Test 2: Medium question
echo -e "\n\n2. Testing medium question:"
START=$(date +%s%3N)
RESPONSE=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the main benefits of using Python for data science?", "session_id": "test-medium"}' | jq -r '.response')
END=$(date +%s%3N)
DURATION=$((END - START))
WORD_COUNT=$(echo "$RESPONSE" | wc -w)
echo "Query: 'What are the main benefits...' (58 chars)"
echo "Response time: ${DURATION}ms"  
echo "Response length: $WORD_COUNT words"
echo "Response preview: $(echo "$RESPONSE" | head -c 200)..."

# Test 3: Complex detailed request
echo -e "\n\n3. Testing complex request:"
START=$(date +%s%3N)
RESPONSE=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum computing in detail, including how qubits work, quantum entanglement, superposition, and potential applications in cryptography and drug discovery", "session_id": "test-complex"}' | jq -r '.response')
END=$(date +%s%3N)
DURATION=$((END - START))
WORD_COUNT=$(echo "$RESPONSE" | wc -w)
echo "Query: 'Explain quantum computing...' (173 chars)"
echo "Response time: ${DURATION}ms"
echo "Response length: $WORD_COUNT words"
echo "Response preview: $(echo "$RESPONSE" | head -c 200)..."

# Test 4: Code generation (medium-long)
echo -e "\n\n4. Testing code generation:"
START=$(date +%s%3N)
RESPONSE=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a Python function to calculate fibonacci numbers efficiently", "session_id": "test-code"}' | jq -r '.response')
END=$(date +%s%3N)
DURATION=$((END - START))
WORD_COUNT=$(echo "$RESPONSE" | wc -w)
echo "Query: 'Write a Python function...' (75 chars)"
echo "Response time: ${DURATION}ms"
echo "Response length: $WORD_COUNT words"

echo -e "\n===================================="
echo "Summary:"
echo "- Short queries (2 chars) should get ~100-200 tokens"
echo "- Medium queries (50-100 chars) should get ~300-600 tokens"  
echo "- Complex queries (150+ chars) should get ~1000-2000 tokens"
echo "- Response time should scale proportionally"