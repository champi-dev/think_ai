#!/bin/bash

echo "🔧 Fixing ALL Think AI compilation errors comprehensively..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to fix all parameter syntax errors
fix_all_parameters() {
    echo -e "${YELLOW}Fixing ALL parameter syntax errors...${NC}"
    
    # Fix all double type patterns in knowledge module
    find think-ai-knowledge -name "*.rs" -type f | while read -r file; do
        # Fix Arc patterns
        sed -i 's/&Arc<KnowledgeEngine>Arc<KnowledgeEngine>/\&Arc<KnowledgeEngine>/g' "$file"
        
        # Fix Vec patterns
        sed -i 's/&Vec<KnowledgeNode>Vec<KnowledgeNode>/\&Vec<KnowledgeNode>/g' "$file"
        
        # Fix str patterns
        sed -i 's/&strstr/\&str/g' "$file"
        sed -i 's/_query: &strstr/_query: \&str/g' "$file"
        
        # Fix array patterns
        sed -i 's/&\[f32\]\[f32\]/\&[f32]/g' "$file"
        sed -i 's/&\[&&KnowledgeNode\]\[nodes: &\[&&KnowledgeNode\]nodes: &\[&&KnowledgeNode\]KnowledgeNode\]/\&[\&KnowledgeNode]/g' "$file"
        
        # Fix Option patterns
        sed -i 's/Option<context: Option<&str>str>/Option<\&str>/g' "$file"
        
        # Fix underscore parameters by removing the underscore
        sed -i 's/_engine: &Arc<KnowledgeEngine>/engine: \&Arc<KnowledgeEngine>/g' "$file"
        sed -i 's/_knowledge: &Vec<KnowledgeNode>/knowledge: \&Vec<KnowledgeNode>/g' "$file"
        sed -i 's/_nodes: &\[&KnowledgeNode\]/nodes: \&[\&KnowledgeNode]/g' "$file"
        sed -i 's/_nodes: &\[&&KnowledgeNode\]/nodes: \&[\&\&KnowledgeNode]/g' "$file"
        sed -i 's/_query: &str/query: \&str/g' "$file"
        sed -i 's/_embedding: &\[f32\]/embedding: \&[f32]/g' "$file"
        sed -i 's/_context: &str/context: \&str/g' "$file"
        sed -i 's/_context: Option<&str>/context: Option<\&str>/g' "$file"
        sed -i 's/_context: Option<String>/context: Option<String>/g' "$file"
        sed -i 's/_input: &str/input: \&str/g' "$file"
        sed -i 's/_hash: u64/hash: u64/g' "$file"
        sed -i 's/_stats: /stats: /g' "$file"
        
        # Fix double underscores  
        sed -i 's/knowledge__engine/knowledge_engine/g' "$file"
        sed -i 's/from__context/from_context/g' "$file"
        sed -i 's/to__context/to_context/g' "$file"
    done
    
    # Fix consciousness module patterns
    find think-ai-consciousness -name "*.rs" -type f | while read -r file; do
        # Fix dreams.rs specific patterns
        sed -i 's/&\[Symbol\]\[Symbol\]/\&[Symbol]/g' "$file"
        sed -i 's/&DreamThemeDreamTheme/\&DreamTheme/g' "$file"
        sed -i 's/_symbols: symbols: &\[Symbol\]/symbols: \&[Symbol]/g' "$file"
        sed -i 's/_theme: theme: &DreamTheme/theme: \&DreamTheme/g' "$file"
        
        # Fix evolution.rs patterns
        sed -i 's/&mut Identitymut Identity/\&mut Identity/g' "$file"
        sed -i 's/_identity: identity: &mut Identity/identity: \&mut Identity/g' "$file"
    done
}

