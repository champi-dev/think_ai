#!/bin/bash
set -e

echo "=== Final Production Build ==="
echo "Building all components except think-ai-image-gen..."
echo ""

# Build everything except image-gen
cargo build --release --workspace --exclude think-ai-image-gen 2>&1 | tail -100

echo ""
echo "=== Build Summary ==="
echo "Libraries built:"
ls -la target/release/*.rlib | grep think_ai | wc -l

echo ""
echo "Binaries available:"
ls -la target/release/think-ai* 2>/dev/null | grep -v "\\.d$" | grep -v "\\.rlib$" | head -20

echo ""
echo "Build complete!"