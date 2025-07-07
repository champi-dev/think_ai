#!/bin/bash
# Debug script for Think AI not returning proper responses

echo "🔍 Debugging Think AI Response Issues"
echo "===================================="
echo ""

# 1. Check if knowledge is loaded
echo "1️⃣ Checking knowledge base..."
echo ""

# Check stats to see if knowledge is loaded
echo "Checking /api/stats endpoint..."
STATS=$(curl -s http://localhost:8080/api/stats 2>/dev/null)
if [ -z "$STATS" ]; then
    echo "❌ Cannot connect to server"
    exit 1
fi

echo "Stats response: $STATS"
echo ""

# Parse total_nodes
TOTAL_NODES=$(echo "$STATS" | grep -o '"total_nodes":[0-9]*' | cut -d':' -f2)
if [ "$TOTAL_NODES" = "0" ] || [ -z "$TOTAL_NODES" ]; then
    echo "❌ No knowledge loaded! Total nodes: 0"
    echo ""
    echo "🔧 Solution: Load knowledge base"
    echo "Run: ./target/release/train-comprehensive"
    echo "Or: cargo run --release --bin train-comprehensive"
else
    echo "✅ Knowledge loaded: $TOTAL_NODES nodes"
fi

# 2. Test direct chat endpoint
echo ""
echo "2️⃣ Testing chat endpoint directly..."
echo ""

CHAT_RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "What is the sun?"}' 2>/dev/null)

echo "Raw response:"
echo "$CHAT_RESPONSE" | jq . 2>/dev/null || echo "$CHAT_RESPONSE"

# 3. Check server logs
echo ""
echo "3️⃣ Recent server logs (last 20 lines)..."
echo ""

# Try to find server process and its output
SERVER_PID=$(lsof -ti:8080 2>/dev/null)
if [ -n "$SERVER_PID" ]; then
    echo "Server PID: $SERVER_PID"
    echo "Check server terminal for error messages"
fi

# 4. Test with verbose mode
echo ""
echo "4️⃣ Testing with debug request..."
echo ""

DEBUG_RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "Hello Think AI", "context": ["debug"], "max_length": 100}' \
    -w "\n\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" 2>/dev/null)

echo "$DEBUG_RESPONSE"

# 5. Recommendations
echo ""
echo "📋 Troubleshooting Steps:"
echo "========================"
echo ""

if [ "$TOTAL_NODES" = "0" ] || [ -z "$TOTAL_NODES" ]; then
    echo "1. Load the knowledge base:"
    echo "   cargo run --release --bin train-comprehensive"
    echo ""
fi

echo "2. Check server startup:"
echo "   - Kill existing server: killall full-working-o1"
echo "   - Start with debug logging: RUST_LOG=debug ./target/release/full-working-o1"
echo ""

echo "3. Verify knowledge files exist:"
echo "   ls -la think-ai.db think_ai_*.json"
echo ""

echo "4. Try the minimal server instead:"
echo "   ./target/release/minimal-server"
echo ""

echo "5. Check for port conflicts:"
echo "   lsof -i:8080"
echo ""

echo "6. Rebuild with fresh state:"
echo "   cargo clean"
echo "   cargo build --release"
echo "   cargo run --release --bin train-comprehensive"
echo "   ./target/release/full-working-o1"