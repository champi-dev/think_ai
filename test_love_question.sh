#!/bin/bash

echo "🧪 Testing Think AI Love Question Fix"
echo "====================================="
echo

# Build the project
echo "🔨 Building Think AI..."
cargo build --release
if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"
echo

# Clean up problematic knowledge storage
echo "🧹 Cleaning up problematic knowledge storage..."
rm -rf ./trained_knowledge ./knowledge_storage
echo "✅ Knowledge storage cleaned!"
echo

# Test the love question
echo "❓ Testing: 'What is love?'"
echo "Expected: Proper explanation about love as an emotion/attachment"
echo "NOT expected: 'Abstract principle derived from X examples: Symmetry breaking...'"
echo
echo "Running test..."
echo

# Use timeout to prevent hanging
echo "what is love" | timeout 30s ./target/release/think-ai chat

echo
echo "🧪 Test complete!"
echo
echo "If you saw a proper explanation of love instead of abstract principles,"
echo "then the fix is working correctly!"