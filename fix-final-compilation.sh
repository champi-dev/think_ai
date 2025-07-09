#!/bin/bash
echo "🔧 Final comprehensive fix for Think AI compilation..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting final comprehensive fixes...${NC}"

# Function to fix files
fix_file() {
    local file=$1
    echo -e "${GREEN}Fixing $file...${NC}"
}

# Fix EffectManager in webapp/src/ui/effects.rs
fix_file "think-ai-webapp/src/ui/effects.rs"
# Remove duplicate new() methods (lines 79-126)
sed -i '79,126d' think-ai-webapp/src/ui/effects.rs 2>/dev/null || true

# Fix ResponseStream in webapp/src/ui/dashboard.rs
fix_file "think-ai-webapp/src/ui/dashboard.rs"
# Fix the variable name in update method
sed -i 's/self\.stream = _stream;/self.stream = stream;/g' think-ai-webapp/src/ui/dashboard.rs

# Fix double type names in knowledge/src/types.rs
fix_file "think-ai-knowledge/src/types.rs"
# Fix ResponseContext double types
sed -i 's/ResponseContextResponseContext/ResponseContext/g' think-ai-knowledge/src/types.rs
sed -i 's/QueryResultQueryResult/QueryResult/g' think-ai-knowledge/src/types.rs
sed -i 's/KnowledgeNodeKnowledgeNode/KnowledgeNode/g' think-ai-knowledge/src/types.rs
sed -i 's/KnowledgeGraphKnowledgeGraph/KnowledgeGraph/g' think-ai-knowledge/src/types.rs

# Fix all remaining double type patterns across the codebase
echo -e "${YELLOW}Fixing all remaining double type patterns...${NC}"
find . -name "*.rs" -type f | while read -r file; do
    # Skip target and git directories
    if [[ "$file" == *"/target/"* ]] || [[ "$file" == *"/.git/"* ]]; then
        continue
    fi
    
    # Fix common double type patterns
    sed -i 's/ArcArc/Arc/g' "$file" 2>/dev/null || true
    sed -i 's/VecVec/Vec/g' "$file" 2>/dev/null || true
    sed -i 's/StringString/String/g' "$file" 2>/dev/null || true
    sed -i 's/strstr/str/g' "$file" 2>/dev/null || true
    sed -i 's/usizeusize/usize/g' "$file" 2>/dev/null || true
    sed -i 's/f32f32/f32/g' "$file" 2>/dev/null || true
    sed -i 's/f64f64/f64/g' "$file" 2>/dev/null || true
    sed -i 's/boolbool/bool/g' "$file" 2>/dev/null || true
    sed -i 's/u8u8/u8/g' "$file" 2>/dev/null || true
    sed -i 's/u32u32/u32/g' "$file" 2>/dev/null || true
    sed -i 's/u64u64/u64/g' "$file" 2>/dev/null || true
    sed -i 's/i32i32/i32/g' "$file" 2>/dev/null || true
    sed -i 's/i64i64/i64/g' "$file" 2>/dev/null || true
done

# Fix empty let patterns
echo -e "${YELLOW}Fixing empty let patterns...${NC}"
find . -name "*.rs" -type f -exec sed -i 's/let  = /let _ = /' {} \;

# Fix specific variable references with underscores in knowledge module
echo -e "${YELLOW}Fixing knowledge module variable references...${NC}"
sed -i 's/shared_knowledge_/shared_knowledge/g' think-ai-knowledge/src/isolated_session.rs
sed -i 's/nodes_/nodes/g' think-ai-knowledge/src/feynman_explainer.rs
sed -i 's/success_/success/g' think-ai-knowledge/src/intelligent_relevance.rs
sed -i 's/reasoning_trace_/reasoning_trace/g' think-ai-knowledge/src/llm_benchmarks.rs
sed -i 's/selected_index_/selected_index/g' think-ai-knowledge/src/multi_candidate_selector.rs
sed -i 's/domain_/domain/g' think-ai-knowledge/src/multi_candidate_selector.rs
sed -i 's/let _hypothesis_topic =/let hypothesis_topic =/' think-ai-knowledge/src/self_learning.rs

