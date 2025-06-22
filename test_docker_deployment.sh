#!/bin/bash
# Test Docker deployment for full system evidence

echo "🐳 Testing Think AI Docker Deployment"
echo "===================================="

# Build the full system image
echo "1️⃣ Building Docker image..."
if docker build -f Dockerfile.railway-full-optimized -t think-ai-test:full .; then
    echo "✅ Docker build successful"
else
    echo "❌ Docker build failed"
    exit 1
fi

# Get image size
SIZE=$(docker images think-ai-test:full --format "{{.Size}}")
echo "📦 Image size: $SIZE"

# Run container
echo -e "\n2️⃣ Starting container..."
docker run -d --name think-ai-full-test \
    -p 8888:8080 \
    -e PORT=8080 \
    -e THINK_AI_USE_LIGHTWEIGHT=false \
    -e THINK_AI_MINIMAL_INIT=false \
    think-ai-test:full

# Wait for startup
echo "⏳ Waiting for container to start..."
sleep 10

# Test endpoints
echo -e "\n3️⃣ Testing endpoints..."

# Health check
echo -n "Testing /health: "
if curl -s http://localhost:8888/health | jq .; then
    echo "✅ Health endpoint working"
else
    echo "❌ Health endpoint failed"
fi

# Root endpoint
echo -n "Testing /: "
if curl -s http://localhost:8888/ | head -n 5; then
    echo "✅ Root endpoint working"
else  
    echo "❌ Root endpoint failed"
fi

# API endpoints
echo -n "Testing /api/v1/chat: "
if curl -s -X POST http://localhost:8888/api/v1/chat \
    -H "Content-Type: application/json" \
    -d '{"message":"Hello, are you the full system?"}' | jq .; then
    echo "✅ Chat API working"
else
    echo "❌ Chat API failed"
fi

# Container logs
echo -e "\n4️⃣ Container logs:"
docker logs think-ai-full-test 2>&1 | tail -20

# Check what's running inside
echo -e "\n5️⃣ Container contents:"
docker exec think-ai-full-test ls -la /app/ | head -20
echo "..."
docker exec think-ai-full-test find /app -name "*.py" -type f | wc -l
echo "Python files in container"

# Cleanup
echo -e "\n6️⃣ Cleaning up..."
docker stop think-ai-full-test
docker rm think-ai-full-test

echo -e "\n✅ Deployment test complete!"