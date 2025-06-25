#!/bin/bash
# Local testing script for Think AI v5.0

echo "🚀 Testing Think AI Locally"
echo "=========================="

# Generate random port based on UUID
PORT=$(python3 -c "import uuid; print(30000 + int(str(uuid.uuid4().int)[:4]))")
echo "📡 Using port: $PORT"

# 1. Start the server
echo "1️⃣ Starting server..."
PORT=$PORT python3 main.py &
SERVER_PID=$!
sleep 3

# 2. Test the API
echo -e "\n2️⃣ Testing API endpoints..."

# Health check
echo -e "\n📍 Health Check:"
curl -s http://localhost:$PORT/ | python3 -m json.tool

# Chat test
echo -e "\n💬 Chat Test:"
curl -s -X POST http://localhost:$PORT/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello AI"}' | python3 -m json.tool

# Multiple tests
echo -e "\n🔄 Multiple Chat Tests:"
for msg in "What is O(1)?" "Tell me a joke" "¿Hablas español?"; do
  echo -e "\n> $msg"
  curl -s -X POST http://localhost:$PORT/chat \
    -H "Content-Type: application/json" \
    -d "{\"message\": \"$msg\"}" | python3 -m json.tool
done

# 3. Stop server
echo -e "\n3️⃣ Stopping server..."
kill $SERVER_PID

echo -e "\n✅ Testing complete!"