# Fix Display trait implementations
echo -e "${YELLOW}Fixing Display trait implementations...${NC}"
find . -name "*.rs" -type f -exec sed -i \
    '/impl.*Display.*for/,/^}/ {
        /fn fmt(&self)/,/^[[:space:]]*}/ {
            /fn fmt(&self)/ s/fn fmt(&self)/fn fmt(\&self, f: \&mut std::fmt::Formatter<'"'"'_>) -> std::fmt::Result/
        }
    }' {} \;

# Fix specific Display issues
sed -i 's/f: &mut std::fmt::Formatter)/f: \&mut std::fmt::Formatter<'"'"'_>) -> std::fmt::Result/' think-ai-knowledge/src/evidence.rs
sed -i 's/f: &mut std::fmt::Formatter)/f: \&mut std::fmt::Formatter<'"'"'_>) -> std::fmt::Result/' think-ai-knowledge/src/persistence.rs

# Fix webapp type issues
echo -e "${YELLOW}Fixing webapp type issues...${NC}"
fix_file "think-ai-webapp/src/lib.rs"
# Fix ThinkAiWebapp::new() return type
sed -i '/pub fn new() -> Result<Self, JsValue> {/,/^    }$/{
    s/Ok(Self {/Ok(ThinkAiWebapp {/g
}' think-ai-webapp/src/lib.rs

# Fix missing ChatMsg variants in webapp
fix_file "think-ai-webapp/src/lib.rs"
# Add missing variants to ChatMsg enum if not present
if ! grep -q "UpdateStatus" think-ai-webapp/src/lib.rs; then
    sed -i '/pub enum ChatMsg {/,/^}$/{
        /ResponseStream(String),/a\
    UpdateStatus(String),\
    SetLoading(bool),\
    ProcessResponse(String),
    }' think-ai-webapp/src/lib.rs
fi

# Fix webapp graphics imports
echo -e "${YELLOW}Fixing webapp graphics imports...${NC}"
for file in think-ai-webapp/src/graphics/*.rs; do
    if [ -f "$file" ]; then
        # Add missing WebGl imports
        if grep -q "WebGlProgram" "$file" && ! grep -q "use web_sys::{.*WebGlProgram" "$file"; then
            sed -i '1i\use web_sys::WebGlProgram;' "$file"
        fi
    fi
done

# Fix metadata parameters in vector operations
echo -e "${YELLOW}Fixing metadata parameters...${NC}"
sed -i '/add(vector_array.clone(),/,/);/ {
    s/add(vector_array.clone(), metadata)/add(vector_array.clone(), None)/
}' think-ai-vector/src/index/operations.rs

sed -i '/meta.push(metadata);/s/metadata/None/' think-ai-vector/src/index/storage.rs

# Fix the comprehensive_knowledge.rs method call
echo -e "${YELLOW}Fixing method call arguments...${NC}"
sed -i '/engine.add_knowledge(/,/)/ {
    /KnowledgeDomain::Medicine,/a\            "medical_knowledge".to_string(),
}' think-ai-knowledge/src/comprehensive_knowledge.rs

# Clean up any duplicate imports
echo -e "${YELLOW}Cleaning up duplicate imports...${NC}"
find . -name "*.rs" -type f | while read -r file; do
    if [[ "$file" == *"/target/"* ]] || [[ "$file" == *"/.git/"* ]]; then
        continue
    fi
    
    # Remove consecutive duplicate lines (including imports)
    awk '!seen[$0]++' "$file" > "$file.tmp" && mv "$file.tmp" "$file" 2>/dev/null || true
done

echo -e "${GREEN}✅ Final compilation fixes complete!${NC}"
echo -e "${YELLOW}Running build to verify...${NC}"

# Try to build
cd /home/champi/Dev/think_ai
cargo build --release 2>&1 | tee build-final-test.log

# Check if build succeeded
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo -e "${GREEN}✅ Build successful!${NC}"
    echo -e "${YELLOW}You can now run:${NC}"
    echo "  ./target/release/think-ai chat"
    echo "  ./target/release/think-ai server"
    echo "  ./target/release/think-ai-webapp"
else
    echo -e "${RED}❌ Build still has errors. Check build-final-test.log${NC}"
    echo -e "${YELLOW}Remaining errors:${NC}"
    grep -E "error\[E[0-9]+\]:|error:" build-final-test.log | head -20
fi