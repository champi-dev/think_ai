#!/bin/bash
# Verify which Docker image Railway will use

echo "🔍 Verifying Docker Image Configuration"
echo "======================================"
echo ""

# Check Dockerfile
echo "1. Dockerfile BASE_IMAGE:"
grep "ARG BASE_IMAGE" Dockerfile | grep -o "devsarmico/think-ai-base:[^ ]*"

# Check railway.json
echo ""
echo "2. railway.json BASE_IMAGE:"
grep -A2 "buildArgs" railway.json | grep "BASE_IMAGE" | grep -o "devsarmico/think-ai-base:[^ \"]*"

# Check if optimized image exists on Docker Hub
echo ""
echo "3. Docker Hub Status:"
if docker manifest inspect devsarmico/think-ai-base:optimized >/dev/null 2>&1; then
    echo "✅ devsarmico/think-ai-base:optimized exists on Docker Hub"
else
    echo "❌ devsarmico/think-ai-base:optimized NOT FOUND on Docker Hub"
    echo "   You need to build and push it first!"
fi

echo ""
echo "4. Image Sizes (if available locally):"
docker images --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}" | grep -E "(REPOSITORY|think-ai-base)"

echo ""
echo "Railway will use the image specified above!"