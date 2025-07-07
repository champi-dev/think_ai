#!/bin/bash
# Run Think AI as a True LLM

echo "🧠 Starting Think AI LLM"
echo "======================="
echo ""

# Kill any existing servers
echo "Stopping existing servers..."
pkill -f "think-ai-llm" 2>/dev/null || true
pkill -f "full-working-o1" 2>/dev/null || true
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
sleep 1

# Run the LLM
echo "Starting LLM server..."
./target/release/think-ai-llm &
SERVER_PID=$!

# Wait for server to start
echo "Waiting for server to start..."
for i in {1..10}; do
    if curl -s http://localhost:8080/health >/dev/null 2>&1; then
        echo "✅ Server started!"
        break
    fi
    sleep 1
done

echo ""
echo "🚀 Think AI LLM is running!"
echo ""
echo "Test commands:"
echo "============="
echo ""
echo "1. Basic chat:"
echo '   curl -X POST http://localhost:8080/api/chat \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"query": "Hello!"}'"'"
echo ""
echo "2. Knowledge query:"
echo '   curl -X POST http://localhost:8080/api/chat \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"query": "What is artificial intelligence?"}'"'"
echo ""
echo "3. Creative query:"
echo '   curl -X POST http://localhost:8080/api/chat \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"query": "Tell me about the future of computing"}'"'"
echo ""
echo "4. Check stats:"
echo '   curl http://localhost:8080/api/stats | jq .'
echo ""
echo "Server PID: $SERVER_PID"
echo "To stop: kill $SERVER_PID"
echo ""
echo "The LLM will:"
echo "- Generate novel responses by combining knowledge"
echo "- Cache responses for O(1) future access"
echo "- Show whether responses are from cache or generated"