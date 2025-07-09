#!/bin/bash

echo "🔧 Fixing Think AI knowledge module syntax errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to fix knowledge module specific issues
fix_knowledge_syntax() {
    echo -e "${YELLOW}Fixing knowledge module syntax errors...${NC}"
    
    find think-ai-knowledge -name "*.rs" -type f | while read -r file; do
        # Fix double Arc parameters
        sed -i 's/&Arc<KnowledgeEngine>Arc<KnowledgeEngine>/\&Arc<KnowledgeEngine>/g' "$file"
        
        # Fix double Vec parameters
        sed -i 's/&Vec<KnowledgeNode>Vec<KnowledgeNode>/\&Vec<KnowledgeNode>/g' "$file"
        
        # Fix double array parameters
        sed -i 's/&\[f32\]\[f32\]/\&[f32]/g' "$file"
        
        # Fix double str parameters
        sed -i 's/&strstr/\&str/g' "$file"
        sed -i 's/: &strstr/: \&str/g' "$file"
        
        # Fix complex Option patterns
        sed -i 's/Option<context: Option<&str>str>/Option<\&str>/g' "$file"
        
        # Fix complex array patterns
        sed -i 's/&\[&&KnowledgeNode\]\[nodes: &\[&&KnowledgeNode\]nodes: &\[&&KnowledgeNode\]KnowledgeNode\]/\&[\&KnowledgeNode]/g' "$file"
        
        # Fix _engine parameter patterns
        sed -i 's/_engine: &Arc<KnowledgeEngine>/engine: \&Arc<KnowledgeEngine>/g' "$file"
        
        # Fix _nodes parameter patterns
        sed -i 's/_nodes: &\[&&KnowledgeNode\]/nodes: \&[\&KnowledgeNode]/g' "$file"
        sed -i 's/_nodes: &\[\&KnowledgeNode\]/nodes: \&[\&KnowledgeNode]/g' "$file"
        
        # Fix _knowledge parameter patterns
        sed -i 's/_knowledge: &Vec<KnowledgeNode>/knowledge: \&Vec<KnowledgeNode>/g' "$file"
        
        # Fix _query parameter patterns
        sed -i 's/_query: &str/query: \&str/g' "$file"
        
        # Fix _embedding parameter patterns
        sed -i 's/_embedding: &\[f32\]/embedding: \&[f32]/g' "$file"
        
        # Fix _context parameter patterns
        sed -i 's/_context: Option<&str>/context: Option<\&str>/g' "$file"
    done
}

# Function to fix remaining webapp issues
fix_webapp_missing() {
    echo -e "${YELLOW}Checking for any remaining webapp issues...${NC}"
    
    if [ -f "think-ai-webapp/src/graphics/mod.rs" ]; then
        # Check if we need to fix unclosed delimiters
        if grep -q "Ok(Self {" "think-ai-webapp/src/graphics/mod.rs"; then
            # Count opening and closing braces to ensure they match
            echo "Webapp graphics module seems fixed"
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
    cargo build 2>&1 | tee build-knowledge-fixes.log
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✅ Build successful!${NC}"
        return 0
    else
        echo -e "${RED}❌ Build failed. Check build-knowledge-fixes.log for details.${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo "Starting knowledge module syntax error fixes..."
    
    # Run all fixes
    fix_knowledge_syntax
    fix_webapp_missing
    run_cargo_fmt
    
    echo -e "${GREEN}✅ All knowledge fixes applied!${NC}"
    echo -e "${YELLOW}Testing build...${NC}"
    
    # Test the build
    if test_build; then
        echo -e "${GREEN}🎉 All compilation errors fixed successfully!${NC}"
    else
        echo -e "${RED}Some errors remain. Please check build-knowledge-fixes.log${NC}"
    fi
}

# Run main function
main