#!/bin/bash
echo "🔧 Fixing last two compilation errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fix think-ai-utils/src/perf.rs - missing semicolon
echo -e "${GREEN}Fixing think-ai-utils/src/perf.rs...${NC}"
sed -i '15s/$/;/' think-ai-utils/src/perf.rs

# Fix think-ai-image-gen/src/lib.rs - broken test function
echo -e "${GREEN}Fixing think-ai-image-gen/src/lib.rs test function...${NC}"
# First, let's look at what we have
echo -e "${YELLOW}Current test function state:${NC}"
tail -n 20 think-ai-image-gen/src/lib.rs

# Now fix it properly
cat > think-ai-image-gen/src/lib.rs.fix << 'EOF'
        };
        let request2 = request1.clone();
        let key1 = generator.generate_cache_key(&request1);
        let key2 = generator.generate_cache_key(&request2);
        assert_eq!(key1, key2, "Same requests should generate same cache keys");
    }
}
EOF

# Replace the broken test with the fixed version
head -n 237 think-ai-image-gen/src/lib.rs > think-ai-image-gen/src/lib.rs.tmp
cat think-ai-image-gen/src/lib.rs.fix >> think-ai-image-gen/src/lib.rs.tmp
mv think-ai-image-gen/src/lib.rs.tmp think-ai-image-gen/src/lib.rs

# Clean up
rm -f think-ai-image-gen/src/lib.rs.fix

echo -e "${GREEN}✅ Final fixes complete!${NC}"
echo -e "${YELLOW}Running build to verify...${NC}"

# Try to build again
cd /home/champi/Dev/think_ai
cargo build --release 2>&1 | tee build-final-final.log

# Check if build succeeded
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful!${NC}"
    echo -e "${YELLOW}You can now run:${NC}"
    echo "  ./target/release/think-ai chat"
    echo "  ./target/release/think-ai server"
    echo "  ./target/release/think-ai-webapp"
else
    echo -e "${RED}❌ Build still has errors. Check build-final-final.log${NC}"
    echo -e "${YELLOW}Remaining errors:${NC}"
    grep -E "error\[E[0-9]+\]:|error:" build-final-final.log | head -10
fi