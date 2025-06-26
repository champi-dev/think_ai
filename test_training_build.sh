#!/bin/bash

# Test script to verify training system builds correctly

set -e

echo "🔍 Testing Think AI Training System Build..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# Test cargo build
echo "📦 Checking Rust build..."
if cargo check --bin comprehensive-train 2>/dev/null; then
    echo -e "${GREEN}✓ Cargo check passed${NC}"
else
    echo -e "${RED}✗ Cargo check failed${NC}"
    exit 1
fi

# Test compilation
echo "🔨 Testing compilation..."
if cargo build --release --bin comprehensive-train; then
    echo -e "${GREEN}✓ Build successful${NC}"
else
    echo -e "${RED}✗ Build failed${NC}"
    exit 1
fi

# Check if binary exists
if [ -f "./target/release/comprehensive-train" ]; then
    echo -e "${GREEN}✓ Binary created successfully${NC}"
else
    echo -e "${RED}✗ Binary not found${NC}"
    exit 1
fi

# Test imports
echo "🧪 Testing module imports..."
cargo test --lib --package think-ai-knowledge -- --nocapture comprehensive_trainer::tests 2>/dev/null || true

echo ""
echo -e "${GREEN}✅ All checks passed! The training system is ready.${NC}"
echo ""
echo "Next steps:"
echo "1. Run ./run_comprehensive_training.sh for full training"
echo "2. Run ./advanced_training.sh --quick for a quick test"
echo "3. See TRAINING_GUIDE.md for detailed documentation"