#!/bin/bash
set -e

echo "🌐 Testing Think AI PWA (Progressive Web App)"
echo "==========================================="

# Kill any existing processes on port 8080
echo "🔧 Cleaning up port 8080..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 1

# Build the webapp
echo -e "\n📦 Building Think AI webapp..."
cargo build --release --bin think-ai-webapp

# Start the webapp server
echo -e "\n🚀 Starting Think AI PWA server..."
./target/release/think-ai-webapp &
SERVER_PID=$!

# Wait for server to start
sleep 3

echo -e "\n✅ Think AI PWA is running!"
echo ""
echo "📱 PWA Features Available:"
echo "  • Install prompt for desktop/mobile"
echo "  • Offline support with service worker"
echo "  • Background sync for API requests"
echo "  • Automatic cache updates on new builds"
echo "  • App works offline with cached responses"
echo ""
echo "🌐 Open in browser: http://localhost:8080"
echo ""
echo "📲 To test PWA installation:"
echo "  1. Open Chrome/Edge DevTools (F12)"
echo "  2. Go to Application tab > Service Workers"
echo "  3. Check 'Offline' to test offline mode"
echo "  4. Click install button when prompted"
echo ""
echo "Press Ctrl+C to stop the server..."

# Wait for user to stop
trap "kill $SERVER_PID 2>/dev/null; echo -e '\n👋 Server stopped'; exit 0" INT
wait $SERVER_PID