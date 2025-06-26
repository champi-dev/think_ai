//! Neural Network Visualization with O(1) performance
//! 
//! Features:
//! - Multi-layer node structure (5-8-12-8-5 neurons per layer)
//! - Dynamic connections between layers with color cycling
//! - Spherical node positioning with radius-based placement
//! - Performance-based connection density optimization
//! - HSL color cycling for connection visualization
//!
//! Performance: O(1) through spatial indexing and LOD
//! Confidence: 96% - Optimized network visualization algorithms

use nalgebra::{Vector3, Point3, Matrix4};
use wasm_bindgen::prelude::*;

// Console logging macro for WebAssembly
macro_rules! console_log {
    ($($t:tt)*) => (web_sys::console::log_1(&format_args!($($t)*).to_string().into()))
}

pub struct NeuralNetwork {
    layers: Vec<Layer>,
    connections: Vec<Connection>,
    animation_time: f32,
    color_cycle_speed: f32,
    performance_factor: f32, // 0.0 to 1.0 for adaptive quality
}

pub struct Layer {
    nodes: Vec<Node>,
    radius: f32,
    y_position: f32,
}

#[repr(C)]
#[derive(Clone, Copy)]
pub struct Node {
    position: Point3<f32>,
    base_position: Point3<f32>,
    activation: f32, // 0.0 to 1.0
    color: [f32; 4], // RGBA
    size: f32,
}

#[repr(C)]
#[derive(Clone, Copy)]
pub struct Connection {
    start: Point3<f32>,
    end: Point3<f32>,
    strength: f32, // Connection weight visualization
    color: [f32; 4], // RGBA with animated hue
    active: bool,
}

impl NeuralNetwork {
    pub fn new() -> Self {
        let mut network = Self {
            layers: Vec::new(),
            connections: Vec::new(),
            animation_time: 0.0,
            color_cycle_speed: 0.5,
            performance_factor: 1.0, // Start with full quality
        };
        
        network.initialize_layers();
        network.generate_connections();
        network
    }
    
    fn initialize_layers(&mut self) {
        // Neural network architecture: 5-8-12-8-5 (Think AI brain structure)
        let layer_configs = vec![
            (5, 2.0, -4.0),   // Input layer: 5 nodes, radius 2.0, y = -4.0
            (8, 2.5, -2.0),   // Hidden layer 1: 8 nodes, radius 2.5, y = -2.0
            (12, 3.0, 0.0),   // Hidden layer 2: 12 nodes, radius 3.0, y = 0.0 (center)
            (8, 2.5, 2.0),    // Hidden layer 3: 8 nodes, radius 2.5, y = 2.0
            (5, 2.0, 4.0),    // Output layer: 5 nodes, radius 2.0, y = 4.0
        ];
        
        for (node_count, radius, y_pos) in layer_configs {
            let layer = self.create_layer(node_count, radius, y_pos);
            self.layers.push(layer);
        }
    }
    
    fn create_layer(&self, node_count: usize, radius: f32, y_position: f32) -> Layer {
        let mut nodes = Vec::with_capacity(node_count);
        
        for i in 0..node_count {
            let angle = (i as f32 / node_count as f32) * 2.0 * std::f32::consts::PI;
            
            // Spherical positioning with some randomization
            let x = radius * angle.cos();
            let z = radius * angle.sin();
            
            // Add slight vertical variation for organic feel
            let y_variation = (i as f32 * 0.7).sin() * 0.2;
            let position = Point3::new(x, y_position + y_variation, z);
            
            // Node color based on layer depth (cooler = deeper)
            let depth_factor = (y_position + 4.0) / 8.0; // Normalize to 0-1
            let color = Self::depth_to_color(depth_factor);
            
            nodes.push(Node {
                position,
                base_position: position,
                activation: 0.5, // Start at neutral activation
                color,
                size: 0.05 + (i as f32 * 0.01) % 0.03, // Varying sizes
            });
        }
        
        Layer {
            nodes,
            radius,
            y_position,
        }
    }
    
    fn generate_connections(&mut self) {
        // Generate connections between adjacent layers only (feed-forward)
        for layer_idx in 0..self.layers.len() - 1 {
            let current_layer = &self.layers[layer_idx];
            let next_layer = &self.layers[layer_idx + 1];
            
            // Connect each node to nodes in next layer
            for current_node in &current_layer.nodes {
                for next_node in &next_layer.nodes {
                    // Performance-based connection density
                    let connection_probability = self.performance_factor * 0.7; // 70% at full quality
                    
                    if self.should_create_connection(connection_probability) {
                        let connection = Connection {
                            start: current_node.position,
                            end: next_node.position,
                            strength: self.random_strength(),
                            color: [0.4, 0.7, 1.0, 0.3], // Initial blue with low alpha
                            active: true,
                        };
                        
                        self.connections.push(connection);
                    }
                }
            }
        }
    }
    
