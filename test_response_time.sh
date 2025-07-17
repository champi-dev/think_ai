#!/bin/bash

# Test response time for Think AI API

echo "Testing Think AI response time..."

# Test 1: Simple query
echo -e "\nTest 1: Simple query"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' \
  -w "\nTotal time: %{time_total}s\n"

# Test 2: Complex query
echo -e "\n\nTest 2: Complex query"
time curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the meaning of life?"}' \
  -w "\nTotal time: %{time_total}s\n"

# Test 3: Multiple requests in parallel
echo -e "\n\nTest 3: 5 parallel requests"
for i in {1..5}; do
  (time curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"Request $i\"}" \
    -o /dev/null \
    -w "Request $i - Total time: %{time_total}s\n") &
done
wait

echo -e "\n\nAll tests completed!"