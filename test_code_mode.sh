#\!/bin/bash

echo "Testing Code Mode Formatting"
echo "============================"
echo ""

# Test 1: Simple code request
echo "Test 1: Python function request"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "[CODE REQUEST] Write a Python function to calculate fibonacci numbers",
    "sessionId": "test-code-format",
    "model": "codellama"
  }'  < /dev/null |  jq -r '.response' | head -30

echo ""
echo "Test 2: JavaScript code request"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "[CODE REQUEST] Create a JavaScript function to sort an array of objects by a property",
    "sessionId": "test-code-format-2",
    "model": "codellama"
  }' | jq -r '.response' | head -30

echo ""
echo "Test 3: Bash script request"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "query": "[CODE REQUEST] Write a bash script to backup files to a remote server",
    "sessionId": "test-code-format-3",
    "model": "codellama"
  }' | jq -r '.response' | head -30

