#!/bin/bash
# Build hypercached Docker image with maximum compression

set -e

echo "🚀 Building hypercached Think AI image..."

# Enable BuildKit for better caching
export DOCKER_BUILDKIT=1
export BUILDKIT_PROGRESS=plain

# Image name
IMAGE_NAME="champidev/think-ai"
TAG="hypercache"

# Build with aggressive caching and compression
docker build \
  --build-arg BUILDKIT_INLINE_CACHE=1 \
  --cache-from ${IMAGE_NAME}:${TAG} \
  --cache-from ${IMAGE_NAME}:latest \
  --compress \
  --squash \
  -f Dockerfile.railway-hypercache \
  -t ${IMAGE_NAME}:${TAG} \
  .

# Get image size
SIZE=$(docker images ${IMAGE_NAME}:${TAG} --format "{{.Size}}")
echo "✅ Built ${IMAGE_NAME}:${TAG} - Size: ${SIZE}"

# Tag as latest
docker tag ${IMAGE_NAME}:${TAG} ${IMAGE_NAME}:latest

# Optional: Compress further with docker save
echo "📦 Creating compressed archive..."
docker save ${IMAGE_NAME}:${TAG} | gzip -9 > think-ai-hypercache.tar.gz
ARCHIVE_SIZE=$(ls -lh think-ai-hypercache.tar.gz | awk '{print $5}')
echo "✅ Archive size: ${ARCHIVE_SIZE}"

# Push if requested
if [ "$1" == "push" ]; then
    echo "📤 Pushing to Docker Hub..."
    docker push ${IMAGE_NAME}:${TAG}
    docker push ${IMAGE_NAME}:latest
    echo "✅ Pushed successfully!"
fi

echo "🎉 Done! Use '${IMAGE_NAME}:${TAG}' for Railway deployment"