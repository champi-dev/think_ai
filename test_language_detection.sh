#!/bin/bash

# Test language detection locally

echo "=== Testing Language Detection in Think AI ==="
echo

# Kill any existing processes on test port
echo "WARNING: This will kill any process on port 8080. Make sure it's not production!"
echo "Press Ctrl+C to cancel, or wait 3 seconds to continue..."
sleep 3

echo "Killing any processes on port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 1

# Start the server in background
echo "Starting HTTP server on port 8080..."
cargo run --bin think-ai-server &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
sleep 10

# Check if server is running
echo "Checking server health..."
curl http://localhost:8080/health -s || echo "Server health check failed"
echo

# Test 1: Spanish language detection
echo
echo "Test 1: Spanish language detection"
echo "Sending request with Accept-Language: es-ES"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -H "Accept-Language: es-ES,es;q=0.9,en;q=0.8" \
  -d '{"message": "Hola"}' \
  -s | python3 -m json.tool

# Test 2: French language detection
echo
echo "Test 2: French language detection"
echo "Sending request with Accept-Language: fr-FR"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -H "Accept-Language: fr-FR" \
  -d '{"message": "Bonjour"}' \
  -s | python3 -m json.tool

# Test 3: Default to English
echo
echo "Test 3: Default to English (no Accept-Language header)"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}' \
  -s | python3 -m json.tool

# Test 4: Explicit language parameter
echo
echo "Test 4: Explicit language parameter (Japanese)"
echo "Header says English but explicit parameter says Japanese"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -H "Accept-Language: en-US" \
  -d '{"message": "Konnichiwa", "language": "ja"}' \
  -s | python3 -m json.tool

# Test 5: RTL language (Arabic)
echo
echo "Test 5: RTL language detection (Arabic)"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -H "Accept-Language: ar-SA" \
  -d '{"message": "مرحبا"}' \
  -s | python3 -m json.tool

# Test 6: Quality values
echo
echo "Test 6: Language quality values"
echo "Accept-Language: en;q=0.5,de;q=0.9,es;q=0.8"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -H "Accept-Language: en;q=0.5,de;q=0.9,es;q=0.8" \
  -d '{"message": "Test"}' \
  -s | python3 -m json.tool

# Test 7: Invalid language fallback
echo
echo "Test 7: Invalid language fallback"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test", "language": "xyz"}' \
  -s | python3 -m json.tool

# Kill the server
echo
echo "Killing server..."
kill $SERVER_PID 2>/dev/null || true

echo
echo "=== Testing complete ==="