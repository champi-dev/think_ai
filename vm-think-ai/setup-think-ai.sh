#!/bin/sh
# Run this inside the Alpine VM after initial setup

echo "📦 Installing Think AI dependencies..."

# Update packages
apk update
apk upgrade

# Install Python and development tools
apk add python3 py3-pip python3-dev
apk add git gcc musl-dev linux-headers
apk add redis neo4j

# Install database tools
apk add postgresql postgresql-dev
apk add --repository=http://dl-cdn.alpinelinux.org/alpine/edge/testing cassandra

# Create Think AI directory
mkdir -p /opt/think-ai

echo "✅ Basic setup complete!"
echo "Next steps:"
echo "1. Copy Think AI code to /opt/think-ai"
echo "2. Install Python dependencies: pip install -r requirements.txt"
echo "3. Start services: redis-server, neo4j, etc."
