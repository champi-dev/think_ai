#!/bin/bash

# Think AI Comprehensive Training Script
# This script trains Think AI to be a powerful, useful tool and natural conversationalist

set -e  # Exit on error

echo "🤖 Think AI Comprehensive Training System"
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "Cargo.toml" ]; then
    echo -e "${RED}Error: Must be run from the think_ai root directory${NC}"
    exit 1
fi

# Build the project in release mode for optimal performance
echo -e "${BLUE}🔨 Building Think AI in release mode...${NC}"
cargo build --release --bin comprehensive-train

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Build failed! Please fix compilation errors.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Build successful!${NC}"
echo ""

# Create knowledge directory if it doesn't exist
mkdir -p knowledge_data

# Run the comprehensive training
echo -e "${YELLOW}🚀 Starting comprehensive training...${NC}"
echo -e "${YELLOW}This will train Think AI with:${NC}"
echo -e "${YELLOW}  • 1,000 iterations for tool capabilities${NC}"
echo -e "${YELLOW}  • 1,000 iterations for conversational abilities${NC}"
echo -e "${YELLOW}  • Self-improvement optimization${NC}"
echo ""

# Set the knowledge file path
export KNOWLEDGE_PATH="knowledge_data/comprehensive_knowledge.json"

# Run the training
./target/release/comprehensive-train

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 Training completed successfully!${NC}"
    echo -e "${GREEN}Knowledge base saved to: knowledge_data/comprehensive_knowledge.json${NC}"
    echo ""
    echo -e "${BLUE}📊 Next steps:${NC}"
    echo -e "${BLUE}1. Run './target/release/think-ai chat' to test the enhanced AI${NC}"
    echo -e "${BLUE}2. Check knowledge_data/ for the trained knowledge base${NC}"
    echo -e "${BLUE}3. Use the API server to integrate with applications${NC}"
else
    echo -e "${RED}❌ Training failed! Check the error messages above.${NC}"
    exit 1
fi