#!/bin/bash
set -e

echo "🚀 Think AI Local Testing Guide"
echo "==============================="
echo ""

# 1. Build everything first
echo "📦 Step 1: Build all components"
echo "cargo build --release"
echo ""

# 2. Test the CLI
echo "💬 Step 2: Test the CLI Chat"
echo "./target/release/think-ai chat"
echo "# Try asking questions like:"
echo "# - What is quantum computing?"
echo "# - Explain O(1) algorithms"
echo "# - How does consciousness work?"
echo ""

# 3. Test the HTTP server
echo "🌐 Step 3: Test the HTTP Server"
echo "# First, kill any existing process on port 8080:"
echo "lsof -ti:8080 | xargs kill -9 2>/dev/null || true"
echo "# Then start the server:"
echo "./target/release/think-ai server"
echo "# In another terminal, test with:"
echo "curl -X POST http://localhost:8080/chat -H 'Content-Type: application/json' -d '{\"message\":\"Hello AI\"}'"
echo ""

# 4. Test the webapp
echo "🎨 Step 4: Test the 3D Webapp"
echo "./target/release/think-ai-webapp"
echo "# Open browser to http://localhost:8080"
echo "# You'll see the 3D consciousness visualization"
echo ""

# 5. Test knowledge training
echo "🧠 Step 5: Test Knowledge Training"
echo "./target/release/train-human-conversation"
echo "./target/release/train-consciousness 5"
echo ""

# 6. Test realtime knowledge (requires internet)
echo "📡 Step 6: Test Realtime Knowledge Gathering"
echo "./target/release/start-realtime-knowledge"
echo "# This will gather from Hacker News, Reddit, etc."
echo "# Press Ctrl+C to stop"
echo ""

# 7. Run unit tests
echo "🧪 Step 7: Run Unit Tests"
echo "cargo test"
echo ""

# 8. Run benchmarks
echo "⚡ Step 8: Run Performance Benchmarks"
echo "cargo bench"
echo ""

# 9. Test Python/JS libraries (if installed)
echo "📚 Step 9: Test Published Libraries"
echo "# JavaScript:"
echo "npx thinkai-quantum chat"
echo "# Python:"
echo "pip install thinkai-quantum"
echo "thinkai-quantum chat"
echo ""

echo "✅ All test commands ready!"
echo "Run any of the above commands to test specific components."