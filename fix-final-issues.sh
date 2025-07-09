#!/bin/bash
echo "🔧 Final comprehensive fix for all remaining issues..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fix think-ai-utils/src/lib.rs - it has an extra closing brace, need to add missing }
echo -e "${GREEN}Fixing think-ai-utils/src/lib.rs...${NC}"
# Add missing closing brace for macro
echo "}" >> think-ai-utils/src/lib.rs

# Fix variable references in cache files
echo -e "${GREEN}Fixing cache variable references...${NC}"
# Fix triple underscore variables - simple replacements
sed -i 's/___hasher/hasher/g' think-ai-cache/src/lib.rs
sed -i 's/___bytes/bytes/g' think-ai-cache/src/lib.rs
sed -i 's/___cache/cache/g' think-ai-cache/src/lib.rs
sed -i 's/___value/value/g' think-ai-cache/src/lib.rs
sed -i 's/___retrieved/retrieved/g' think-ai-cache/src/lib.rs
sed -i 's/___data/data/g' think-ai-cache/src/lib.rs

# Fix image-gen variables
sed -i 's/___api_key/api_key/g' think-ai-image-gen/src/lib.rs
sed -i 's/___api_url/api_url/g' think-ai-image-gen/src/lib.rs
sed -i 's/___cache_dir/cache_dir/g' think-ai-image-gen/src/lib.rs
sed -i 's/___max_cache_gb/max_cache_gb/g' think-ai-image-gen/src/lib.rs
sed -i 's/___client/client/g' think-ai-image-gen/src/lib.rs
sed -i 's/___optimizer/optimizer/g' think-ai-image-gen/src/lib.rs
sed -i 's/___learner/learner/g' think-ai-image-gen/src/lib.rs
sed -i 's/___cache_key/cache_key/g' think-ai-image-gen/src/lib.rs
sed -i 's/___enhanced_prompt/enhanced_prompt/g' think-ai-image-gen/src/lib.rs
sed -i 's/___start_time/start_time/g' think-ai-image-gen/src/lib.rs
sed -i 's/___generation_time_ms/generation_time_ms/g' think-ai-image-gen/src/lib.rs
sed -i 's/___metadata/metadata/g' think-ai-image-gen/src/lib.rs
sed -i 's/___total_generations/total_generations/g' think-ai-image-gen/src/lib.rs
sed -i 's/___cache_stats/cache_stats/g' think-ai-image-gen/src/lib.rs
sed -i 's/___config/config/g' think-ai-image-gen/src/lib.rs
sed -i 's/___generator/generator/g' think-ai-image-gen/src/lib.rs

# Fix webapp variables
sed -i 's/___on_input/on_input/g' think-ai-webapp/src/ui/dashboard.rs
sed -i 's/___input/input/g' think-ai-webapp/src/ui/dashboard.rs
sed -i 's/___on_submit/on_submit/g' think-ai-webapp/src/ui/dashboard.rs
sed -i 's/___query_lower/query_lower/g' think-ai-webapp/src/lib.rs

# Fix vector variables
sed -i 's/___hash_tables/hash_tables/g' think-ai-vector/src/index/mod.rs
sed -i 's/___projections/projections/g' think-ai-vector/src/index/mod.rs

# Fix specific files with missing closing braces
echo -e "${GREEN}Adding missing closing braces...${NC}"

# Fix think-ai-webapp/src/ui/effects.rs
echo "    }" >> think-ai-webapp/src/ui/effects.rs
echo "}" >> think-ai-webapp/src/ui/effects.rs

# Fix think-ai-webapp/src/ui/dashboard.rs
echo "        }" >> think-ai-webapp/src/ui/dashboard.rs
echo "    }" >> think-ai-webapp/src/ui/dashboard.rs
echo "}" >> think-ai-webapp/src/ui/dashboard.rs
echo "}" >> think-ai-webapp/src/ui/dashboard.rs

# Fix think-ai-webapp/src/lib.rs
echo "        }" >> think-ai-webapp/src/lib.rs
echo "    }" >> think-ai-webapp/src/lib.rs
echo "}" >> think-ai-webapp/src/lib.rs

# Fix think-ai-qwen/src/client.rs
echo "        };" >> think-ai-qwen/src/client.rs
echo "    }" >> think-ai-qwen/src/client.rs
echo "}" >> think-ai-qwen/src/client.rs

# Fix think-ai-consciousness/src/lib.rs
echo "        }" >> think-ai-consciousness/src/lib.rs
echo "    }" >> think-ai-consciousness/src/lib.rs
echo "}" >> think-ai-consciousness/src/lib.rs

# Fix think-ai-cache/src/lib.rs
echo "        }" >> think-ai-cache/src/lib.rs
echo "    }" >> think-ai-cache/src/lib.rs
echo "}" >> think-ai-cache/src/lib.rs
echo "}" >> think-ai-cache/src/lib.rs
echo "}" >> think-ai-cache/src/lib.rs
echo "}" >> think-ai-cache/src/lib.rs

# Fix think-ai-storage/src/backends/memory.rs
sed -i 's/value___:/value:/g' think-ai-storage/src/backends/memory.rs
sed -i 's/key___:/key:/g' think-ai-storage/src/backends/memory.rs
echo "    }" >> think-ai-storage/src/backends/memory.rs
echo "}" >> think-ai-storage/src/backends/memory.rs

# Fix think-ai-image-gen/src/lib.rs
# Fix the test module
echo "        };" >> think-ai-image-gen/src/lib.rs
echo "    }" >> think-ai-image-gen/src/lib.rs
echo "}" >> think-ai-image-gen/src/lib.rs

# Fix cache variable reference
sed -i 's/_cache/cache/g' think-ai-image-gen/src/lib.rs

echo -e "${GREEN}✅ Final fixes complete!${NC}"
echo -e "${YELLOW}Running build to verify...${NC}"

# Try to build again
cd /home/champi/Dev/think_ai
cargo build --release 2>&1 | tee build-final-issues.log

# Check if build succeeded
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✅ BUILD SUCCESSFUL!${NC}"
    echo -e "${YELLOW}You can now run:${NC}"
    echo "  ./target/release/think-ai chat      # Interactive CLI"
    echo "  ./target/release/think-ai server    # HTTP server"
    echo "  ./target/release/think-ai-webapp    # Web interface"
    
    # List available binaries
    echo -e "\n${GREEN}Available binaries:${NC}"
    ls -la target/release/think-ai* | grep -v "\.d$" | grep -v "\.rlib$" | head -20
else
    echo -e "${RED}❌ Build still has errors. Check build-final-issues.log${NC}"
    echo -e "${YELLOW}Top remaining errors:${NC}"
    grep -E "error(\[E[0-9]+\])?:" build-final-issues.log | grep -v "error: could not compile" | head -15
fi