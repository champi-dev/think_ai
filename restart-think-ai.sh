#\!/bin/bash
set -e

echo "🔄 Restarting Think AI Service..."

# Kill the old process
echo "Stopping old service (PID 200375)..."
kill -TERM 200375
sleep 2

# Make sure it's stopped
if kill -0 200375 2>/dev/null; then
    echo "Force stopping..."
    kill -KILL 200375
fi

# Start the new service
echo "Starting new service..."
cd /home/administrator/think_ai

# Use the latest built binary
if [ -f "./target/release/railway-server" ]; then
    echo "Using railway-server binary..."
    PORT=8080 ./target/release/railway-server &
elif [ -f "./target/release/full-working-o1" ]; then
    echo "Using full-working-o1 binary..."
    PORT=8080 ./target/release/full-working-o1 &
else
    echo "Error: No suitable binary found\!"
    exit 1
fi

NEW_PID=$\!
echo "New service started with PID: $NEW_PID"

# Wait for service to start
sleep 3

# Verify it's running
if lsof -i :8080  < /dev/null |  grep -q LISTEN; then
    echo "✅ Service successfully restarted on port 8080"
    echo "🌐 Accessible via:"
    echo "  - https://thinkai.lat (ngrok)"
    echo "  - cloudflared tunnel"
else
    echo "❌ Service failed to start on port 8080"
    exit 1
fi

echo ""
echo "✅ Think AI service restarted successfully!"
echo "PID: $NEW_PID"
