#!/bin/bash
# Build and push Think AI v3.1.0 to Docker Hub

# Set variables
DOCKER_USERNAME="${DOCKER_USERNAME:-your-docker-username}"
IMAGE_NAME="think-ai"
VERSION="v3.1.0"
FULL_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"
LATEST_IMAGE_NAME="${DOCKER_USERNAME}/${IMAGE_NAME}:latest"

echo "🚀 Building Think AI v3.1.0 Docker image..."
echo "   Image: ${FULL_IMAGE_NAME}"

# Build the image using Dockerfile.v3
docker build -f Dockerfile.v3 -t ${FULL_IMAGE_NAME} -t ${LATEST_IMAGE_NAME} .

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    
    echo "📤 Pushing to Docker Hub..."
    echo "   Please ensure you're logged in: docker login"
    
    # Push versioned tag
    docker push ${FULL_IMAGE_NAME}
    
    # Push latest tag
    docker push ${LATEST_IMAGE_NAME}
    
    if [ $? -eq 0 ]; then
        echo "✅ Push successful!"
        echo ""
        echo "🎉 Docker image published:"
        echo "   ${FULL_IMAGE_NAME}"
        echo "   ${LATEST_IMAGE_NAME}"
        echo ""
        echo "To deploy on Railway:"
        echo "1. Update your Railway service to use: ${FULL_IMAGE_NAME}"
        echo "2. Or use the Dockerfile.v3 directly in Railway"
    else
        echo "❌ Push failed! Check your Docker Hub credentials"
    fi
else
    echo "❌ Build failed!"
    exit 1
fi