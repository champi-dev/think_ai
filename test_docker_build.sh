#!/bin/bash

echo "🐳 Testing Docker build locally..."

# Build Docker image
echo "Building Docker image..."
docker build -t think-ai-test .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker build successful"

# Run container
echo "Starting container..."
docker run -d --name think-ai-test -p 8080:8080 think-ai-test

# Wait for startup
echo "Waiting for server to start..."
sleep 5

# Test endpoints
echo -e "\n📡 Testing endpoints:"

echo -n "1. Health check: "
curl -s http://localhost:8080/health || echo "FAILED"

echo -e "\n2. Stats endpoint: "
curl -s http://localhost:8080/api/stats | jq '.' || echo "FAILED"

echo -e "\n3. Chat endpoint: "
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Hello"}' | jq '.' || echo "FAILED"

echo -e "\n4. Webapp check: "
curl -s http://localhost:8080 | grep -q "Think AI" && echo "✅ Webapp loaded" || echo "❌ Webapp not found"

# Cleanup
echo -e "\nCleaning up..."
docker stop think-ai-test
docker rm think-ai-test

echo "✅ Docker test complete!"