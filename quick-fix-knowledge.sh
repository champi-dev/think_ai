#!/bin/bash
# Quick fix to load knowledge and get Think AI responding

echo "🔧 Quick Fix for Think AI Responses"
echo "==================================="
echo ""

# 1. Kill existing server
echo "1️⃣ Stopping existing server..."
killall full-working-o1 2>/dev/null || true
sleep 1

# 2. Check available training binaries
echo ""
echo "2️⃣ Available training options:"
ls target/release/train* target/release/*train* 2>/dev/null | grep -v ".d$" || echo "No training binaries found"

# 3. Try to train with knowledge
echo ""
echo "3️⃣ Loading knowledge base..."

# Try different training binaries in order of preference
if [ -f "target/release/train-comprehensive" ]; then
    echo "Using comprehensive trainer..."
    timeout 30 ./target/release/train-comprehensive || true
elif [ -f "target/release/comprehensive_train" ]; then
    echo "Using comprehensive_train..."
    timeout 30 ./target/release/comprehensive_train || true
elif [ -f "target/release/train_1000" ]; then
    echo "Using train_1000..."
    ./target/release/train_1000
elif [ -f "target/release/train_direct_answers" ]; then
    echo "Using direct answers trainer..."
    ./target/release/train_direct_answers
elif [ -f "target/release/train_minimal" ]; then
    echo "Using minimal trainer..."
    ./target/release/train_minimal
else
    echo "⚠️  No training binary found. Building one..."
    cargo build --release --bin train_1000
    if [ -f "target/release/train_1000" ]; then
        ./target/release/train_1000
    fi
fi

# 4. Check if knowledge files were created
echo ""
echo "4️⃣ Checking knowledge files..."
if ls think-ai*.json 2>/dev/null || ls *.db 2>/dev/null; then
    echo "✅ Knowledge files found:"
    ls -lh think-ai*.json *.db 2>/dev/null | head -5
else
    echo "⚠️  No knowledge files found. Creating minimal knowledge..."
    
    # Create minimal knowledge file
    cat > think-ai-knowledge.json << 'EOF'
{
  "nodes": [
    {
      "id": "1",
      "content": "Hello! I'm Think AI, a high-performance knowledge system with O(1) response time.",
      "domain": "greeting",
      "confidence": 1.0
    },
    {
      "id": "2",
      "content": "The sun is a star at the center of our solar system. It's a nearly perfect sphere of hot plasma.",
      "domain": "astronomy",
      "confidence": 0.95
    },
    {
      "id": "3",
      "content": "O(1) means constant time complexity - operations complete in the same time regardless of input size.",
      "domain": "computer_science",
      "confidence": 1.0
    }
  ]
}
EOF
    echo "Created minimal knowledge file"
fi

# 5. Start server
echo ""
echo "5️⃣ Starting server with knowledge..."
RUST_LOG=info ./target/release/full-working-o1 &
SERVER_PID=$!

# Wait for server
echo "Waiting for server to start..."
for i in {1..10}; do
    if curl -s http://localhost:8080/health >/dev/null 2>&1; then
        echo "✅ Server started!"
        break
    fi
    sleep 1
done

# 6. Test responses
echo ""
echo "6️⃣ Testing responses..."
echo ""

# Test 1: Hello
echo "Test 1 - Greeting:"
curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "hello"}' | jq -r '.response' 2>/dev/null || echo "No response"

echo ""
echo "Test 2 - Knowledge query:"
curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "What is the sun?"}' | jq -r '.response' 2>/dev/null || echo "No response"

echo ""
echo "Test 3 - Stats:"
TOTAL_NODES=$(curl -s http://localhost:8080/api/stats | jq -r '.total_nodes' 2>/dev/null || echo "0")
echo "Total knowledge nodes: $TOTAL_NODES"

# 7. Provide next steps
echo ""
echo "📋 Next Steps:"
echo "============="

if [ "$TOTAL_NODES" = "0" ] || [ -z "$TOTAL_NODES" ]; then
    echo "❌ No knowledge loaded. Try:"
    echo "   1. Build a trainer: cargo build --release --bin train_comprehensive"
    echo "   2. Run trainer: ./target/release/train_comprehensive"
    echo "   3. Restart this script"
else
    echo "✅ Knowledge loaded!"
    echo ""
    echo "Test in your browser:"
    echo "   http://localhost:8080"
    echo ""
    echo "Or use curl:"
    echo '   curl -X POST http://localhost:8080/api/chat \'
    echo '     -H "Content-Type: application/json" \'
    echo '     -d '"'"'{"query": "Your question here"}'"'"
fi

echo ""
echo "Server PID: $SERVER_PID"
echo "To stop: kill $SERVER_PID"