#!/bin/bash

# Verify Think AI deployment
echo "=== Verifying Think AI Deployment ==="

# Check if service is running
if pgrep -f "full-working-o1" > /dev/null; then
    echo "✓ Think AI process is running"
else
    echo "✗ Think AI process is NOT running"
    exit 1
fi

# Check health endpoint
if curl -s http://localhost:8080/health | grep -q "healthy"; then
    echo "✓ Health endpoint responding"
else
    echo "✗ Health endpoint not responding"
fi

# Check for streaming functionality
if curl -s http://localhost:8080/ | grep -q "streaming-text"; then
    echo "✓ Streaming functionality present"
else
    echo "✗ Streaming functionality missing"
fi

# Check for CSS updates
if curl -s http://localhost:8080/ | grep -q "JetBrains Mono"; then
    echo "✓ CSS updates (JetBrains Mono) present"
else
    echo "✗ CSS updates missing"
fi

echo
echo "Deployment verification complete!"
