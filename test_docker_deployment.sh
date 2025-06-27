#!/bin/bash

echo "🐳 Testing Docker deployment build..."

# Clean up any existing containers
docker rm -f think-ai-test 2>/dev/null || true
docker rmi think-ai-test 2>/dev/null || true

# Build Docker image
echo "Building Docker image..."
if docker build -t think-ai-test .; then
    echo "✅ Docker build successful!"
    
    # Test the container
    echo "Starting container..."
    if docker run -d --name think-ai-test -p 8080:8080 think-ai-test; then
        echo "✅ Container started successfully!"
        
        # Wait for startup
        echo "Waiting for server to start..."
        sleep 10
        
        # Test health endpoint
        echo "Testing health endpoint..."
        if curl -f http://localhost:8080/health; then
            echo "✅ Health check passed!"
        else
            echo "❌ Health check failed"
        fi
        
        # Show logs
        echo "Container logs:"
        docker logs think-ai-test
        
        # Cleanup
        docker stop think-ai-test
        docker rm think-ai-test
    else
        echo "❌ Container failed to start"
        exit 1
    fi
else
    echo "❌ Docker build failed"
    exit 1
fi

echo "🎉 Docker deployment test complete!"