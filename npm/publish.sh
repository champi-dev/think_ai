#!/bin/bash

echo "🚀 Publishing Think AI to NPM"
echo "============================"

# Check if logged in to npm
echo "Checking npm login..."
npm whoami &> /dev/null
if [ $? -ne 0 ]; then
    echo "❌ Not logged in to npm. Please run: npm login"
    exit 1
fi

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/

# Install dependencies
echo "Installing dependencies..."
npm install

# Build TypeScript
echo "Building TypeScript..."
npm run build

# Run tests if they exist
if [ -f "jest.config.js" ]; then
    echo "Running tests..."
    npm test
fi

# Publish
echo "Publishing to npm..."
npm publish --access public

if [ $? -eq 0 ]; then
    echo "✅ Successfully published think-ai-consciousness to npm!"
    echo "Install with: npm install think-ai-consciousness"
else
    echo "❌ Failed to publish to npm"
    exit 1
fi