#!/bin/bash
# Deploy with Docker

echo "Building and running Think AI v3.1.0 with Docker..."

# Build
docker build -f Dockerfile.railway -t think-ai:latest .

# Run
docker run -d \
  --name think-ai \
  -p 8080:8080 \
  -e PORT=8080 \
  -e THINK_AI_COLOMBIAN=true \
  --restart unless-stopped \
  think-ai:latest

echo "Think AI is running at http://localhost:8080"
