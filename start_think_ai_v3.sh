#!/bin/bash
# Start Think AI v3.1.0 with webapp

echo "🚀 Starting Think AI v3.1.0 Full System..."

# Kill any existing processes
echo "Cleaning up existing processes..."
lsof -ti:8080 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Start API
echo "Starting API on port 8080..."
cd think_ai_v3
PORT=8080 THINK_AI_COLOMBIAN=true python app.py &
API_PID=$!

# Wait for API to start
echo "Waiting for API to initialize..."
sleep 10

# Start webapp
echo "Starting webapp on port 3000..."
cd ../webapp
NEXT_PUBLIC_API_URL=http://localhost:8080 npm start &
WEBAPP_PID=$!

echo ""
echo "✅ Think AI v3.1.0 is running!"
echo "   API: http://localhost:8080"
echo "   Webapp: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop"

# Wait and handle shutdown
trap "kill $API_PID $WEBAPP_PID 2>/dev/null; exit" INT
wait