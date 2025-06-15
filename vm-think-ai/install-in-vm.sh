#!/bin/sh
# Run this inside the Alpine VM

echo "📦 Installing Think AI in VM..."

# Install dependencies
apk update
apk add python3 py3-pip git redis postgresql

# Start services
rc-service redis start
rc-update add redis default

# Clone and setup Think AI
cd /root
if [ ! -d "think_ai" ]; then
    # Copy from host or clone
    echo "Please copy Think AI code to /root/think_ai"
else
    cd think_ai
    pip install -r requirements.txt
    python run_full_system.py
fi
