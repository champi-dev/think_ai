#!/bin/bash

echo "Testing Think AI Natural Language Expression System"
echo "================================================="

# Build the project
echo -e "\n1. Building the project..."
cargo build --release 2>&1 | grep -E "(error|warning|Finished)" || echo "Build completed"

# Test basic CLI chat
echo -e "\n2. Testing basic chat responses..."
echo "Hello!" | ./target/release/think-ai chat 2>/dev/null | head -20
echo "Who are you?" | ./target/release/think-ai chat 2>/dev/null | head -20
echo "What can you do?" | ./target/release/think-ai chat 2>/dev/null | head -20

# Test knowledge queries
echo -e "\n3. Testing knowledge-based responses..."
echo "What is the universe?" | ./target/release/think-ai chat 2>/dev/null | head -20
echo "How does consciousness work?" | ./target/release/think-ai chat 2>/dev/null | head -20

# Test varied responses
echo -e "\n4. Testing response variety..."
for i in {1..3}; do
    echo "Test query $i" | ./target/release/think-ai chat 2>/dev/null | grep -A5 "Think AI" | head -10
done

# Run unit tests
echo -e "\n5. Running unit tests..."
cargo test --lib natural_response 2>&1 | grep -E "(test result|passed|failed)" || echo "Tests completed"
cargo test --lib dynamic_expression 2>&1 | grep -E "(test result|passed|failed)" || echo "Tests completed"

echo -e "\n6. Testing HTTP server integration..."
# Kill any existing server
pkill -f "think-ai server" 2>/dev/null

# Start server in background
./target/release/think-ai server &
SERVER_PID=$!
sleep 2

# Test API endpoints
echo -e "\nTesting /api/chat endpoint..."
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how are you?"}' | jq -r '.response' 2>/dev/null || echo "API test failed"

curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is consciousness?"}' | jq -r '.response' 2>/dev/null || echo "API test failed"

# Clean up
kill $SERVER_PID 2>/dev/null

echo -e "\n7. Performance test..."
time {
    for i in {1..10}; do
        echo "Query $i" | ./target/release/think-ai chat 2>/dev/null >/dev/null
    done
}

echo -e "\nTest complete!"