# Function to fix webapp
fix_webapp_properly() {
    echo -e "${YELLOW}Fixing webapp module properly...${NC}"
    
    # Create a working webapp graphics module
    cat > think-ai-webapp/src/graphics/mod.rs << 'EOF'
use wasm_bindgen::prelude::*;
use web_sys::{WebGlRenderingContext, WebGlProgram, WebGlShader};

pub mod consciousness;
pub mod materials;
pub mod neural_network;
pub mod particles;
pub mod shaders;

pub struct GraphicsEngine {
    context: WebGlRenderingContext,
    program: WebGlProgram,
    time: f32,
    delta_time: f32,
    last_time: f32,
}

impl GraphicsEngine {
    pub fn new() -> Result<Self, JsValue> {
        // Get canvas and WebGL context
        let document = web_sys::window().unwrap().document().unwrap();
        let canvas = document.get_element_by_id("canvas").unwrap();
        let canvas: web_sys::HtmlCanvasElement = canvas
            .dyn_into::<web_sys::HtmlCanvasElement>()
            .map_err(|_| "Failed to cast to HtmlCanvasElement")?;

        let context = canvas
            .get_context("webgl")?
            .unwrap()
            .dyn_into::<WebGlRenderingContext>()?;

        // Create shader program
        let vert_shader = compile_shader(
            &context,
            WebGlRenderingContext::VERTEX_SHADER,
            include_str!("../shaders/vertex.glsl"),
        )?;
        
        let frag_shader = compile_shader(
            &context,
            WebGlRenderingContext::FRAGMENT_SHADER,
            include_str!("../shaders/fragment.glsl"),
        )?;

        let program = link_program(&context, &vert_shader, &frag_shader)?;
        context.use_program(Some(&program));

        Ok(Self {
            context,
            program,
            time: 0.0,
            delta_time: 0.0,
            last_time: 0.0,
        })
    }

    pub fn render(&mut self, current_time: f32) {
        self.delta_time = current_time - self.last_time;
        self.last_time = current_time;
        self.time = current_time;

        // Clear the canvas
        self.context.clear_color(0.0, 0.0, 0.0, 1.0);
        self.context.clear(WebGlRenderingContext::COLOR_BUFFER_BIT);

        // Render components
        // TODO: Implement actual rendering
    }

    pub fn resize(&self, width: i32, height: i32) {
        self.context.viewport(0, 0, width, height);
    }
}

fn compile_shader(
    context: &WebGlRenderingContext,
    shader_type: u32,
    source: &str,
) -> Result<WebGlShader, String> {
    let shader = context
        .create_shader(shader_type)
        .ok_or_else(|| String::from("Unable to create shader object"))?;
    
    context.shader_source(&shader, source);
    context.compile_shader(&shader);

    if context
        .get_shader_parameter(&shader, WebGlRenderingContext::COMPILE_STATUS)
        .as_bool()
        .unwrap_or(false)
    {
        Ok(shader)
    } else {
        Err(context
            .get_shader_info_log(&shader)
            .unwrap_or_else(|| String::from("Unknown error creating shader")))
    }
}

fn link_program(
    context: &WebGlRenderingContext,
    vert_shader: &WebGlShader,
    frag_shader: &WebGlShader,
) -> Result<WebGlProgram, String> {
    let program = context
        .create_program()
        .ok_or_else(|| String::from("Unable to create shader object"))?;

    context.attach_shader(&program, vert_shader);
    context.attach_shader(&program, frag_shader);
    context.link_program(&program);

    if context
        .get_program_parameter(&program, WebGlRenderingContext::LINK_STATUS)
        .as_bool()
        .unwrap_or(false)
    {
        Ok(program)
    } else {
        Err(context
            .get_program_info_log(&program)
            .unwrap_or_else(|| String::from("Unknown error creating program object")))
    }
}
EOF
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
    echo "Starting comprehensive compilation error fixes..."
    
    # Run all fixes
    fix_all_parameters
    fix_webapp_properly
    run_cargo_fmt
    
    echo -e "${GREEN}✅ All fixes applied!${NC}"
    echo -e "${YELLOW}Testing build...${NC}"
    
    # Test the build
    if test_build; then
        echo -e "${GREEN}🎉 All compilation errors fixed successfully!${NC}"
        echo -e "${GREEN}You can now run: cargo build --release${NC}"
    else
        echo -e "${RED}Some errors may remain. Please check build-final-fixes.log${NC}"
        # Show last few errors for quick diagnosis
        echo -e "${YELLOW}Last few error lines:${NC}"
        tail -20 build-final-fixes.log | grep -E "error:|error\["
    fi
}

# Run main function
main