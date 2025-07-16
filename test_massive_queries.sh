#!/bin/bash

# E2E Test Script for 50k Token Handling with GPU Support
echo "🧪 Think AI - Massive Query E2E Test Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check GPU availability
echo -e "${YELLOW}📊 Checking GPU availability...${NC}"
if command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}✅ NVIDIA GPU detected${NC}"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo -e "${GREEN}✅ macOS detected - checking for Metal GPU${NC}"
    system_profiler SPDisplaysDataType | grep "Chipset Model" || echo "Apple Silicon GPU"
else
    echo -e "${YELLOW}⚠️  No GPU detected - will use CPU${NC}"
fi
echo ""

# Step 2: Create test binary entry in Cargo.toml
echo -e "${YELLOW}📝 Setting up test binary...${NC}"
# Check if the binary entry already exists
if ! grep -q "name = \"test_massive_queries\"" think-ai-core/Cargo.toml; then
    # Add the test binary to Cargo.toml
    cat >> think-ai-core/Cargo.toml << 'EOF'

[[bin]]
name = "test_massive_queries"
path = "../test_massive_queries.rs"
EOF
    echo -e "${GREEN}✅ Added test binary to Cargo.toml${NC}"
else
    echo -e "${GREEN}✅ Test binary already configured${NC}"
fi

# Step 3: Build the test
echo ""
echo -e "${YELLOW}🔨 Building test in release mode...${NC}"
cd think-ai-core
cargo build --release --bin test_massive_queries
BUILD_STATUS=$?

if [ $BUILD_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful${NC}"
else
    echo -e "${RED}❌ Build failed${NC}"
    exit 1
fi

# Step 4: Run the test
echo ""
echo -e "${YELLOW}🚀 Running massive query test...${NC}"
echo "================================"
echo ""

# Set reasonable memory limits
export RUST_MIN_STACK=8388608  # 8MB stack
export RUST_BACKTRACE=1

# Run with timing
time ../target/release/test_massive_queries

TEST_STATUS=$?

echo ""
echo "================================"
if [ $TEST_STATUS -eq 0 ]; then
    echo -e "${GREEN}✅ All tests completed successfully!${NC}"
    echo ""
    echo "Key achievements:"
    echo "- ✅ 50k token limit configured"
    echo "- ✅ GPU detection and usage when available"
    echo "- ✅ Streaming support for massive queries"
    echo "- ✅ Concurrent query handling"
    echo "- ✅ No hanging on massive queries"
else
    echo -e "${RED}❌ Test failed with exit code: $TEST_STATUS${NC}"
fi

# Step 5: Check memory usage
echo ""
echo -e "${YELLOW}📊 System resource check:${NC}"
if command -v free &> /dev/null; then
    free -h | grep -E "^Mem|^Swap"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    vm_stat | grep -E "Pages free|Pages active"
fi

echo ""
echo "Test complete!"