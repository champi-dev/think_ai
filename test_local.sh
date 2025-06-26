#!/bin/bash

echo "🚀 Think AI Local Testing Guide"
echo "================================"

# Check if binary exists
if [ ! -f "./target/release/full-server" ]; then
    echo "⚠️  Binary not found. Building Think AI..."
    cargo build --release
fi

echo -e "\n📋 Available test modes:\n"
echo "1. Start the server:"
echo "   ./target/release/full-server"
echo ""
echo "2. Test with curl (in another terminal):"
echo "   curl -X POST http://localhost:8080/api/chat \\"
echo "     -H 'Content-Type: application/json' \\"
echo "     -d '{\"query\": \"What is the sun?\"}'"
echo ""
echo "3. Use the CLI directly:"
echo "   ./target/release/think-ai chat"
echo ""
echo "4. Run automated tests:"
echo "   ./test_quantum_llm.sh"
echo ""
echo "5. Start with custom knowledge directory:"
echo "   KNOWLEDGE_DIR=/path/to/knowledge ./target/release/full-server"
echo ""
echo "Press Enter to start the server, or Ctrl+C to exit..."
read

# Kill any existing server
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

echo -e "\n🌐 Starting Think AI server on http://localhost:8080..."
./target/release/full-server