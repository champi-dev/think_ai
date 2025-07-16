#!/bin/bash

echo "🔄 Think AI System Restart Script"
echo "================================="
echo ""

# Check current production status
echo "📊 Current production status:"
PROD_PID=$(pgrep -f 'think-ai-full' | head -1)
if [ -n "$PROD_PID" ]; then
    echo "✅ Production server running (PID: $PROD_PID)"
    ps aux | grep $PROD_PID | grep -v grep
else
    echo "❌ No production server found"
fi

echo ""
echo "🏗️  Rebuilding system..."
if cargo build --release; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi

echo ""
echo "🧪 Testing new binary locally..."
# Kill any test servers
lsof -ti:7777 | xargs kill -9 2>/dev/null || true

# Start test server
PORT=7777 ./target/release/think-ai-full > /tmp/think-ai-test.log 2>&1 &
TEST_PID=$!
sleep 3

# Test endpoints
echo "Testing API endpoints..."
if curl -s -f http://localhost:7777/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "test", "context": "test"}' > /dev/null 2>&1; then
    echo "✅ Chat endpoint working"
else
    echo "❌ Chat endpoint failed"
fi

# Kill test server
kill $TEST_PID 2>/dev/null

echo ""
echo "🚀 To restart production server:"
echo "1. Stop current server: kill $PROD_PID"
echo "2. Start new server: PORT=8080 nohup ./target/release/think-ai-full > /var/log/think-ai.log 2>&1 &"
echo ""
echo "Or use systemd:"
echo "sudo systemctl restart think-ai"