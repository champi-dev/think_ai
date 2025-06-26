//! WebGL shader management and compilation
//! 
//! Provides O(1) shader compilation and caching with hash-based lookups

use wasm_bindgen::JsValue;
use web_sys::{WebGlRenderingContext, WebGlShader, WebGlProgram};
use std::collections::HashMap;

/// O(1) shader cache using hash-based lookups
pub struct ShaderCache {
    programs: HashMap<u64, WebGlProgram>,
    vertex_shaders: HashMap<u64, WebGlShader>,
    fragment_shaders: HashMap<u64, WebGlShader>,
}

impl ShaderCache {
    pub fn new() -> Self {
        Self {
            programs: HashMap::new(),
            vertex_shaders: HashMap::new(),
            fragment_shaders: HashMap::new(),
        }
    }

    /// O(1) shader program retrieval by hash
    pub fn get_program(&self, hash: u64) -> Option<&WebGlProgram> {
        self.programs.get(&hash)
    }

    /// O(1) program compilation and caching
    pub fn compile_program(
        &mut self,
        gl: &WebGlRenderingContext,
        vertex_source: &str,
        fragment_source: &str,
    ) -> Result<u64, JsValue> {
        let hash = self.calculate_program_hash(vertex_source, fragment_source);
        
        if self.programs.contains_key(&hash) {
            return Ok(hash);
        }

        let vertex_shader = self.compile_shader(gl, WebGlRenderingContext::VERTEX_SHADER, vertex_source)?;
        let fragment_shader = self.compile_shader(gl, WebGlRenderingContext::FRAGMENT_SHADER, fragment_source)?;
        
        let program = gl.create_program().ok_or("Failed to create shader program")?;
        gl.attach_shader(&program, &vertex_shader);
        gl.attach_shader(&program, &fragment_shader);
        gl.link_program(&program);

        if !gl.get_program_parameter(&program, WebGlRenderingContext::LINK_STATUS).as_bool().unwrap_or(false) {
            let info = gl.get_program_info_log(&program)
                .unwrap_or_else(|| "Unknown error creating shader program".to_string());
            return Err(JsValue::from_str(&info));
        }

        self.programs.insert(hash, program);
        Ok(hash)
    }

    fn compile_shader(
        &mut self,
        gl: &WebGlRenderingContext,
        shader_type: u32,
        source: &str,
    ) -> Result<WebGlShader, JsValue> {
        let shader = gl.create_shader(shader_type).ok_or("Failed to create shader")?;
        gl.shader_source(&shader, source);
        gl.compile_shader(&shader);

        if !gl.get_shader_parameter(&shader, WebGlRenderingContext::COMPILE_STATUS).as_bool().unwrap_or(false) {
            let info = gl.get_shader_info_log(&shader)
                .unwrap_or_else(|| "Unknown error compiling shader".to_string());
            return Err(JsValue::from_str(&info));
        }

        Ok(shader)
    }

    /// O(1) hash calculation for shader programs
    fn calculate_program_hash(&self, vertex: &str, fragment: &str) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        vertex.hash(&mut hasher);
        fragment.hash(&mut hasher);
        hasher.finish()
    }
}

/// Standard consciousness visualization shaders
pub mod consciousness_shaders {
    pub const CONSCIOUSNESS_VERTEX: &str = r#"
        attribute vec3 position;
        attribute vec3 color;
        attribute float consciousness_level;
        
        uniform mat4 u_model_view_projection;
        uniform float u_time;
        
        varying vec3 v_color;
        varying float v_consciousness;
        
        void main() {
            vec3 pos = position;
            
            // Consciousness-based vertex displacement
            float wave = sin(u_time * 2.0 + consciousness_level * 10.0) * 0.1;
            pos.y += wave * consciousness_level;
            
            gl_Position = u_model_view_projection * vec4(pos, 1.0);
            v_color = color;
            v_consciousness = consciousness_level;
        }
    "#;

    pub const CONSCIOUSNESS_FRAGMENT: &str = r#"
        precision mediump float;
        
        varying vec3 v_color;
        varying float v_consciousness;
        
        uniform float u_time;
        
        void main() {
            vec3 color = v_color;
            
            // Consciousness glow effect
            float glow = 0.5 + 0.5 * sin(u_time * 3.0 + v_consciousness * 6.28);
            color *= (1.0 + glow * v_consciousness);
            
            gl_FragColor = vec4(color, 0.8);
        }
    "#;
}

/// Neural network visualization shaders
pub mod neural_shaders {
    pub const NEURAL_VERTEX: &str = r#"
        attribute vec3 position;
        attribute float activation;
        
        uniform mat4 u_model_view_projection;
        uniform float u_time;
        
        varying float v_activation;
        
        void main() {
            vec3 pos = position;
            
            // Pulse based on activation
            float pulse = 1.0 + activation * 0.2 * sin(u_time * 4.0);
            pos *= pulse;
            
            gl_Position = u_model_view_projection * vec4(pos, 1.0);
            v_activation = activation;
        }
    "#;

    pub const NEURAL_FRAGMENT: &str = r#"
        precision mediump float;
        
        varying float v_activation;
        
        void main() {
            vec3 color = mix(
                vec3(0.2, 0.2, 0.8),  // Low activation: blue
                vec3(1.0, 0.4, 0.1),  // High activation: orange
                v_activation
            );
            
            gl_FragColor = vec4(color, 0.9);
        }
    "#;
}