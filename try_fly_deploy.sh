#!/bin/bash

echo "🚁 Alternative Deployment: Fly.io"
echo "================================="

echo ""
echo "🔧 Railway CLI having issues? Try Fly.io instead!"
echo ""

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "📦 Installing Fly.io CLI..."
    curl -L https://fly.io/install.sh | sh
    export PATH="$HOME/.fly/bin:$PATH"
    echo "✅ Fly CLI installed"
else
    echo "✅ Fly CLI already installed"
fi

echo ""
echo "🛠️ Setting up Fly.io deployment..."

# Create fly.toml configuration
cat > fly.toml << 'EOF'
app = "think-ai-quantum"
primary_region = "iad"

[build]
  dockerfile = "Dockerfile"

[http_service]
  internal_port = 8080
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0
  processes = ["app"]

[[http_service.checks]]
  interval = "10s"
  grace_period = "5s"
  method = "GET"
  path = "/health"
  protocol = "http"
  timeout = "2s"

[env]
  PORT = "8080"
  RUST_LOG = "info"

[[vm]]
  cpu_kind = "shared"
  cpus = 1
  memory_mb = 512
EOF

echo "✅ Created fly.toml configuration"

echo ""
echo "🚀 Deploy to Fly.io:"
echo "==================="
echo "1. flyctl auth login"
echo "2. flyctl launch --no-deploy"
echo "3. flyctl deploy"
echo ""
echo "📝 Or run this script:"
echo "./try_fly_deploy.sh"
echo ""
echo "🌐 Your app will be available at:"
echo "https://think-ai-quantum.fly.dev"
echo ""
echo "✨ Features that will be deployed:"
echo "• Clean UI with 3D quantum animation"
echo "• O(1) performance optimizations"
echo "• Hierarchical knowledge system"
echo "• Health monitoring at /health"