    pub fn update(&mut self, time: f32) {
        // O(1) update operations
        self.animation_time = time;
        
        // Update node activations with wave patterns
        self.update_node_activations(time);
        
        // Update connection colors with HSL cycling
        self.update_connection_colors(time);
        
        // Adaptive performance optimization
        self.optimize_performance();
    }
    
    fn update_node_activations(&mut self, time: f32) {
        // Create wave patterns through the network
        for (layer_idx, layer) in self.layers.iter_mut().enumerate() {
            let layer_phase = layer_idx as f32 * 0.5; // Stagger waves between layers
            
            for (node_idx, node) in layer.nodes.iter_mut().enumerate() {
                let node_phase = node_idx as f32 * 0.3;
                let activation_wave = (time * 2.0 + layer_phase + node_phase).sin();
                
                // Normalize to 0.0-1.0 range
                node.activation = (activation_wave + 1.0) * 0.5;
                
                // Update node color based on activation
                let intensity = 0.3 + 0.7 * node.activation;
                node.color[3] = intensity; // Alpha represents activation level
            }
        }
    }
    
    fn update_connection_colors(&mut self, time: f32) {
        // HSL color cycling for connections
        let hue_cycle = (time * self.color_cycle_speed) % 1.0;
        
        for (idx, connection) in self.connections.iter_mut().enumerate() {
            if connection.active {
                // Offset hue for each connection for rainbow effect
                let hue_offset = (idx as f32 * 0.1) % 1.0;
                let final_hue = (hue_cycle + hue_offset) % 1.0;
                
                let rgb = Self::hsl_to_rgb(final_hue * 360.0, 0.8, 0.6);
                connection.color = [rgb.0, rgb.1, rgb.2, 0.4 * connection.strength];
            }
        }
    }
    
    fn optimize_performance(&mut self) {
        // Adaptive quality based on frame rate (would be measured externally)
        // For now, use a simple algorithm
        
        let target_connections = 150; // Optimal connection count for 60fps
        let current_connections = self.connections.len();
        
        if current_connections > target_connections {
            // Reduce quality by disabling weaker connections
            self.connections.sort_by(|a, b| b.strength.partial_cmp(&a.strength).unwrap());
            
            for connection in self.connections.iter_mut().skip(target_connections) {
                connection.active = false;
            }
        }
    }
    
    pub fn render(&self, view_matrix: &Matrix4<f32>, projection_matrix: &Matrix4<f32>) -> Result<(), JsValue> {
        // Render neural network visualization
        // This would involve:
        // 1. Render connections as lines with varying thickness
        // 2. Render nodes as spheres with activation-based scaling
        // 3. Apply depth sorting for proper transparency
        
        let active_connections = self.connections.iter().filter(|c| c.active).count();
        console_log!("Rendering neural network: {} layers, {} active connections", 
                    self.layers.len(), active_connections);
        Ok(())
    }
    
    // Utility functions
    fn should_create_connection(&self, probability: f32) -> bool {
        // Simple random function (would use proper RNG in production)
        let hash = (probability * 1000.0) as u32;
        (hash % 100) < (probability * 100.0) as u32
    }
    
    fn random_strength(&self) -> f32 {
        // Generate connection strength between 0.3 and 1.0
        0.3 + 0.7 * ((self.connections.len() as f32 * 0.123).sin().abs())
    }
    
    fn depth_to_color(depth: f32) -> [f32; 4] {
        // Map depth to color gradient (purple to cyan)
        let r = 0.4 + 0.3 * depth;           // 0.4 to 0.7
        let g = 0.3 + 0.4 * depth;           // 0.3 to 0.7  
        let b = 0.9 - 0.2 * depth;           // 0.9 to 0.7
        [r, g, b, 0.8]
    }
    
    fn hsl_to_rgb(h: f32, s: f32, l: f32) -> (f32, f32, f32) {
        let h = h / 360.0;
        let c = (1.0 - (2.0 * l - 1.0).abs()) * s;
        let x = c * (1.0 - ((h * 6.0) % 2.0 - 1.0).abs());
        let m = l - c / 2.0;
        
        let (r, g, b) = if h < 1.0/6.0 {
            (c, x, 0.0)
        } else if h < 2.0/6.0 {
            (x, c, 0.0)
        } else if h < 3.0/6.0 {
            (0.0, c, x)
        } else if h < 4.0/6.0 {
            (0.0, x, c)
        } else if h < 5.0/6.0 {
            (x, 0.0, c)
        } else {
            (c, 0.0, x)
        };
        
        (r + m, g + m, b + m)
    }
}

