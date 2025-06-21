#!/bin/bash
# Enable the fast pre-commit pipeline (<10s)

echo "🚀 Enabling Fast Pre-commit Pipeline..."

# Backup current config
if [ -f ".pre-commit-config.yaml" ]; then
    cp .pre-commit-config.yaml .pre-commit-config.yaml.bak
    echo "✅ Backed up current config to .pre-commit-config.yaml.bak"
fi

# Use fast config
cp .pre-commit-config-fast.yaml .pre-commit-config.yaml
echo "✅ Fast pipeline enabled"

# Install hooks
pre-commit install --install-hooks
echo "✅ Hooks installed"

echo ""
echo "⚡ Fast pipeline features:"
echo "  • Runs in <10s with aggressive caching"
echo "  • Non-blocking formatters"
echo "  • Parallel test execution"
echo "  • Coverage verification (70% threshold)"
echo "  • Lightweight build checks"
echo ""
echo "📦 To deploy libraries:"
echo "  pre-commit run deploy-libs --hook-stage manual"
echo "  # or directly: ./scripts/deploy-all-libs.sh"