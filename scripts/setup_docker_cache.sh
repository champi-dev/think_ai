#!/bin/bash
# Setup Docker caching for faster builds

echo "🚀 Setting up Docker caching for faster builds..."
echo "=============================================="

# Enable BuildKit globally
echo "export DOCKER_BUILDKIT=1" >> ~/.bashrc
echo "export COMPOSE_DOCKER_CLI_BUILD=1" >> ~/.bashrc

# Create Docker daemon config for better caching
DOCKER_CONFIG_DIR="$HOME/.docker"
mkdir -p "$DOCKER_CONFIG_DIR"

cat > "$DOCKER_CONFIG_DIR/daemon.json" << EOF
{
  "features": {
    "buildkit": true
  },
  "builder": {
    "gc": {
      "defaultKeepStorage": "20GB",
      "enabled": true
    }
  },
  "registry-mirrors": [],
  "insecure-registries": [],
  "debug": false,
  "experimental": true
}
EOF

echo "✅ Docker BuildKit enabled globally"
echo ""
echo "🐳 Creating Docker build cache volume..."
docker volume create think-ai-build-cache 2>/dev/null || true

echo ""
echo "📝 Usage tips for faster builds:"
echo "  1. BuildKit is now enabled by default"
echo "  2. Use --cache-from and --cache-to flags"
echo "  3. Example:"
echo "     docker build --cache-from=type=local,src=/tmp/docker-cache \\"
echo "                  --cache-to=type=local,dest=/tmp/docker-cache \\"
echo "                  -t myimage ."
echo ""
echo "✅ Docker caching setup complete!"
echo "   Restart your terminal or run: source ~/.bashrc"