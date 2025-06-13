#!/bin/bash

echo "🧠 THINK AI - OFFLINE MODE"
echo "========================="
echo ""
echo "Running without distributed databases..."
echo "Using intelligent fallbacks for all features."
echo ""

# Set offline mode
export OFFLINE_MODE=true

# Run the consciousness chat
exec python3 full_architecture_chat.py