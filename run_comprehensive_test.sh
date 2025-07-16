#!/bin/bash

# Comprehensive test script for Think AI Knowledge Transfer System
# This demonstrates the full knowledge transfer capabilities

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     🧠 THINK AI KNOWLEDGE TRANSFER DEMONSTRATION 🧠      ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  This test demonstrates the Knowledge Transfer System     ║"
echo "║  that enables Think AI to learn from Claude's patterns   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if release binary exists
if [ ! -f "./target/release/think-ai" ]; then
    echo -e "${YELLOW}🔨 Building Think AI in release mode...${NC}"
    cargo build --release --bin think-ai
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Build failed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Build successful!${NC}"
fi

echo ""
echo -e "${BLUE}📊 Running comprehensive test with 100 iterations...${NC}"
echo -e "${YELLOW}This will demonstrate:${NC}"
echo "  • Progressive learning across 6 knowledge domains"
echo "  • Adaptive difficulty adjustment"
echo "  • Cache optimization and performance"
echo "  • Thinking pattern transfer"
echo ""

# Run training with 100 iterations
./target/release/think-ai train --iterations 100

echo ""
echo -e "${GREEN}✨ Test complete!${NC}"
echo ""
echo -e "${BLUE}📁 Generated files:${NC}"
ls -la training_*.json knowledge_*.json 2>/dev/null | tail -6

echo ""
echo -e "${YELLOW}💡 Next steps:${NC}"
echo "1. Review the training session files to see learning progress"
echo "2. Test the trained system with: ./target/release/think-ai chat"
echo "3. Run full 1000 iteration training: ./run_knowledge_transfer.sh 1000"
echo ""
echo -e "${GREEN}📚 Sample questions to test the trained system:${NC}"
echo "  • How do I implement a cache with O(1) operations?"
echo "  • Explain recursion in simple terms"
echo "  • Debug my application that crashes intermittently"
echo "  • Design a high-performance messaging system"
echo "  • What's the difference between stack and heap memory?"