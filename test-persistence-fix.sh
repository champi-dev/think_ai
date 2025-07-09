#!/bin/bash

echo "Testing persistence.rs fix..."
echo "==============================="
echo ""

# Change to the project directory
cd /home/champi/Dev/think_ai

# Try to build the knowledge crate specifically
echo "Building think-ai-knowledge crate..."
cargo build --package think-ai-knowledge 2>&1 | head -20

# Check if the build was successful
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "✅ Build successful! All unclosed delimiter errors have been fixed."
else
    echo ""
    echo "❌ Build failed. There might be other errors to fix."
fi

# Run clippy to check for any warnings
echo ""
echo "Running clippy on think-ai-knowledge..."
cargo clippy --package think-ai-knowledge --no-deps 2>&1 | head -20

echo ""
echo "Test complete!"