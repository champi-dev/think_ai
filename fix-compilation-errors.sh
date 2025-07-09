#!/bin/bash

echo "🔧 Fixing Think AI compilation errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to fix parameter syntax errors
fix_parameter_syntax() {
    echo -e "${YELLOW}Fixing parameter syntax errors...${NC}"
    
    # Fix patterns like "_perception: perception: &PerceptionPerception" to "perception: &Perception"
    find . -name "*.rs" -type f | while read -r file; do
        # Skip target directory
        if [[ "$file" == *"/target/"* ]]; then
            continue
        fi
        
        # Fix perception parameters
        sed -i 's/_perception: perception: &PerceptionPerception/perception: \&Perception/g' "$file"
        sed -i 's/perception: perception: &PerceptionPerception/perception: \&Perception/g' "$file"
        
        # Fix identity parameters
        sed -i 's/_identity: identity: &IdentityIdentity/identity: \&Identity/g' "$file"
        sed -i 's/identity: identity: &IdentityIdentity/identity: \&Identity/g' "$file"
        
        # Fix consciousness_state parameters
        sed -i 's/_consciousness_state: consciousness_state: &ConsciousnessStateConsciousnessState/consciousness_state: \&ConsciousnessState/g' "$file"
        sed -i 's/consciousness_state: consciousness_state: &ConsciousnessStateConsciousnessState/consciousness_state: \&ConsciousnessState/g' "$file"
        
        # Fix memory parameters
        sed -i 's/_memory: memory: &MemoryMemory/memory: \&Memory/g' "$file"
        sed -i 's/memory: memory: &MemoryMemory/memory: \&Memory/g' "$file"
        
        # Fix type declarations in function signatures
        sed -i 's/perception: &PerceptionPerception/perception: \&Perception/g' "$file"
        sed -i 's/identity: &IdentityIdentity/identity: \&Identity/g' "$file"
        sed -i 's/consciousness_state: &ConsciousnessStateConsciousnessState/consciousness_state: \&ConsciousnessState/g' "$file"
        sed -i 's/memory: &MemoryMemory/memory: \&Memory/g' "$file"
    done
}

# Function to fix webapp delimiter issues
fix_webapp_delimiters() {
    echo -e "${YELLOW}Fixing webapp delimiter issues...${NC}"
    
    # Fix the specific files mentioned in the errors
    if [ -f "think-ai-webapp/src/graphics/mod.rs" ]; then
        # Fix the double Ok( pattern
        sed -i 's/Ok(Ok(Self {/Ok(Self {/g' "think-ai-webapp/src/graphics/mod.rs"
    fi
}

# Function to fix underscore variable references
fix_underscore_refs() {
    echo -e "${YELLOW}Fixing underscore variable references...${NC}"
    
    # For introspection.rs
    if [ -f "think-ai-consciousness/src/sentience/introspection.rs" ]; then
        # Remove underscores from parameter names where they're being used
        sed -i 's/fn analyze(&mut self, _perception:/fn analyze(\&mut self, perception:/g' "think-ai-consciousness/src/sentience/introspection.rs"
        sed -i 's/fn reflect_on_experience(&mut self, _perception:/fn reflect_on_experience(\&mut self, perception:/g' "think-ai-consciousness/src/sentience/introspection.rs"
        sed -i 's/fn assess_doubts(&mut self, _perception:/fn assess_doubts(\&mut self, perception:/g' "think-ai-consciousness/src/sentience/introspection.rs"
        sed -i 's/_perception: &Perception/perception: \&Perception/g' "think-ai-consciousness/src/sentience/introspection.rs"
        sed -i 's/_identity: &Identity/identity: \&Identity/g' "think-ai-consciousness/src/sentience/introspection.rs"
        sed -i 's/_consciousness_state: &ConsciousnessState/consciousness_state: \&ConsciousnessState/g' "think-ai-consciousness/src/sentience/introspection.rs"
    fi
    
    # For memory.rs
    if [ -f "think-ai-consciousness/src/sentience/memory.rs" ]; then
        sed -i 's/_perception: &Perception/perception: \&Perception/g' "think-ai-consciousness/src/sentience/memory.rs"
        sed -i 's/_memory: &Memory/memory: \&Memory/g' "think-ai-consciousness/src/sentience/memory.rs"
        sed -i 's/_consciousness_state: &ConsciousnessState/consciousness_state: \&ConsciousnessState/g' "think-ai-consciousness/src/sentience/memory.rs"
    fi
    
    # For mod.rs
    if [ -f "think-ai-consciousness/src/sentience/mod.rs" ]; then
        sed -i 's/_perception: &Perception/perception: \&Perception/g' "think-ai-consciousness/src/sentience/mod.rs"
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
    cargo build 2>&1 | tee build-test.log
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✅ Build successful!${NC}"
        return 0
    else
        echo -e "${RED}❌ Build failed. Check build-test.log for details.${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo "Starting compilation error fixes..."
    
    # Run all fixes
    fix_parameter_syntax
    fix_webapp_delimiters
    fix_underscore_refs
    run_cargo_fmt
    
    echo -e "${GREEN}✅ All fixes applied!${NC}"
    echo -e "${YELLOW}Testing build...${NC}"
    
    # Test the build
    if test_build; then
        echo -e "${GREEN}🎉 All compilation errors fixed successfully!${NC}"
    else
        echo -e "${RED}Some errors remain. Please check build-test.log${NC}"
    fi
}

# Run main function
main