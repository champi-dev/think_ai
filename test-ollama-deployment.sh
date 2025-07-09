#!/bin/bash
set -e

echo "🧪 Testing Ollama deployment locally..."

# Build the Docker image
echo "🔨 Building Docker image..."
docker build -f Dockerfile.railway -t think-ai-ollama-test .

# Run the container
echo "🚀 Starting container..."
docker run -d \
    --name think-ai-test \
    -p 8080:8080 \
    -e PORT=8080 \
    think-ai-ollama-test

# Wait for startup
echo "⏳ Waiting for services to start (60 seconds)..."
sleep 60

# Check if server is running
echo "🔍 Checking server health..."
if curl -s http://localhost:8080/health | grep -q "OK"; then
    echo "✅ Server is healthy!"
else
    echo "❌ Server health check failed"
    docker logs think-ai-test
    docker stop think-ai-test
    docker rm think-ai-test
    exit 1
fi

# Test chat endpoint
echo "💬 Testing chat endpoint..."
RESPONSE=$(curl -s -X POST http://localhost:8080/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "Hello, what is the universe?"}')

echo "📝 Response: $RESPONSE"

# Check if response contains expected fields
if echo "$RESPONSE" | grep -q "response"; then
    echo "✅ Chat endpoint working!"
    
    # Check if using Qwen or fallback
    if echo "$RESPONSE" | grep -q "The universe is"; then
        echo "🎉 Qwen is responding!"
    else
        echo "⚠️ Using fallback responses"
    fi
else
    echo "❌ Chat endpoint failed"
fi

# Cleanup
echo "🧹 Cleaning up..."
docker stop think-ai-test
docker rm think-ai-test

echo "✅ Test complete!"