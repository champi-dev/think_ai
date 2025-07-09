#!/bin/bash

echo "🔧 Fixing additional Think AI syntax errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to fix dreams.rs specific issues
fix_dreams_syntax() {
    echo -e "${YELLOW}Fixing dreams.rs syntax errors...${NC}"
    
    if [ -f "think-ai-consciousness/src/sentience/dreams.rs" ]; then
        # Fix array syntax patterns like &[Symbol][Symbol] -> &[Symbol]
        sed -i 's/&\[Symbol\]\[Symbol\]/\&[Symbol]/g' "think-ai-consciousness/src/sentience/dreams.rs"
        
        # Fix double type names
        sed -i 's/&DreamThemeDreamTheme/\&DreamTheme/g' "think-ai-consciousness/src/sentience/dreams.rs"
        
        # Fix parameter patterns with symbols
        sed -i 's/_symbols: symbols: &\[Symbol\]/symbols: \&[Symbol]/g' "think-ai-consciousness/src/sentience/dreams.rs"
        sed -i 's/symbols: symbols: &\[Symbol\]/symbols: \&[Symbol]/g' "think-ai-consciousness/src/sentience/dreams.rs"
        
        # Fix parameter patterns with theme
        sed -i 's/_theme: theme: &DreamTheme/theme: \&DreamTheme/g' "think-ai-consciousness/src/sentience/dreams.rs"
        sed -i 's/theme: theme: &DreamTheme/theme: \&DreamTheme/g' "think-ai-consciousness/src/sentience/dreams.rs"
    fi
}

# Function to fix evolution.rs specific issues
fix_evolution_syntax() {
    echo -e "${YELLOW}Fixing evolution.rs syntax errors...${NC}"
    
    if [ -f "think-ai-consciousness/src/sentience/evolution.rs" ]; then
        # Fix the messed up &mut patterns
        sed -i 's/&mut Identitymut Identity/\&mut Identity/g' "think-ai-consciousness/src/sentience/evolution.rs"
        
        # Fix parameter patterns
        sed -i 's/_identity: identity: &mut Identity/identity: \&mut Identity/g' "think-ai-consciousness/src/sentience/evolution.rs"
        sed -i 's/identity: identity: &mut Identity/identity: \&mut Identity/g' "think-ai-consciousness/src/sentience/evolution.rs"
    fi
}

# Function to clean up any remaining double type patterns
fix_double_types() {
    echo -e "${YELLOW}Fixing double type patterns across all files...${NC}"
    
    find . -name "*.rs" -type f | while read -r file; do
        # Skip target directory
        if [[ "$file" == *"/target/"* ]]; then
            continue
        fi
        
        # Fix common double type patterns
        sed -i 's/ConsciousnessStateConsciousnessState/ConsciousnessState/g' "$file"
        sed -i 's/PerceptionPerception/Perception/g' "$file"
        sed -i 's/IdentityIdentity/Identity/g' "$file"
        sed -i 's/MemoryMemory/Memory/g' "$file"
        sed -i 's/DreamThemeDreamTheme/DreamTheme/g' "$file"
    done
}

# Function to fix remaining parameter syntax issues
fix_remaining_params() {
    echo -e "${YELLOW}Fixing remaining parameter syntax issues...${NC}"
    
    find . -name "*.rs" -type f | while read -r file; do
        # Skip target directory
        if [[ "$file" == *"/target/"* ]]; then
            continue
        fi
        
        # Generic pattern to fix parameter: type: patterns
        # This regex looks for patterns like "word: word: &Type" and fixes them to "word: &Type"
        perl -i -pe 's/(\w+):\s*\1:\s*(&[^,\)]+)/\1: \2/g' "$file"
        
        # Fix underscore parameter patterns more aggressively
        perl -i -pe 's/_(\w+):\s*\1:\s*(&[^,\)]+)/\1: \2/g' "$file"
    done
}

# Function to run cargo fmt
run_cargo_fmt() {
    echo -e "${YELLOW}Running cargo fmt...${NC}"
    cargo fmt
}

# Function to test build
test_build() {
    echo -e "${YELLOW}Testing build...${NC}"
    cargo build 2>&1 | tee build-additional-fixes.log
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✅ Build successful!${NC}"
        return 0
    else
        echo -e "${RED}❌ Build failed. Check build-additional-fixes.log for details.${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo "Starting additional syntax error fixes..."
    
    # Run all fixes
    fix_dreams_syntax
    fix_evolution_syntax
    fix_double_types
    fix_remaining_params
    run_cargo_fmt
    
    echo -e "${GREEN}✅ All additional fixes applied!${NC}"
    echo -e "${YELLOW}Testing build...${NC}"
    
    # Test the build
    if test_build; then
        echo -e "${GREEN}🎉 All compilation errors fixed successfully!${NC}"
    else
        echo -e "${RED}Some errors remain. Please check build-additional-fixes.log${NC}"
    fi
}

# Run main function
main