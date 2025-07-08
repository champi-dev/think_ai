#!/bin/bash

echo "🧭 Testing Think AI Navigation Links"
echo "===================================="
echo ""

# Kill any existing process
echo "🔧 Clearing port 8080..."
kill $(lsof -t -i:8080) 2>/dev/null || true
sleep 1

echo "🚀 Starting server..."
./target/release/full-server-with-images &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo ""
echo "✅ Server is running!"
echo ""
echo "🔗 Available routes:"
echo ""
echo "1. Main 3D Visualization:"
echo "   http://localhost:8080/"
echo ""
echo "2. Chat Interface:"
echo "   http://localhost:8080/chat.html"
echo ""
echo "3. Image Generator (multiple routes):"
echo "   http://localhost:8080/image-generator"
echo "   http://localhost:8080/images"
echo "   http://localhost:8080/static/image_generator.html"
echo ""
echo "📱 Navigation features:"
echo "- Each page has links to the other sections"
echo "- Image generator is accessible from all pages"
echo "- Consistent navigation experience"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Wait for user to stop
wait $SERVER_PID