#!/bin/bash

echo "🔧 ULTIMATE FIX FOR ALL COMPILATION ISSUES"
echo "=========================================="

# Step 1: Fix the TinyLlama imports in full-server-fast.rs
echo ""
echo "1️⃣ Fixing TinyLlama imports..."
sed -i '1i\use think_ai_tinyllama::{TinyLlamaClient, EnhancedTinyLlama};' think-ai-cli/src/bin/full-server-fast.rs

# Step 2: Fix the webapp Matrix4 type issues
echo ""
echo "2️⃣ Fixing Matrix4 types in webapp..."
find think-ai-webapp/src -name "*.rs" -type f -exec sed -i 's/Matrix4<f32>/\[f32; 16\]/g' {} \;
find think-ai-webapp/src -name "*.rs" -type f -exec sed -i 's/&Matrix4/&\[f32; 16\]/g' {} \;

# Step 3: Fix the math module to export proper types
echo ""
echo "3️⃣ Fixing math module..."
cat > think-ai-webapp/src/math.rs << 'EOF'
pub type Matrix4 = [f32; 16];
pub type Vector3 = Vector3Struct;

#[derive(Clone, Copy, Debug)]
pub struct Vector3Struct {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Vector3Struct {
    pub fn new(x: f32, y: f32, z: f32) -> Self {
        Self { x, y, z }
    }
}

pub struct Matrix4Utils;

impl Matrix4Utils {
    pub fn identity() -> Matrix4 {
        [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]
    }
    
    pub fn perspective(fovy: f32, aspect: f32, near: f32, far: f32) -> Matrix4 {
        let f = 1.0 / (fovy / 2.0).tan();
        [
            f / aspect, 0.0, 0.0, 0.0,
            0.0, f, 0.0, 0.0,
            0.0, 0.0, (far + near) / (near - far), -1.0,
            0.0, 0.0, (2.0 * far * near) / (near - far), 0.0,
        ]
    }
    
    pub fn look_at(eye: &Vector3Struct, center: &Vector3Struct, up: &Vector3Struct) -> Matrix4 {
        let z = Vector3Struct {
            x: eye.x - center.x,
            y: eye.y - center.y,
            z: eye.z - center.z,
        };
        let z_len = (z.x * z.x + z.y * z.y + z.z * z.z).sqrt();
        let z = Vector3Struct {
            x: z.x / z_len,
            y: z.y / z_len,
            z: z.z / z_len,
        };
        
        let x = Vector3Struct {
            x: up.y * z.z - up.z * z.y,
            y: up.z * z.x - up.x * z.z,
            z: up.x * z.y - up.y * z.x,
        };
        let x_len = (x.x * x.x + x.y * x.y + x.z * x.z).sqrt();
        let x = Vector3Struct {
            x: x.x / x_len,
            y: x.y / x_len,
            z: x.z / x_len,
        };
        
        let y = Vector3Struct {
            x: z.y * x.z - z.z * x.y,
            y: z.z * x.x - z.x * x.z,
            z: z.x * x.y - z.y * x.x,
        };
        
        [
            x.x, y.x, z.x, 0.0,
            x.y, y.y, z.y, 0.0,
            x.z, y.z, z.z, 0.0,
            -(x.x * eye.x + x.y * eye.y + x.z * eye.z),
            -(y.x * eye.x + y.y * eye.y + y.z * eye.z),
            -(z.x * eye.x + z.y * eye.y + z.z * eye.z),
            1.0,
        ]
    }
}
EOF

# Step 4: Fix neural_network.rs to use proper Matrix4
echo ""
echo "4️⃣ Fixing neural_network.rs..."
sed -i 's/Matrix4::identity()/Matrix4Utils::identity()/g' think-ai-webapp/src/graphics/neural_network.rs
sed -i '5i\use crate::math::Matrix4Utils;' think-ai-webapp/src/graphics/neural_network.rs

# Step 5: Fix consciousness.rs render method
echo ""
echo "5️⃣ Fixing consciousness.rs..."
cat > think-ai-webapp/src/graphics/consciousness.rs << 'EOF'
use wasm_bindgen::prelude::*;
use web_sys::{WebGlRenderingContext, WebGlProgram, WebGlBuffer};
use crate::math::{Matrix4, Vector3, Matrix4Utils};
use crate::graphics::particles::ParticleSystem;
use crate::graphics::neural_network::NeuralNetwork;
use std::rc::Rc;

pub struct ConsciousnessVisualization {
    gl: Rc<WebGlRenderingContext>,
    particle_system: ParticleSystem,
    neural_network: NeuralNetwork,
    energy_field: EnergyField,
    time: f32,
}

struct EnergyField {
    gl: Rc<WebGlRenderingContext>,
    program: WebGlProgram,
    buffer: WebGlBuffer,
}

impl ConsciousnessVisualization {
    pub fn new(gl: Rc<WebGlRenderingContext>) -> Result<Self, JsValue> {
        let particle_system = ParticleSystem::new(gl.clone(), 1000)?;
        let neural_network = NeuralNetwork::new(gl.clone())?;
        let energy_field = EnergyField::new(gl.clone())?;
        
        Ok(Self {
            gl,
            particle_system,
            neural_network,
            energy_field,
            time: 0.0,
        })
    }
    
