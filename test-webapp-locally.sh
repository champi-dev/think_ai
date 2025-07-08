#!/bin/bash

echo "🎨 Think AI Image Generation - Local Testing Guide"
echo "================================================"
echo ""

# Check if server binary exists
if [ ! -f "./target/release/full-server-with-images" ]; then
    echo "❌ Server binary not found. Building..."
    cargo build --release --bin full-server-with-images
fi

echo "📋 Instructions:"
echo ""
echo "1. In Terminal 1 - Start the server:"
echo "   ./target/release/full-server-with-images"
echo ""
echo "2. In Terminal 2 (optional) - Watch the logs:"
echo "   tail -f webapp_image_cache/*.json"
echo ""
echo "3. In your web browser, open:"
echo "   http://localhost:8080/static/image_generator.html"
echo ""
echo "🧪 Test Scenarios:"
echo "-----------------"
echo "1. Basic Generation:"
echo "   - Enter: 'a beautiful mountain landscape'"
echo "   - Click Generate"
echo "   - Image appears with AI enhancements"
echo ""
echo "2. Test O(1) Cache:"
echo "   - Generate same prompt again"
echo "   - Should be instant with 'O(1) CACHED' badge"
echo ""
echo "3. Test Learning:"
echo "   - Rate images as Excellent/Good/etc"
echo "   - Check stats update in real-time"
echo ""
echo "4. Test Different Sizes:"
echo "   - Try 1024x1024 for square"
echo "   - Try 1280x720 for landscape (default)"
echo "   - Try 768x1024 for portrait"
echo ""
echo "📱 Other Pages to Test:"
echo "----------------------"
echo "- Main 3D Viz: http://localhost:8080/"
echo "- Chat Interface: http://localhost:8080/chat.html"
echo "- Image Generator: http://localhost:8080/static/image_generator.html"
echo ""
echo "🛠️ Troubleshooting:"
echo "------------------"
echo "- Port in use? Run: kill \$(lsof -t -i:8080)"
echo "- Can't generate? Check console for errors"
echo "- Images look weird? That's the placeholder generator!"
echo ""
echo "Press Enter to start the server now, or Ctrl+C to exit..."
read

# Kill existing process
echo "🔧 Clearing port 8080..."
kill $(lsof -t -i:8080) 2>/dev/null || true
sleep 1

# Start server
echo "🚀 Starting server..."
./target/release/full-server-with-images