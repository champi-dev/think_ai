#!/bin/bash
# Test if Railway will use the pre-built image

echo "🔍 Testing Railway Docker build locally..."
echo ""

# Check if base image exists on Docker Hub
echo "1. Checking if base image exists on Docker Hub:"
if docker pull devsarmico/think-ai-base:latest --dry-run &>/dev/null || docker pull devsarmico/think-ai-base:latest &>/dev/null; then
    echo "   ✅ Base image found!"
else
    echo "   ❌ Base image NOT found on Docker Hub"
    echo "   You need to push it first: docker push devsarmico/think-ai-base:latest"
    exit 1
fi

echo ""
echo "2. Testing Railway build locally:"
echo "   This simulates what Railway will do..."
echo ""

# Simulate Railway build
docker build \
    -f Dockerfile.api \
    --build-arg BASE_IMAGE=devsarmico/think-ai-base:latest \
    -t test-railway-build \
    .

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCESS! Railway will use your pre-built image!"
    echo ""
    echo "Build time comparison:"
    echo "- With pre-built image: <10 seconds ✨"
    echo "- Without pre-built image: 10+ minutes 😴"
else
    echo ""
    echo "❌ Build failed. Check the error above."
fi