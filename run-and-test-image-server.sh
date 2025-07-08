#!/bin/bash

echo "🎨 Think AI Image Generation - Test Guide"
echo "========================================"
echo ""
echo "This will start the server and show you how to test"
echo "the image generation in the web app."
echo ""

# Kill any existing process
echo "🔧 Clearing port 8080..."
kill $(lsof -t -i:8080) 2>/dev/null || true
sleep 1

echo "🚀 Starting server..."
echo ""

# Start server in background
./target/release/full-server-with-images &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo ""
echo "✅ Server is running!"
echo ""
echo "📱 Open your browser and go to:"
echo ""
echo "   http://localhost:8080/static/image_generator.html"
echo ""
echo "🧪 Test these features:"
echo "1. Enter any prompt and click Generate"
echo "2. Images will appear with white borders"
echo "3. Click feedback buttons (Excellent/Good/etc)"
echo "4. Try the same prompt twice - second is instant!"
echo "5. Check stats at the bottom of the page"
echo ""
echo "💡 Example prompts to try:"
echo "- colorful abstract art"
echo "- futuristic city skyline"
echo "- peaceful zen garden"
echo "- robot playing guitar"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Wait for user to stop
wait $SERVER_PID