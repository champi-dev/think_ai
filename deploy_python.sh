#!/bin/bash
# Deploy Python package to PyPI

echo "🚀 Deploying think-ai-consciousness to PyPI..."

# Clean previous builds
rm -rf dist build *.egg-info

# Build the package
python -m build

# Upload to PyPI (uncomment when ready)
# python -m twine upload dist/*

echo "✅ Package built successfully!"
echo "📦 Built files:"
ls -la dist/

echo ""
echo "To upload to PyPI, run:"
echo "python -m twine upload dist/*"