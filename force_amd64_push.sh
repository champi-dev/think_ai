#!/bin/bash
# Force build and push AMD64 image

echo "🔨 Building AMD64 image for Railway..."
echo "This will take 30-40 minutes on Apple Silicon"
echo ""

# Remove any existing images to avoid confusion
echo "Removing existing images..."
docker rmi devsarmico/think-ai-base:latest || true

# Build specifically for AMD64
echo "Building for linux/amd64..."
docker build \
    --platform linux/amd64 \
    -f Dockerfile.base \
    -t devsarmico/think-ai-base:latest \
    --no-cache \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build complete! Pushing to Docker Hub..."
    docker push devsarmico/think-ai-base:latest
    
    echo ""
    echo "🎉 AMD64 image pushed successfully!"
    echo "Railway will now work correctly!"
else
    echo "❌ Build failed"
    exit 1
fi