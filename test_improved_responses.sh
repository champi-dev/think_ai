#\!/bin/bash
echo "🧪 Testing Improved Response Generation"
echo "====================================="

# Test 1: Complex explanation request
echo -e "\n1. Testing complex explanation (should be detailed):"
echo "Request: Explain quantum physics in detail"
RESPONSE=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain quantum physics in detail", "session_id": "test-complex"}')

RESP_LENGTH=$(echo "$RESPONSE" | jq -r '.response' | wc -w)
echo "Response word count: $RESP_LENGTH"
echo "First 100 chars: $(echo "$RESPONSE" | jq -r '.response' | head -c 100)..."

# Test 2: Session context retention
echo -e "\n2. Testing session context:"
curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My name is TestUser and I love quantum physics", "session_id": "test-context"}' > /dev/null

sleep 1

RESPONSE2=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is my name and what do I love?", "session_id": "test-context"}')

echo "Response: $(echo "$RESPONSE2" | jq -r '.response' | head -c 200)"

# Test 3: Code generation request
echo -e "\n3. Testing code generation (should be substantial):"
RESPONSE3=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a Python function to implement quicksort with detailed comments", "session_id": "test-code"}')

CODE_LENGTH=$(echo "$RESPONSE3" | jq -r '.response' | wc -w)
echo "Code response word count: $CODE_LENGTH"

# Test 4: Simple greeting (should be shorter)
echo -e "\n4. Testing simple greeting:"
RESPONSE4=$(curl -s -X POST http://localhost:7777/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test-greeting"}')

GREETING_LENGTH=$(echo "$RESPONSE4" | jq -r '.response' | wc -w)
echo "Greeting word count: $GREETING_LENGTH"
echo "Response: $(echo "$RESPONSE4" | jq -r '.response')"

echo -e "\n====================================="
echo "Test Summary:"
echo "- Complex explanation: $RESP_LENGTH words (target: 500-1000+)"
echo "- Code generation: $CODE_LENGTH words (target: 300-600+)"
echo "- Simple greeting: $GREETING_LENGTH words (target: 20-50)"
