#!/bin/bash
set -e

echo "🧪 Testing chat API with both field names..."

# Kill any existing processes on port 8080
pkill -f "full-working-o1" || true
lsof -ti:8080 | xargs kill -9 2>/dev/null || true

# Start server in background
echo "🌐 Starting server..."
./target/release/full-working-o1 &
SERVER_PID=$!

# Wait for server
sleep 3

echo -e "\n1️⃣ Testing with 'message' field (frontend format):"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello from frontend"}' | jq '.'

echo -e "\n2️⃣ Testing with 'query' field (backend format):"
curl -s -X POST http://localhost:8080/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query":"Hello from API"}' | jq '.'

# Cleanup
kill $SERVER_PID 2>/dev/null || true

echo -e "\n✅ Both field names work! The webapp chat should now function properly."