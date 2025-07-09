#!/bin/bash

echo "🔧 Final compilation fixes for Think AI..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Create missing shader files for webapp
create_shader_files() {
    echo -e "${YELLOW}Creating missing shader files...${NC}"
    
    mkdir -p think-ai-webapp/src/shaders
    
    # Create vertex shader
    cat > think-ai-webapp/src/shaders/vertex.glsl << 'EOF'
attribute vec3 position;
attribute vec3 normal;
attribute vec2 texcoord;

uniform mat4 u_model;
uniform mat4 u_view;
uniform mat4 u_projection;
uniform mat4 u_normal_matrix;

varying vec3 v_position;
varying vec3 v_normal;
varying vec2 v_texcoord;

void main() {
    vec4 world_pos = u_model * vec4(position, 1.0);
    v_position = world_pos.xyz;
    v_normal = normalize((u_normal_matrix * vec4(normal, 0.0)).xyz);
    v_texcoord = texcoord;
    
    gl_Position = u_projection * u_view * world_pos;
}
EOF

    # Create fragment shader
    cat > think-ai-webapp/src/shaders/fragment.glsl << 'EOF'
precision mediump float;

uniform vec3 u_light_position;
uniform vec3 u_view_position;
uniform vec3 u_diffuse_color;
uniform vec3 u_specular_color;
uniform vec3 u_emissive_color;
uniform float u_shininess;
uniform float u_transparency;
uniform float u_consciousness_factor;

varying vec3 v_position;
varying vec3 v_normal;
varying vec2 v_texcoord;

void main() {
    vec3 normal = normalize(v_normal);
    vec3 light_dir = normalize(u_light_position - v_position);
    vec3 view_dir = normalize(u_view_position - v_position);
    vec3 reflect_dir = reflect(-light_dir, normal);
    
    // Diffuse lighting
    float diff = max(dot(normal, light_dir), 0.0);
    vec3 diffuse = diff * u_diffuse_color;
    
    // Specular lighting
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), u_shininess);
    vec3 specular = spec * u_specular_color;
    
    // Consciousness glow effect
    vec3 consciousness_glow = u_emissive_color * u_consciousness_factor;
    
    // Final color
    vec3 result = diffuse + specular + consciousness_glow;
    gl_FragColor = vec4(result, u_transparency);
}
EOF
}

# 2. Fix remaining underscore variables
fix_remaining_underscores() {
    echo -e "${YELLOW}Fixing remaining underscore variables...${NC}"
    
    # Fix specific files with underscore issues
    files=(
        "think-ai-knowledge/src/evidence.rs"
        "think-ai-knowledge/src/responder.rs"
        "think-ai-knowledge/src/trainer.rs"
        "think-ai-knowledge/src/comprehensive_trainer.rs"
        "think-ai-knowledge/src/intelligent_response_selector.rs"
        "think-ai-knowledge/src/llm_benchmarks.rs"
        "think-ai-knowledge/src/multi_candidate_selector.rs"
        "think-ai-knowledge/src/o1_benchmark_monitor.rs"
        "think-ai-knowledge/src/automated_benchmark_runner.rs"
        "think-ai-knowledge/src/autonomous_agent.rs"
        "think-ai-knowledge/src/benchmark_trainer.rs"
        "think-ai-knowledge/src/dynamic_expression.rs"
        "think-ai-knowledge/src/isolated_session.rs"
        "think-ai-knowledge/src/parallel_processor.rs"
    )
    
    for file in "${files[@]}"; do
        if [ -f "$file" ]; then
            # Fix _engine patterns
            sed -i 's/pub fn new(_engine:/pub fn new(engine:/g' "$file"
            sed -i 's/Self { engine }/Self { engine: engine.clone() }/g' "$file"
            
            # Fix _stats patterns  
            sed -i 's/let _stats =/let stats =/g' "$file"
            
            # Fix _response_time patterns
            sed -i 's/let _response_time =/let response_time =/g' "$file"
            
            # Fix _context patterns
            sed -i 's/_context: &str/context: \&str/g' "$file"
            sed -i 's/_context: Option</context: Option</g' "$file"
            
            # Fix _input patterns
            sed -i 's/_input: &str/input: \&str/g' "$file"
            
            # Fix _hash patterns
            sed -i 's/_hash: u64/hash: u64/g' "$file"
            
            # Fix double underscores
            sed -i 's/knowledge__engine/knowledge_engine/g' "$file"
            sed -i 's/from__context/from_context/g' "$file"
            sed -i 's/to__context/to_context/g' "$file"
            sed -i 's/user__answer/user_answer/g' "$file"
            sed -i 's/correct__answer/correct_answer/g' "$file"
            sed -i 's/categorystats/category_stats/g' "$file"
            sed -i 's/difficultystats/difficulty_stats/g' "$file"
        fi
    done
}

# 3. Fix webapp component issues
fix_webapp_components() {
    echo -e "${YELLOW}Fixing webapp component issues...${NC}"
    
    # Fix ui/effects.rs if it doesn't exist
    if [ ! -f "think-ai-webapp/src/ui/effects.rs" ]; then
        cat > think-ai-webapp/src/ui/effects.rs << 'EOF'
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
    
    pub fn clear_effects(&mut self) {
        self.active_effects.clear();
    }
}
EOF
    fi
    
    # Fix specific type issues
    sed -i 's/&ResponseAnalysisResponseAnalysis/\&ResponseAnalysis/g' think-ai-knowledge/src/intelligent_response_selector.rs
}

# 4. Run cargo fmt
run_cargo_fmt() {
    echo -e "${YELLOW}Running cargo fmt...${NC}"
    cargo fmt
}

# 5. Test build
test_build() {
    echo -e "${YELLOW}Testing build...${NC}"
    cargo build 2>&1 | tee build-final-test.log
    
    if [ ${PIPESTATUS[0]} -eq 0 ]; then
        echo -e "${GREEN}✅ Build successful!${NC}"
        return 0
    else
        echo -e "${RED}❌ Build failed. Check build-final-test.log for details.${NC}"
        return 1
    fi
}

# Main execution
main() {
    echo "Starting final compilation fixes..."
    
    # Run all fixes
    create_shader_files
    fix_remaining_underscores
    fix_webapp_components
    run_cargo_fmt
    
    echo -e "${GREEN}✅ All final fixes applied!${NC}"
    echo -e "${YELLOW}Testing build...${NC}"
    
    # Test the build
    if test_build; then
        echo -e "${GREEN}🎉 Compilation successful!${NC}"
        echo -e "${GREEN}Build complete. You can now run:${NC}"
        echo -e "${GREEN}  cargo build --release${NC}"
        echo -e "${GREEN}  cargo test${NC}"
        echo -e "${GREEN}  ./target/release/think-ai chat${NC}"
    else
        echo -e "${RED}Some errors remain. Check build-final-test.log${NC}"
    fi
}

# Run main function
main