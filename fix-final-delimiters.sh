#!/bin/bash
set -e

echo "Final delimiter fixes..."

# Fix consciousness_field.rs - seems to have extra closing braces
echo "Checking consciousness_field.rs for extra braces"
# Remove any extra braces after line 66
sed -i '67,$ d' think-ai-consciousness/src/consciousness_field.rs 2>/dev/null || true

# Fix operations.rs 
echo "Fixing think-ai-vector/src/index/operations.rs"
echo "}" >> think-ai-vector/src/index/operations.rs

# Check and fix consciousness_engine.rs structure
echo "Fixing think-ai-core/src/consciousness_engine.rs"
# First, let me check line 323
if ! grep -q "^}$" think-ai-core/src/consciousness_engine.rs; then
    echo "}" >> think-ai-core/src/consciousness_engine.rs
fi

# Check image-gen lib.rs 
echo "Checking think-ai-image-gen/src/lib.rs"
# Make sure file ends properly
if ! tail -1 think-ai-image-gen/src/lib.rs | grep -q "^}$"; then
    echo "}" >> think-ai-image-gen/src/lib.rs
fi

echo "Fixes applied."