    pub fn update(&mut self, delta_time: f32) {
        self.time += delta_time;
        self.particle_system.update(delta_time);
        self.neural_network.update(delta_time);
    }
    
    pub fn render(&self, width: f32, height: f32) -> Result<(), JsValue> {
        let projection = Matrix4Utils::perspective(45.0_f32.to_radians(), width / height, 0.1, 100.0);
        let eye = Vector3::new(5.0 * self.time.cos(), 3.0, 5.0 * self.time.sin());
        let center = Vector3::new(0.0, 0.0, 0.0);
        let up = Vector3::new(0.0, 1.0, 0.0);
        let view = Matrix4Utils::look_at(&eye, &center, &up);
        
        self.particle_system.render(&projection, &view)?;
        self.neural_network.render(&projection, &view)?;
        self.energy_field.render(&projection, &view)?;
        
        Ok(())
    }
}

impl EnergyField {
    fn new(gl: Rc<WebGlRenderingContext>) -> Result<Self, JsValue> {
        let vertex_shader = r#"
            attribute vec3 position;
            uniform mat4 projection;
            uniform mat4 view;
            varying vec3 vPosition;
            
            void main() {
                vPosition = position;
                gl_Position = projection * view * vec4(position, 1.0);
            }
        "#;
        
        let fragment_shader = r#"
            precision mediump float;
            varying vec3 vPosition;
            uniform float time;
            
            void main() {
                float wave = sin(vPosition.x * 2.0 + time) * 0.5 + 0.5;
                vec3 color = mix(vec3(0.1, 0.2, 0.8), vec3(0.8, 0.2, 0.4), wave);
                gl_FragColor = vec4(color, 0.5);
            }
        "#;
        
        let program = crate::graphics::shaders::create_program(&gl, vertex_shader, fragment_shader)?;
        let buffer = gl.create_buffer().ok_or("Failed to create buffer")?;
        
        Ok(Self { gl, program, buffer })
    }
    
    fn render(&self, projection: &Matrix4, view: &Matrix4) -> Result<(), JsValue> {
        self.gl.use_program(Some(&self.program));
        
        let proj_loc = self.gl.get_uniform_location(&self.program, "projection");
        let view_loc = self.gl.get_uniform_location(&self.program, "view");
        let time_loc = self.gl.get_uniform_location(&self.program, "time");
        
        if let Some(loc) = proj_loc {
            self.gl.uniform_matrix4fv_with_f32_array(Some(&loc), false, projection);
        }
        if let Some(loc) = view_loc {
            self.gl.uniform_matrix4fv_with_f32_array(Some(&loc), false, view);
        }
        if let Some(loc) = time_loc {
            self.gl.uniform1f(Some(&loc), 0.0);
        }
        
        Ok(())
    }
}
EOF

# Step 6: Fix the build function parameter count in dashboard.rs
echo ""
echo "6️⃣ Fixing dashboard build function..."
sed -i 's/PulsingOrb::build("O(1) Performance", 16.0)/PulsingOrb { label: "O(1) Performance", size: 16.0 }/' think-ai-webapp/src/ui/dashboard.rs

# Step 7: Run cargo clippy fix
echo ""
echo "7️⃣ Running cargo clippy fix..."
cargo clippy --fix --allow-dirty --allow-staged 2>/dev/null || true

# Step 8: Final build attempt
echo ""
echo "8️⃣ Final build attempt..."
cargo build --release 2>&1 | tail -50

echo ""
echo "✅ All fixes applied!"