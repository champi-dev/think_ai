#!/bin/bash

# Think AI JavaScript Library - npm Publishing Script

set -e

echo "🚀 Publishing Think AI JavaScript Library to npm..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found. Run this script from the think-ai-js directory."
    exit 1
fi

# Verify that we have built the library
if [ ! -d "dist" ]; then
    echo "📦 Building library..."
    npm run build
fi

# Verify build artifacts exist
if [ ! -f "dist/index.js" ] || [ ! -f "dist/cli.js" ]; then
    echo "❌ Error: Build artifacts missing. Please run 'npm run build' first."
    exit 1
fi

# Show current version
CURRENT_VERSION=$(node -p "require('./package.json').version")
echo "📋 Current version: $CURRENT_VERSION"

# Test the CLI to ensure it works
echo "🧪 Testing CLI..."
if ! node dist/cli.js --help > /dev/null; then
    echo "❌ Error: CLI test failed"
    exit 1
fi

echo "✅ CLI test passed"

# Check if already published  
PACKAGE_NAME=$(node -p "require('./package.json').name")
if npm view $PACKAGE_NAME@$CURRENT_VERSION > /dev/null 2>&1; then
    echo "⚠️  Version $CURRENT_VERSION already exists on npm"
    echo "💡 Consider updating the version in package.json"
    exit 1
fi

# Publish to npm
echo "📤 Publishing to npm..."
npm publish

echo "✅ Successfully published $PACKAGE_NAME@$CURRENT_VERSION to npm!"
echo ""
echo "📦 Users can now install with:"
echo "   npm install $PACKAGE_NAME"
echo ""
echo "🎉 Think AI JavaScript library is now available to all users!"