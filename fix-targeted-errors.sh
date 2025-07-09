#!/bin/bash

echo "🔧 Fixing targeted Think AI compilation errors..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to undo consciousness underscore additions
undo_consciousness_underscores() {
    echo -e "${YELLOW}Undoing consciousness module underscore additions...${NC}"
    
    find think-ai-consciousness -name "*.rs" -type f | while read -r file; do
        # Remove underscores we accidentally added
        sed -i 's/_perception: &Perception,/perception: \&Perception,/g' "$file"
        sed -i 's/_memory: &Memory,/memory: \&Memory,/g' "$file"
        sed -i 's/_symbols: &\[Symbol\],/symbols: \&[Symbol],/g' "$file"
        sed -i 's/_theme: &DreamTheme,/theme: \&DreamTheme,/g' "$file"
        sed -i 's/_identity: &Identity,/identity: \&Identity,/g' "$file"
        sed -i 's/_identity: &mut Identity,/identity: \&mut Identity,/g' "$file"
        sed -i 's/_consciousness_state: &ConsciousnessState,/consciousness_state: \&ConsciousnessState,/g' "$file"
        
        # But keep underscores where variables are actually unused
        # This is for desires.rs line 293
        sed -i '293s/perception: &Perception,/_perception: \&Perception,/' "think-ai-consciousness/src/sentience/desires.rs" 2>/dev/null || true
        # For dreams.rs line 214
        sed -i '214s/memory: &Memory,/_memory: \&Memory,/' "think-ai-consciousness/src/sentience/dreams.rs" 2>/dev/null || true
        # For dreams.rs line 299
        sed -i '299s/symbols: &\[Symbol\],/_symbols: \&[Symbol],/' "think-ai-consciousness/src/sentience/dreams.rs" 2>/dev/null || true
        # For dreams.rs line 541
        sed -i '541s/theme: &DreamTheme,/_theme: \&DreamTheme,/' "think-ai-consciousness/src/sentience/dreams.rs" 2>/dev/null || true
        # For evolution.rs line 156
        sed -i '156s/identity: &Identity,/_identity: \&Identity,/' "think-ai-consciousness/src/sentience/evolution.rs" 2>/dev/null || true
        # For evolution.rs line 195
        sed -i '195s/identity: &mut Identity,/_identity: \&mut Identity,/' "think-ai-consciousness/src/sentience/evolution.rs" 2>/dev/null || true
        # For expression.rs line 128
        sed -i '128s/consciousness_state: &ConsciousnessState,/_consciousness_state: \&ConsciousnessState,/' "think-ai-consciousness/src/sentience/expression.rs" 2>/dev/null || true
        # For expression.rs line 160
        sed -i '160s/identity: &Identity,/_identity: \&Identity,/' "think-ai-consciousness/src/sentience/expression.rs" 2>/dev/null || true
    done
}

# Function to fix webapp specific issues
fix_webapp_specific() {
    echo -e "${YELLOW}Fixing webapp specific issues...${NC}"
    
    # Fix duplicate imports in dashboard.rs
    if [ -f "think-ai-webapp/src/ui/dashboard.rs" ]; then
        # Remove the duplicate JsValue import (line 5)
        sed -i '5d' "think-ai-webapp/src/ui/dashboard.rs"
    fi
    
    # Fix missing EffectManager in effects.rs
    if [ -f "think-ai-webapp/src/ui/effects.rs" ]; then
        # Check if EffectManager exists, if not add it
        if ! grep -q "pub struct EffectManager" "think-ai-webapp/src/ui/effects.rs"; then
            cat >> "think-ai-webapp/src/ui/effects.rs" << 'EOF'

pub struct EffectManager {
    active_effects: Vec<String>,
}

impl EffectManager {
    pub fn new() -> Self {
        Self {
            active_effects: Vec::new(),
        }
    }
    
    pub fn add_effect(&mut self, effect: String) {
        self.active_effects.push(effect);
    }
}
EOF
        fi
    fi
    
    # Fix materials.rs missing program field
    if [ -f "think-ai-webapp/src/graphics/materials.rs" ]; then
        # Check if MaterialCache is missing program field
        if ! grep -q "program:" "think-ai-webapp/src/graphics/materials.rs"; then
            # Add program field to MaterialCache struct
            sed -i '/pub struct MaterialCache {/,/^}/ {
                /active_material:/ a\
    program: WebGlProgram,
            }' "think-ai-webapp/src/graphics/materials.rs" 2>/dev/null || true
        fi
    fi
    
    # Fix the Result type issue for wasm_bindgen
    if [ -f "think-ai-webapp/src/lib.rs" ]; then
        # The issue is that wasm_bindgen can't handle Result<CustomType, JsValue>
        # We need to return the type directly or use a different approach
        sed -i 's/pub fn new() -> Result<ThinkAiWebapp, JsValue> {/pub fn new() -> ThinkAiWebapp {/g' "think-ai-webapp/src/lib.rs"
        # Remove Ok() wrapper from the return
        sed -i '/^        Ok(Self {/,/^        })$/ {
            s/Ok(Self {/Self {/
            s/})$/}/
        }' "think-ai-webapp/src/lib.rs"
    fi
    
    # Fix components.rs StreamMsg vs ChatMsg mismatch
    if [ -f "think-ai-webapp/src/ui/components.rs" ]; then
        # Change StreamMsg to ChatMsg in the match arms
        sed -i 's/StreamMsg::AddResponse/ChatMsg::AddResponse/g' "think-ai-webapp/src/ui/components.rs"
        sed -i 's/StreamMsg::StartStream/ChatMsg::StartStream/g' "think-ai-webapp/src/ui/components.rs"
        sed -i 's/StreamMsg::StopStream/ChatMsg::StopStream/g' "think-ai-webapp/src/ui/components.rs"
        # Fix the function signature
        sed -i 's/msg: StreamMsg/msg: ChatMsg/g' "think-ai-webapp/src/ui/components.rs"
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
    cargo build 2>&1 | tee build-targeted-fixes.log
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✅ Build successful!${NC}"
        return 0
    else
        echo -e "${RED}❌ Build failed. Check build-targeted-fixes.log for details.${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo "Starting targeted error fixes..."
    
    # Run all fixes
    undo_consciousness_underscores
    fix_webapp_specific
    run_cargo_fmt
    
    echo -e "${GREEN}✅ All targeted fixes applied!${NC}"
    echo -e "${YELLOW}Testing build...${NC}"
    
    # Test the build
    if test_build; then
        echo -e "${GREEN}🎉 All compilation errors fixed successfully!${NC}"
    else
        echo -e "${RED}Some errors remain. Please check build-targeted-fixes.log${NC}"
    fi
}

# Run main function
main