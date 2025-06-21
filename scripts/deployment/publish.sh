#!/bin/bash

# Script to publish all libraries

echo "🚀 Publishing Think AI Libraries"
echo "================================"

# Python Package
echo ""
echo "📦 Building Python Package..."
cd think-ai-cli/python

# Clean previous builds
rm -rf dist build *.egg-info

# Build package
python -m build

echo "✅ Python package built"
echo "📤 To publish to PyPI, run:"
echo "   python -m twine upload dist/*"

# Node.js Package
echo ""
echo "📦 Building Node.js Package..."
cd ../nodejs

# Install dependencies
npm install

# Build TypeScript
npm run build

echo "✅ Node.js package built"
echo "📤 To publish to npm, run:"
echo "   npm publish"

# Docker Image
echo ""
echo "🐳 Building Docker Image..."
cd ../..

# Build compressed Docker image
docker build -f Dockerfile.compressed -t think-ai:latest .
docker tag think-ai:latest think-ai:v0.2.0

echo "✅ Docker image built"
echo "📤 To publish to Docker Hub:"
echo "   docker tag think-ai:latest yourusername/think-ai:latest"
echo "   docker push yourusername/think-ai:latest"

# Create release archive
echo ""
echo "📁 Creating Release Archive..."
mkdir -p releases
tar -czf releases/think-ai-v0.2.0.tar.gz \
  --exclude=node_modules \
  --exclude=__pycache__ \
  --exclude=.git \
  --exclude=venv \
  --exclude=dist \
  --exclude=build \
  .

echo ""
echo "✅ All packages ready for deployment!"
echo ""
echo "📋 Summary:"
echo "  • Python wheel: think-ai-cli/python/dist/think_ai_cli-0.2.0-py3-none-any.whl"
echo "  • Node.js package: think-ai-cli/nodejs/"
echo "  • Docker image: think-ai:v0.2.0"
echo "  • Release archive: releases/think-ai-v0.2.0.tar.gz"
echo ""
echo "🌐 For Vercel deployment:"
echo "  • Push to GitHub"
echo "  • Vercel will auto-deploy from main branch"
echo "  • Uses requirements-no-faiss.txt automatically"