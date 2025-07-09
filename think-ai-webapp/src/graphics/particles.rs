use std::rc::Rc;
use wasm_bindgen::prelude::*;
use web_sys::{WebGlBuffer, WebGlProgram, WebGlRenderingContext};

pub struct ParticleSystem {
    particles: Vec<Particle>,
    gl: Rc<WebGlRenderingContext>,
    program: WebGlProgram,
    position_buffer: WebGlBuffer,
    time: f32,
}

struct Particle {
    position: [f32; 3],
    velocity: [f32; 3],
    life: f32,
    size: f32,
}

impl ParticleSystem {
    pub fn new(gl: Rc<WebGlRenderingContext>, count: usize) -> Result<Self, JsValue> {
        let vertex_shader = r#"
            attribute vec3 position;
            attribute float size;
            uniform mat4 projection;
            uniform mat4 view;
            varying float vLife;
            void main() {
                gl_Position = projection * view * vec4(position, 1.0);
                gl_PointSize = size;
                vLife = size / 10.0;
            }
        "#;

        let fragment_shader = r#"
            precision mediump float;
            varying float vLife;

            void main() {
                vec2 coord = gl_PointCoord - vec2(0.5);
                if (length(coord) > 0.5) discard;
                float alpha = vLife * (1.0 - length(coord) * 2.0);
                gl_FragColor = vec4(0.3, 0.6, 1.0, alpha);
            }
        "#;

        let program =
            crate::graphics::shaders::create_program(&gl, vertex_shader, fragment_shader)?;
        let position_buffer = gl.create_buffer().ok_or("Failed to create buffer")?;

        let mut particles = Vec::with_capacity(count);
        for i in 0..count {
            particles.push(Particle {
                position: [
                    (i as f32 * 0.618).sin() * 5.0,
                    (i as f32 * 0.382).cos() * 5.0,
                    (i as f32 * 0.236).sin() * 5.0,
                ],
                velocity: [
                    (i as f32 * 0.1).sin() * 0.1,
                    0.05,
                    (i as f32 * 0.1).cos() * 0.1,
                ],
                life: 1.0,
                size: 10.0,
            });
        }

        Ok(Self {
            particles,
            gl,
            program,
            position_buffer,
            time: 0.0,
        })
    }

    pub fn update(&mut self, delta_time: f32) {
        self.time += delta_time;

        for particle in &mut self.particles {
            // Update position
            particle.position[0] += particle.velocity[0] * delta_time;
            particle.position[1] += particle.velocity[1] * delta_time;
            particle.position[2] += particle.velocity[2] * delta_time;

            // Update life
            particle.life -= delta_time * 0.2;
            if particle.life <= 0.0 {
                particle.life = 1.0;
                particle.position[1] = -5.0;
            }

            // Add some wave motion
            particle.position[0] += (self.time * 2.0).sin() * 0.01;
        }
    }

    pub fn render(&self, projection: &[f32; 16], view: &[f32; 16]) -> Result<(), JsValue> {
        self.gl.use_program(Some(&self.program));

        // Set uniforms
        let proj_loc = self.gl.get_uniform_location(&self.program, "projection");
        let view_loc = self.gl.get_uniform_location(&self.program, "view");

        if let Some(loc) = proj_loc {
            self.gl
                .uniform_matrix4fv_with_f32_array(Some(&loc), false, projection);
        }

        if let Some(loc) = view_loc {
            self.gl
                .uniform_matrix4fv_with_f32_array(Some(&loc), false, view);
        }

        // Create position data
        let mut positions = Vec::with_capacity(self.particles.len() * 3);
        for particle in &self.particles {
            positions.extend_from_slice(&particle.position);
        }

        // Upload position data
        unsafe {
            let array = js_sys::Float32Array::view(&positions);
            self.gl.bind_buffer(
                WebGlRenderingContext::ARRAY_BUFFER,
                Some(&self.position_buffer),
            );
            self.gl.buffer_data_with_array_buffer_view(
                WebGlRenderingContext::ARRAY_BUFFER,
                &array,
                WebGlRenderingContext::DYNAMIC_DRAW,
            );
        }

        // Set attributes
        let position_loc = self.gl.get_attrib_location(&self.program, "position");
        if position_loc >= 0 {
            self.gl.vertex_attrib_pointer_with_i32(
                position_loc as u32,
                3,
                WebGlRenderingContext::FLOAT,
                false,
                0,
                0,
            );
            self.gl.enable_vertex_attrib_array(position_loc as u32);
        }

        // Draw particles
        self.gl.draw_arrays(
            WebGlRenderingContext::POINTS,
            0,
            self.particles.len() as i32,
        );

        Ok(())
    }
}
