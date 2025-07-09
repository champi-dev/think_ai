#!/bin/bash
echo "🔧 Fixing unclosed delimiter errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting delimiter fixes...${NC}"

# Function to check and fix delimiters in a file
check_delimiters() {
    local file=$1
    echo -e "${GREEN}Checking $file...${NC}"
    
    # Count opening and closing braces
    open_braces=$(grep -o '{' "$file" | wc -l)
    close_braces=$(grep -o '}' "$file" | wc -l)
    
    if [ "$open_braces" -ne "$close_braces" ]; then
        echo -e "${YELLOW}Found delimiter mismatch: $open_braces { vs $close_braces }${NC}"
        
        # Calculate how many closing braces we need
        missing=$((open_braces - close_braces))
        
        if [ "$missing" -gt 0 ]; then
            echo -e "${YELLOW}Adding $missing closing braces to $file${NC}"
            # Add missing closing braces at the end of the file
            for ((i=0; i<missing; i++)); do
                echo "}" >> "$file"
            done
        fi
    else
        echo -e "${GREEN}✓ Delimiters balanced${NC}"
    fi
}

# Fix specific files mentioned in errors
check_delimiters "think-ai-utils/src/lib.rs"
check_delimiters "think-ai-image-gen/src/lib.rs"
check_delimiters "think-ai-qwen/src/client.rs"

# Also check the perf.rs file mentioned in utils
if [ -f "think-ai-utils/src/perf.rs" ]; then
    check_delimiters "think-ai-utils/src/perf.rs"
fi

echo -e "${GREEN}✅ Delimiter fixes complete!${NC}"
echo -e "${YELLOW}Running build to verify...${NC}"

# Try to build again
cd /home/champi/Dev/think_ai
cargo build --release 2>&1 | tee build-delimiter-test.log

# Check if build succeeded
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful!${NC}"
else
    echo -e "${RED}❌ Build still has errors. Check build-delimiter-test.log${NC}"
    echo -e "${YELLOW}Remaining errors:${NC}"
    grep -E "error\[E[0-9]+\]:|error:" build-delimiter-test.log | head -20
fi