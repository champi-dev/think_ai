use super::neural_network::NeuralNetwork;
use super::particles::ParticleSystem;
use crate::math::{Matrix4Utils, Vector3};
use std::rc::Rc;
use wasm_bindgen::prelude::*;
use web_sys::{WebGlBuffer, WebGlProgram, WebGlRenderingContext};

pub struct ConsciousnessVisualization {
    _gl: Rc<WebGlRenderingContext>,
    particle_system: ParticleSystem,
    neural_network: NeuralNetwork,
    energy_field: EnergyField,
    time: f32,
}

struct EnergyField {
    gl: Rc<WebGlRenderingContext>,
    program: WebGlProgram,
    _buffer: WebGlBuffer,
}

impl ConsciousnessVisualization {
    pub fn new(gl: Rc<WebGlRenderingContext>) -> Result<Self, JsValue> {
        let particle_system = ParticleSystem::new(gl.clone(), 1000)?;
        let neural_network = NeuralNetwork::new(gl.clone())?;
        let energy_field = EnergyField::new(gl.clone())?;

        Ok(Self {
            _gl: gl,
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
        let projection =
            Matrix4Utils::perspective(45.0_f32.to_radians(), width / height, 0.1, 100.0);
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
            uniform float time;
            varying vec3 vPosition;

            void main() {
                float wave = sin(vPosition.x * 2.0 + time) * 0.5 + 0.5;
                vec3 color = mix(vec3(0.1, 0.2, 0.8), vec3(0.8, 0.2, 0.4), wave);
                gl_FragColor = vec4(color, 0.5);
            }
        "#;

        let program =
            crate::graphics::shaders::create_program(&gl, vertex_shader, fragment_shader)?;
        let buffer = gl.create_buffer().ok_or("Failed to create buffer")?;

        Ok(Self {
            gl,
            program,
            _buffer: buffer,
        })
    }

    fn render(&self, projection: &[f32; 16], view: &[f32; 16]) -> Result<(), JsValue> {
        self.gl.use_program(Some(&self.program));

        let proj_loc = self.gl.get_uniform_location(&self.program, "projection");
        let view_loc = self.gl.get_uniform_location(&self.program, "view");
        let time_loc = self.gl.get_uniform_location(&self.program, "time");

        if let Some(loc) = proj_loc {
            self.gl
                .uniform_matrix4fv_with_f32_array(Some(&loc), false, projection);
        }

        if let Some(loc) = view_loc {
            self.gl
                .uniform_matrix4fv_with_f32_array(Some(&loc), false, view);
        }

        if let Some(loc) = time_loc {
            self.gl.uniform1f(Some(&loc), 0.0);
        }

        Ok(())
    }
}
