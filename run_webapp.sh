#!/bin/bash
# Run Think AI webapp with Python API server

echo "🚀 Starting Think AI Webapp with Python API Server..."

# Check if docker-compose services are running
if ! docker-compose ps | grep -q "Up"; then
    echo "📦 Starting Docker services..."
    docker-compose up -d
    sleep 5
fi

# Start background service
echo "🧠 Starting Think AI background service..."
python3 -m think_ai.core.background_service &
BACKGROUND_PID=$!
echo "Background service PID: $BACKGROUND_PID"

# Start Python API server
echo "🌐 Starting Python API server on port 8080..."
python3 api_server.py &
API_PID=$!
echo "API server PID: $API_PID"

# Wait for API server to be ready
echo "⏳ Waiting for API server to start..."
for i in {1..30}; do
    if curl -s http://localhost:8080/api/v1/health > /dev/null; then
        echo "✅ API server is ready!"
        break
    fi
    sleep 1
done

# Start webapp
echo "🎨 Starting webapp on port 3000..."
cd webapp
npm run dev &
WEBAPP_PID=$!
echo "Webapp PID: $WEBAPP_PID"

echo ""
echo "✨ All services started!"
echo "📱 Webapp: http://localhost:3000"
echo "🔌 API Server: http://localhost:8080"
echo "🩺 Health Check: http://localhost:8080/api/v1/health"
echo ""
echo "Press Ctrl+C to stop all services..."

# Function to clean up on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $WEBAPP_PID 2>/dev/null
    kill $API_PID 2>/dev/null
    kill $BACKGROUND_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup INT

# Wait for all background processes
wait