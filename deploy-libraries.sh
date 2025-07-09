#!/bin/bash
set -e

echo "🚀 Deploying Think AI libraries..."

# Check for required tools
command -v npm >/dev/null 2>&1 || { echo "npm is required but not installed."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "python3 is required but not installed."; exit 1; }
command -v twine >/dev/null 2>&1 || { echo "twine is required but not installed. Run: pip install twine"; exit 1; }

# Build Rust libraries first
echo "🔨 Building Rust libraries..."
cargo build --release

# Deploy npm package
echo "📦 Deploying to npm..."
cd think-ai-js
npm version patch
npm publish
cd ..

# Deploy Python package
echo "🐍 Deploying to PyPI..."
cd think-ai-py
python3 setup.py sdist bdist_wheel
twine upload dist/*
cd ..

echo "✅ Libraries deployed successfully!"
