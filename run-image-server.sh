#!/bin/bash

echo "🎨 Starting Think AI Server with Image Generation"
echo "==============================================="
echo ""
echo "Features:"
echo "- 💬 Chat interface with full AI responses" 
echo "- 🎨 Image generation with AI learning (720p default)"
echo "- 📦 O(1) caching for instant retrieval"
echo "- 🤖 Continuous improvement through feedback"
echo ""

# Kill any existing process on port 8080
echo "🔧 Clearing port 8080..."
kill $(lsof -t -i:8080) 2>/dev/null || true
sleep 1

# Run the full server with image generation
echo "🚀 Starting server on http://localhost:8080"
echo ""
echo "Available endpoints:"
echo "- Web UI: http://localhost:8080"
echo "- Chat: http://localhost:8080/chat.html"
echo "- Image Generator: http://localhost:8080/static/image_generator.html"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

./target/release/full-server-with-images