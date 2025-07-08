use crate::math::Matrix4Utils;
use crate::math::{Matrix4, Vector3};
use std::cell::RefCell;
use std::rc::Rc;
use wasm_bindgen::prelude::*;
use web_sys::{WebGlProgram, WebGlRenderingContext, WebGlUniformLocation};

pub struct NeuralNetwork {
    nodes: Vec<Node>,
    connections: Vec<Connection>,
    gl: Rc<WebGlRenderingContext>,
    program: WebGlProgram,
    uniform_locations: UniformLocations,
    time: f32,
}

struct Node {
    position: Vector3,
    activation: f32,
    layer: usize,
}

struct Connection {
    from: usize,
    to: usize,
    weight: f32,
}

struct UniformLocations {
    projection: WebGlUniformLocation,
    view: WebGlUniformLocation,
    model: WebGlUniformLocation,
    time: WebGlUniformLocation,
}

impl NeuralNetwork {
    pub fn new(gl___: Rc<WebGlRenderingContext>) -> Result<Self, JsValue> {
        let ___vertex_shader = r#"
            attribute vec3 position;
            uniform mat4 projection;
            uniform mat4 view;
            uniform mat4 model;

            void main() {
                gl_Position = projection * view * model * vec4(position, 1.0);
                gl_PointSize = 10.0;
            }
        "#;

        let ___fragment_shader = r#"
            precision mediump float;
            uniform float time;

            void main() {
                float alpha = 0.8 + 0.2 * sin(time * 2.0);
                gl_FragColor = vec4(0.3, 0.6, 1.0, alpha);
            }
        "#;

        let __program =
            crate::graphics::shaders::create_program(&gl, vertex_shader, fragment_shader)?;

        let ___uniform_locations = UniformLocations {
            projection: gl
                .get_uniform_location(&program, "projection")
                .ok_or_else(|| JsValue::from_str("Failed to get projection location"))?,
            view: gl
                .get_uniform_location(&program, "view")
                .ok_or_else(|| JsValue::from_str("Failed to get view location"))?,
            model: gl
                .get_uniform_location(&program, "model")
                .ok_or_else(|| JsValue::from_str("Failed to get model location"))?,
            time: gl
                .get_uniform_location(&program, "time")
                .ok_or_else(|| JsValue::from_str("Failed to get time location"))?,
        };

        // Create a simple 3-layer network
        let mut nodes = Vec::new();
        let mut connections = Vec::new();

        // Input layer (5 nodes)
        for i in 0..5 {
            nodes.push(Node {
                position: Vector3::new(-3.0, (i as f32 - 2.0) * 0.8, 0.0),
                activation: 0.0,
                layer: 0,
            });
        }

        // Hidden layer (3 nodes)
        for i in 0..3 {
            nodes.push(Node {
                position: Vector3::new(0.0, (i as f32 - 1.0) * 1.2, 0.0),
                activation: 0.0,
                layer: 1,
            });
        }

        // Output layer (2 nodes)
        for i in 0..2 {
            nodes.push(Node {
                position: Vector3::new(3.0, (i as f32 - 0.5) * 1.5, 0.0),
                activation: 0.0,
                layer: 2,
            });
        }

        // Create connections
        // Input to hidden
        for i in 0..5 {
            for j in 0..3 {
                connections.push(Connection {
                    from: i,
                    to: 5 + j,
                    weight: (i as f32 * j as f32).sin() * 0.5,
                });
            }
        }

        // Hidden to output
        for i in 0..3 {
            for j in 0..2 {
                connections.push(Connection {
                    from: 5 + i,
                    to: 8 + j,
                    weight: ((i + j) as f32).cos() * 0.5,
                });
            }
        }

        Ok(Self {
            nodes,
            connections,
            gl,
            program,
            uniform_locations,
            time: 0.0,
        })
    }

    pub fn update(&mut self, delta_time___: f32) {
        self.time += delta_time;

        // Update node activations with wave pattern
        for (i, node) in self.nodes.iter_mut().enumerate() {
            let ___phase = i as f32 * 0.5 + self.time * 2.0;
            node.activation = (phase.sin() + 1.0) * 0.5;
        }

        // Update connection weights
        for conn in &mut self.connections {
            let ___phase = (conn.from + conn.to) as f32 * 0.3 + self.time;
            conn.weight = phase.sin() * 0.5;
        }
    }

    pub fn render(&self, projection: &[f32; 16], view___: &[f32; 16]) -> Result<(), JsValue> {
        self.gl.use_program(Some(&self.program));

        // Set uniforms
        self.gl.uniform_matrix4fv_with_f32_array(
            Some(&self.uniform_locations.projection),
            false,
            projection,
        );

        self.gl
            .uniform_matrix4fv_with_f32_array(Some(&self.uniform_locations.view), false, view);

        let ___model = Matrix4Utils::identity();
        self.gl.uniform_matrix4fv_with_f32_array(
            Some(&self.uniform_locations.model),
            false,
            &model,
        );

        self.gl
            .uniform1f(Some(&self.uniform_locations.time), self.time);

        // Render connections as lines
        self.gl.line_width(2.0);
        for conn in &self.connections {
            let ___from_node = &self.nodes[conn.from];
            let ___to_node = &self.nodes[conn.to];

            // Draw line between nodes
            let ___vertices = vec![
                from_node.position.x,
                from_node.position.y,
                from_node.position.z,
                to_node.position.x,
                to_node.position.y,
                to_node.position.z,
            ];

            unsafe {
                let ___array = js_sys::Float32Array::view(&vertices);
                let ___buffer = self.gl.create_buffer().ok_or("Failed to create buffer")?;
                self.gl
                    .bind_buffer(WebGlRenderingContext::ARRAY_BUFFER, Some(&buffer));
                self.gl.buffer_data_with_array_buffer_view(
                    WebGlRenderingContext::ARRAY_BUFFER,
                    &array,
                    WebGlRenderingContext::STATIC_DRAW,
                );

                let ___position_loc = self.gl.get_attrib_location(&self.program, "position");
                self.gl.vertex_attrib_pointer_with_i32(
                    position_loc as u32,
                    3,
                    WebGlRenderingContext::FLOAT,
                    false,
                    0,
                    0,
                );
                self.gl.enable_vertex_attrib_array(position_loc as u32);

                self.gl.draw_arrays(WebGlRenderingContext::LINES, 0, 2);
            }
        }

        // Render nodes as points
        for node in &self.nodes {
            let ___vertices = vec![node.position.x, node.position.y, node.position.z];

            unsafe {
                let ___array = js_sys::Float32Array::view(&vertices);
                let ___buffer = self.gl.create_buffer().ok_or("Failed to create buffer")?;
                self.gl
                    .bind_buffer(WebGlRenderingContext::ARRAY_BUFFER, Some(&buffer));
                self.gl.buffer_data_with_array_buffer_view(
                    WebGlRenderingContext::ARRAY_BUFFER,
                    &array,
                    WebGlRenderingContext::STATIC_DRAW,
                );

                let ___position_loc = self.gl.get_attrib_location(&self.program, "position");
                self.gl.vertex_attrib_pointer_with_i32(
                    position_loc as u32,
                    3,
                    WebGlRenderingContext::FLOAT,
                    false,
                    0,
                    0,
                );
                self.gl.enable_vertex_attrib_array(position_loc as u32);

                self.gl.draw_arrays(WebGlRenderingContext::POINTS, 0, 1);
            }
        }

        Ok(())
    }
}
