#!/bin/bash

echo "Testing GPU server connectivity..."
echo ""

# Test 1: Direct curl to the GPU server
echo "1. Testing direct connection to GPU server:"
curl -X POST http://69.197.178.37:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}' \
  -w "\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  -m 5 || echo "Connection failed"

echo ""
echo "2. Testing CORS headers:"
curl -I http://69.197.178.37:8080/api/chat \
  -H "Origin: https://think-ai-liart.vercel.app" \
  -H "Access-Control-Request-Method: POST" \
  -m 5 || echo "Connection failed"

echo ""
echo "3. Testing if server is running locally:"
curl -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"test"}' \
  -w "\nHTTP Status: %{http_code}\n" \
  -m 2 || echo "Local server not running"

echo ""
echo "4. Checking if the GPU server IP is reachable:"
ping -c 3 69.197.178.37 || echo "Cannot ping GPU server"