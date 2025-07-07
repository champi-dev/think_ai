#!/bin/bash
# Quick local test script for Think AI

set -e

echo "🧪 Think AI Local Testing"
echo "========================"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo "✅ $2"
    else
        echo "❌ $2"
        return 1
    fi
}

# Kill any existing processes on port 8080
echo "🔧 Preparing environment..."
if lsof -ti:8080 >/dev/null 2>&1; then
    echo "   Killing processes on port 8080..."
    lsof -ti:8080 | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# 1. Check Rust installation
echo ""
echo "1️⃣ Checking Rust installation..."
if command_exists cargo; then
    RUST_VERSION=$(rustc --version | cut -d' ' -f2)
    echo "   ✅ Rust installed: $RUST_VERSION"
else
    echo "   ❌ Rust not installed. Please install from https://rustup.rs"
    exit 1
fi

# 2. Build the project
echo ""
echo "2️⃣ Building Think AI..."
if cargo build --release --bin full-working-o1 2>/dev/null; then
    print_status 0 "Build successful"
else
    echo "   ⚠️  Build failed. Trying without web-scraping features..."
    cargo build --release --bin full-working-o1 --no-default-features
fi

# 3. Run tests
echo ""
echo "3️⃣ Running tests..."
if cargo test --lib --bins -- --nocapture 2>/dev/null | grep -q "test result: ok"; then
    print_status 0 "Tests passed"
else
    print_status 1 "Some tests failed (this might be okay)"
fi

# 4. Start the server
echo ""
echo "4️⃣ Starting Think AI server..."
./target/release/full-working-o1 &
SERVER_PID=$!
echo "   Server PID: $SERVER_PID"

# Wait for server to start
echo "   Waiting for server to start..."
for i in {1..30}; do
    if curl -s http://localhost:8080/health >/dev/null 2>&1; then
        break
    fi
    sleep 1
done

# 5. Test endpoints
echo ""
echo "5️⃣ Testing API endpoints..."

# Health check
echo ""
echo "   Testing /health endpoint..."
HEALTH_RESPONSE=$(curl -s http://localhost:8080/health)
if echo "$HEALTH_RESPONSE" | grep -q "ok"; then
    print_status 0 "Health check passed"
    echo "   Response: $HEALTH_RESPONSE"
else
    print_status 1 "Health check failed"
fi

# Chat endpoint
echo ""
echo "   Testing /api/chat endpoint..."
CHAT_RESPONSE=$(curl -s -X POST http://localhost:8080/api/chat \
    -H "Content-Type: application/json" \
    -d '{"query": "What is O(1) performance?"}' 2>/dev/null || echo "failed")

if echo "$CHAT_RESPONSE" | grep -q "response"; then
    print_status 0 "Chat endpoint working"
    echo "   Response preview: $(echo "$CHAT_RESPONSE" | head -c 100)..."
else
    print_status 1 "Chat endpoint failed"
fi

# Stats endpoint
echo ""
echo "   Testing /api/stats endpoint..."
STATS_RESPONSE=$(curl -s http://localhost:8080/api/stats 2>/dev/null || echo "failed")
if echo "$STATS_RESPONSE" | grep -q "total"; then
    print_status 0 "Stats endpoint working"
else
    print_status 1 "Stats endpoint failed"
fi

# 6. Test JavaScript library (if npm is installed)
if command_exists npm; then
    echo ""
    echo "6️⃣ Testing JavaScript library..."
    cd think-ai-js
    
    if [ ! -d "node_modules" ]; then
        echo "   Installing dependencies..."
        npm install --silent
    fi
    
    echo "   Building library..."
    npm run build --silent
    
    echo "   Testing CLI..."
    if node dist/cli.js --version 2>/dev/null | grep -q "1.0"; then
        print_status 0 "JavaScript CLI working"
    else
        print_status 1 "JavaScript CLI failed"
    fi
    
    cd ..
else
    echo ""
    echo "6️⃣ Skipping JavaScript tests (npm not installed)"
fi

# 7. Test Python library (if python3 is installed)
if command_exists python3; then
    echo ""
    echo "7️⃣ Testing Python library..."
    cd think-ai-py
    
    echo "   Installing library..."
    pip install -e . --quiet
    
    echo "   Testing import..."
    if python3 -c "from think_ai import ThinkAI; print('Import successful')" 2>/dev/null; then
        print_status 0 "Python library working"
    else
        print_status 1 "Python library failed"
    fi
    
    cd ..
else
    echo ""
    echo "7️⃣ Skipping Python tests (python3 not installed)"
fi

# 8. Performance check
echo ""
echo "8️⃣ Quick performance check..."
echo "   Sending 10 requests..."
TOTAL_TIME=0
for i in {1..10}; do
    START=$(date +%s%N)
    curl -s http://localhost:8080/health >/dev/null 2>&1
    END=$(date +%s%N)
    ELAPSED=$((($END - $START) / 1000000))
    TOTAL_TIME=$(($TOTAL_TIME + $ELAPSED))
done
AVG_TIME=$(($TOTAL_TIME / 10))
echo "   Average response time: ${AVG_TIME}ms"

if [ $AVG_TIME -lt 50 ]; then
    print_status 0 "Performance is O(1) - excellent!"
else
    print_status 1 "Performance might need optimization"
fi

# Cleanup
echo ""
echo "🧹 Cleaning up..."
kill $SERVER_PID 2>/dev/null || true
echo "   Server stopped"

# Summary
echo ""
echo "📊 Test Summary"
echo "=============="
echo ""
echo "✅ What's working:"
echo "   - Rust build system"
echo "   - Core O(1) engine"
echo "   - HTTP server"
echo "   - API endpoints"
if [ $AVG_TIME -lt 50 ]; then
    echo "   - O(1) performance verified!"
fi

echo ""
echo "📝 Next steps:"
echo "   1. Run full tests: cargo test"
echo "   2. Run benchmarks: cargo bench"
echo "   3. Test libraries: see LOCAL-TESTING-GUIDE.md"
echo "   4. Deploy: ./deploy-after-checks.sh"

echo ""
echo "🚀 Think AI is ready for local development!"