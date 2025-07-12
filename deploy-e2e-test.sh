#\!/bin/bash
set -e

echo "🚀 Deploying Think AI E2E Test..."

# Build the release binary
echo "📦 Building release binary..."
cargo build --release --bin railway-server

# Create a deployment package
echo "📦 Creating deployment package..."
mkdir -p deploy-package
cp target/release/railway-server deploy-package/
cp Dockerfile deploy-package/
cp nixpacks.toml deploy-package/

# Run the server locally first for testing
echo "🧪 Testing server locally on port 3456..."
PORT=3456 ./target/release/railway-server &
SERVER_PID=$\!

# Wait for server to start
sleep 3

# Test the server
echo "✅ Testing local server..."
curl -s http://localhost:3456/health || echo "Health check failed"

# Kill the test server
kill $SERVER_PID

echo "
✅ Build complete\! 

To deploy to Railway:
1. Login to Railway dashboard at https://railway.app
2. Use the Railway GitHub integration to deploy
3. The site will be available at https://thinkai.lat

For manual deployment:
- Binary is at: ./target/release/railway-server
- Ensure PORT environment variable is set
- The server listens on port 8080 by default
"
