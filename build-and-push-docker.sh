#!/bin/bash

# Script to build and push pre-built Docker image

DOCKER_USER="champidev"  # Replace with your Docker Hub username
IMAGE_NAME="think-ai-ollama"
TAG="latest"

echo "🐳 Building pre-built Docker image with Ollama and Qwen..."
echo "=================================================="

# 1. Build the image
echo "📦 Building Docker image..."
docker build -f Dockerfile.prebuilt -t $DOCKER_USER/$IMAGE_NAME:$TAG .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo "✅ Docker image built successfully!"

# 2. Test the image locally
echo ""
echo "🧪 Testing image locally..."
docker run -d --name think-ai-test -p 8080:8080 $DOCKER_USER/$IMAGE_NAME:$TAG

echo "⏳ Waiting 30 seconds for startup..."
sleep 30

# Test endpoints
echo "Testing health endpoint..."
curl -s http://localhost:8080/health
echo ""

echo "Testing chat endpoint..."
curl -s -X POST http://localhost:8080/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "What is 2+2?"}' | jq .

# Clean up test container
docker stop think-ai-test && docker rm think-ai-test

# 3. Push to Docker Hub
echo ""
echo "📤 Push to Docker Hub? (y/n)"
read -r PUSH_CONFIRM

if [ "$PUSH_CONFIRM" = "y" ]; then
    echo "🔐 Logging in to Docker Hub..."
    docker login
    
    echo "📤 Pushing image..."
    docker push $DOCKER_USER/$IMAGE_NAME:$TAG
    
    echo "✅ Image pushed successfully!"
    echo ""
    echo "To use on Railway, create a simple Dockerfile:"
    echo "FROM $DOCKER_USER/$IMAGE_NAME:$TAG"
else
    echo "⏭️ Skipping push. Image available locally as: $DOCKER_USER/$IMAGE_NAME:$TAG"
fi

echo ""
echo "✅ Complete!"