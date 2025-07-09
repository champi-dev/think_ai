#!/bin/bash

echo "🔧 Fixing all remaining Think AI compilation errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to fix knowledge module underscore variables
fix_knowledge_underscores() {
    echo -e "${YELLOW}Fixing knowledge module underscore variable references...${NC}"
    
    # Fix all underscore parameter references in knowledge module
    find think-ai-knowledge -name "*.rs" -type f | while read -r file; do
        # Remove underscores from parameter names where they're being used
        sed -i 's/pub fn new(_engine:/pub fn new(engine:/g' "$file"
        sed -i 's/fn new(_engine:/fn new(engine:/g' "$file"
        
        # Fix double underscores in variable names
        sed -i 's/knowledge__engine/knowledge_engine/g' "$file"
        sed -i 's/from__context/from_context/g' "$file"
        sed -i 's/to__context/to_context/g' "$file"
        
        # Fix all _variable patterns where the variable is referenced without underscore
        perl -i -pe 's/(\w+)\s*:\s*&mut\s+_(\w+)/\1: \&mut \2/g' "$file"
        perl -i -pe 's/(\w+)\s*:\s*_(\w+)/\1: \2/g' "$file"
        
        # Fix specific underscore patterns
        sed -i 's/_engine: Arc<KnowledgeEngine>/engine: Arc<KnowledgeEngine>/g' "$file"
        sed -i 's/_stats\./stats./g' "$file"
        sed -i 's/let _stats =/let stats =/g' "$file"
        sed -i 's/_context: &str/context: \&str/g' "$file"
        sed -i 's/_context: Option<String>/context: Option<String>/g' "$file"
        sed -i 's/_input: &str/input: \&str/g' "$file"
        sed -i 's/_hash: u64/hash: u64/g' "$file"
        sed -i 's/_knowledge: &Vec<KnowledgeNode>/knowledge: \&Vec<KnowledgeNode>/g' "$file"
        sed -i 's/_query: &str/query: \&str/g' "$file"
        sed -i 's/_embedding: &\[f32\]/embedding: \&[f32]/g' "$file"
    done
}

# Function to fix webapp specific issues
fix_webapp_issues() {
    echo -e "${YELLOW}Fixing webapp module issues...${NC}"
    
    # Let's regenerate the problematic parts of mod.rs
    if [ -f "think-ai-webapp/src/graphics/mod.rs" ]; then
        # First backup the file
        cp "think-ai-webapp/src/graphics/mod.rs" "think-ai-webapp/src/graphics/mod.rs.bak"
        
        # Check if the file has the double Ok( pattern anywhere
        if grep -q "Ok(Ok(Self" "think-ai-webapp/src/graphics/mod.rs"; then
            echo "Found double Ok pattern, fixing..."
            sed -i 's/Ok(Ok(Self {/Ok(Self {/g' "think-ai-webapp/src/graphics/mod.rs"
        fi
        
        # Look for unclosed delimiters and fix them
        # This is a simple fix - if we find Ok(Self { without a matching }), add it
        perl -i -0pe 's/(Ok\(Self\s*\{[^}]*?)(\n\s*}\s*$)/$1})$2/gms' "think-ai-webapp/src/graphics/mod.rs"
    fi
}

# Function to fix consciousness module underscore variables
fix_consciousness_underscores() {
    echo -e "${YELLOW}Fixing consciousness module underscore variables...${NC}"
    
    find think-ai-consciousness -name "*.rs" -type f | while read -r file; do
        # Fix unused variable warnings by adding underscores where needed
        sed -i 's/perception: &Perception,/_perception: \&Perception,/g' "$file"
        sed -i 's/memory: &Memory,/_memory: \&Memory,/g' "$file"
        sed -i 's/symbols: &\[Symbol\],/_symbols: \&[Symbol],/g' "$file"
        sed -i 's/theme: &DreamTheme,/_theme: \&DreamTheme,/g' "$file"
        sed -i 's/identity: &Identity,/_identity: \&Identity,/g' "$file"
        sed -i 's/identity: &mut Identity,/_identity: \&mut Identity,/g' "$file"
        sed -i 's/consciousness_state: &ConsciousnessState,/_consciousness_state: \&ConsciousnessState,/g' "$file"
        
        # But don't double-underscore if already present
        sed -i 's/__perception:/_perception:/g' "$file"
        sed -i 's/__memory:/_memory:/g' "$file"
        sed -i 's/__symbols:/_symbols:/g' "$file"
        sed -i 's/__theme:/_theme:/g' "$file"
        sed -i 's/__identity:/_identity:/g' "$file"
        sed -i 's/__consciousness_state:/_consciousness_state:/g' "$file"
    done
}

# Function to check webapp structure
check_webapp_structure() {
    echo -e "${YELLOW}Checking webapp module structure...${NC}"
    
    # Count opening and closing braces in the graphics mod.rs
    if [ -f "think-ai-webapp/src/graphics/mod.rs" ]; then
        open_braces=$(grep -o '{' "think-ai-webapp/src/graphics/mod.rs" | wc -l)
        close_braces=$(grep -o '}' "think-ai-webapp/src/graphics/mod.rs" | wc -l)
        
        echo "Open braces: $open_braces, Close braces: $close_braces"
        
        if [ "$open_braces" -ne "$close_braces" ]; then
            echo -e "${RED}Brace mismatch detected! Manual intervention may be needed.${NC}"
        fi
    fi
}

# Function to run cargo fmt
run_cargo_fmt() {
    echo -e "${YELLOW}Running cargo fmt...${NC}"
    cargo fmt
}

# Function to test build
test_build() {
    echo -e "${YELLOW}Testing build...${NC}"
    cargo build 2>&1 | tee build-final-fixes.log
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✅ Build successful!${NC}"
        return 0
    else
        echo -e "${RED}❌ Build failed. Check build-final-fixes.log for details.${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo "Starting comprehensive error fixes..."
    
    # Run all fixes
    fix_knowledge_underscores
    fix_webapp_issues
    fix_consciousness_underscores
    check_webapp_structure
    run_cargo_fmt
    
    echo -e "${GREEN}✅ All fixes applied!${NC}"
    echo -e "${YELLOW}Testing build...${NC}"
    
    # Test the build
    if test_build; then
        echo -e "${GREEN}🎉 All compilation errors fixed successfully!${NC}"
    else
        echo -e "${RED}Some errors remain. Please check build-final-fixes.log${NC}"
    fi
}

# Run main function
main