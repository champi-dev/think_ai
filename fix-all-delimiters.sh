#!/bin/bash
echo "🔧 Fixing all delimiter errors across the codebase..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check and fix delimiters in a file
check_and_fix_delimiters() {
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

# Fix all files mentioned in the errors
echo -e "${YELLOW}Fixing delimiter errors in all affected files...${NC}"

# Files from the error messages
files=(
    "think-ai-consciousness/src/lib.rs"
    "think-ai-vector/src/index/mod.rs"
    "think-ai-cache/src/lib.rs"
    "think-ai-image-gen/src/lib.rs"
    "think-ai-storage/src/backends/memory.rs"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        check_and_fix_delimiters "$file"
    else
        echo -e "${RED}File not found: $file${NC}"
    fi
done

# Also check any other files that might have issues
echo -e "${YELLOW}Checking for other files with delimiter issues...${NC}"

# Find all Rust files and check for delimiter issues
find . -name "*.rs" -type f | while read -r file; do
    # Skip target and git directories
    if [[ "$file" == *"/target/"* ]] || [[ "$file" == *"/.git/"* ]]; then
        continue
    fi
    
    # Quick check for obvious issues
    open_braces=$(grep -o '{' "$file" 2>/dev/null | wc -l)
    close_braces=$(grep -o '}' "$file" 2>/dev/null | wc -l)
    
    if [ "$open_braces" -ne "$close_braces" ] && [ "$open_braces" -gt 0 ]; then
        echo -e "${YELLOW}Found potential issue in: $file${NC}"
        check_and_fix_delimiters "$file"
    fi
done

echo -e "${GREEN}✅ Delimiter fixes complete!${NC}"
echo -e "${YELLOW}Running build to verify...${NC}"

# Try to build again
cd /home/champi/Dev/think_ai
cargo build --release 2>&1 | tee build-delimiter-fix.log

# Check if build succeeded
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✅ BUILD SUCCESSFUL!${NC}"
    echo -e "${YELLOW}You can now run:${NC}"
    echo "  ./target/release/think-ai chat      # Interactive CLI"
    echo "  ./target/release/think-ai server    # HTTP server"
    echo "  ./target/release/think-ai-webapp    # Web interface"
    
    # List all built binaries
    echo -e "\n${GREEN}Available binaries:${NC}"
    ls -la target/release/think-ai* | grep -v "\.d$" | grep -v "\.rlib$" | head -20
else
    echo -e "${RED}❌ Build still has errors. Check build-delimiter-fix.log${NC}"
    echo -e "${YELLOW}Next errors to fix:${NC}"
    grep -E "error\[E[0-9]+\]:|error:" build-delimiter-fix.log | head -10
fi