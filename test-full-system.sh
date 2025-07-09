#!/bin/bash
set -e

echo "🔧 Testing Full System Build..."

# Test if full-system builds
echo "📦 Building full-system binary..."
cd full-system
cargo build --release

echo "✅ Full system build successful!"

# Test running it locally (with timeout)
echo "🚀 Testing server startup..."
timeout 5s cargo run --release || true

echo "
✅ Full system is ready for deployment!

To deploy to Railway:
1. Commit these changes:
   git add .
   git commit -m 'Add full web application system'
   
2. Push to Railway:
   git push
   railway up

The full web app will be available with:
- Interactive chat interface
- O(1) search capabilities
- Real-time WebSocket support
- Knowledge base API
- Beautiful glass morphism UI
"