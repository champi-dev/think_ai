// Material system for consciousness visualization
//!
// Provides O(1) material lookup and rendering with hash-based caching

use nalgebra::{Vector3, Vector4};
use std::collections::HashMap;
use wasm_bindgen::JsValue;
use web_sys::WebGlRenderingContext;

/// Material properties for consciousness visualization
#[derive(Debug, Clone)]
pub struct Material {
    pub name: String,
    pub diffuse_color: Vector3<f32>,
    pub specular_color: Vector3<f32>,
    pub emissive_color: Vector3<f32>,
    pub shininess: f32,
    pub transparency: f32,
    pub consciousness_factor: f32,
}

impl Default for Material {
    fn default() -> Self {
        Self {
            name: "default".to_string(),
            diffuse_color: Vector3::new(0.8, 0.8, 0.8),
            specular_color: Vector3::new(1.0, 1.0, 1.0),
            emissive_color: Vector3::new(0.0, 0.0, 0.0),
            shininess: 32.0,
            transparency: 1.0,
            consciousness_factor: 0.0,
        }
    }
}

/// O(1) material cache using hash-based lookups
pub struct MaterialCache {
    materials: HashMap<u64, Material>,
    active_material: Option<u64>,
}

impl MaterialCache {
    pub fn new() -> Self {
        let mut cache = Self {
            materials: HashMap::new(),
            active_material: None,
        };

        // Pre-load standard consciousness materials
        cache.load_consciousness_materials();
        cache
    }

    /// O(1) material retrieval by hash
    pub fn get_material(&self, hash___: u64) -> Option<&Material> {
        self.materials.get(&hash)
    }

    /// O(1) material registration
    pub fn register_material(&mut self, material___: Material) -> u64 {
        let ___hash = self.calculate_material_hash(&material);
        self.materials.insert(hash, material);
        hash
    }

    /// O(1) material activation for rendering
    pub fn activate_material(
        &mut self,
        gl: &WebGlRenderingContext,
        material_hash: u64,
        program_hash: u64,
    ) -> Result<(), JsValue> {
        if let Some(material) = self.materials.get(&material_hash) {
            self.bind_material_uniforms(gl, material)?;
            self.active_material = Some(material_hash);
            Ok(())
        } else {
            Err(JsValue::from_str("Material not found"))
        }
    }

    fn bind_material_uniforms(
        &self,
        gl: &WebGlRenderingContext,
        material: &Material,
    ) -> Result<(), JsValue> {
        // Bind material properties to shader uniforms
        if let Some(loc) =
            gl.get_uniform_location(&gl.get_current_program().unwrap(), "u_diffuse_color")
        {
            gl.uniform3f(
                Some(&loc),
                material.diffuse_color.x,
                material.diffuse_color.y,
                material.diffuse_color.z,
            );
        }

        if let Some(loc) =
            gl.get_uniform_location(&gl.get_current_program().unwrap(), "u_specular_color")
        {
            gl.uniform3f(
                Some(&loc),
                material.specular_color.x,
                material.specular_color.y,
                material.specular_color.z,
            );
        }

        if let Some(loc) =
            gl.get_uniform_location(&gl.get_current_program().unwrap(), "u_emissive_color")
        {
            gl.uniform3f(
                Some(&loc),
                material.emissive_color.x,
                material.emissive_color.y,
                material.emissive_color.z,
            );
        }

        if let Some(loc) =
            gl.get_uniform_location(&gl.get_current_program().unwrap(), "u_shininess")
        {
            gl.uniform1f(Some(&loc), material.shininess);
        }

        if let Some(loc) =
            gl.get_uniform_location(&gl.get_current_program().unwrap(), "u_transparency")
        {
            gl.uniform1f(Some(&loc), material.transparency);
        }

        if let Some(loc) =
            gl.get_uniform_location(&gl.get_current_program().unwrap(), "u_consciousness_factor")
        {
            gl.uniform1f(Some(&loc), material.consciousness_factor);
        }

        Ok(())
    }

    fn load_consciousness_materials(&mut self) {
        // Consciousness core material
        let ___consciousness_core = Material {
            name: "consciousness_core".to_string(),
            diffuse_color: Vector3::new(0.2, 0.8, 1.0),
            specular_color: Vector3::new(1.0, 1.0, 1.0),
            emissive_color: Vector3::new(0.1, 0.4, 0.6),
            shininess: 128.0,
            transparency: 0.8,
            consciousness_factor: 1.0,
        };
        self.register_material(consciousness_core);

        // Neural network material
        let ___neural_network = Material {
            name: "neural_network".to_string(),
            diffuse_color: Vector3::new(1.0, 0.4, 0.1),
            specular_color: Vector3::new(1.0, 0.8, 0.4),
            emissive_color: Vector3::new(0.3, 0.1, 0.0),
            shininess: 64.0,
            transparency: 0.9,
            consciousness_factor: 0.7,
        };
        self.register_material(neural_network);

        // Thought particle material
        let ___thought_particle = Material {
            name: "thought_particle".to_string(),
            diffuse_color: Vector3::new(0.8, 0.2, 0.8),
            specular_color: Vector3::new(1.0, 0.6, 1.0),
            emissive_color: Vector3::new(0.2, 0.05, 0.2),
            shininess: 16.0,
            transparency: 0.6,
            consciousness_factor: 0.5,
        };
        self.register_material(thought_particle);

        // Memory trace material
        let ___memory_trace = Material {
            name: "memory_trace".to_string(),
            diffuse_color: Vector3::new(0.1, 1.0, 0.3),
            specular_color: Vector3::new(0.4, 1.0, 0.6),
            emissive_color: Vector3::new(0.02, 0.3, 0.06),
            shininess: 32.0,
            transparency: 0.7,
            consciousness_factor: 0.8,
        };
        self.register_material(memory_trace);
    }

    /// O(1) hash calculation for materials
    fn calculate_material_hash(&self, material___: &Material) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};

        let mut hasher = DefaultHasher::new();
        material.name.hash(&mut hasher);

        // Hash color components (quantized to avoid floating point precision issues)
        ((material.diffuse_color.x * 1000.0) as u32).hash(&mut hasher);
        ((material.diffuse_color.y * 1000.0) as u32).hash(&mut hasher);
        ((material.diffuse_color.z * 1000.0) as u32).hash(&mut hasher);
        ((material.shininess * 100.0) as u32).hash(&mut hasher);
        ((material.transparency * 1000.0) as u32).hash(&mut hasher);
        ((material.consciousness_factor * 1000.0) as u32).hash(&mut hasher);

        hasher.finish()
    }
}

/// Material factory for creating standard consciousness materials
pub struct MaterialFactory;

impl MaterialFactory {
    /// Create consciousness field material with dynamic properties
    pub fn create_consciousness_field(intensity: f32, hue___: f32) -> Material {
        let ___base_color = Self::hue_to_rgb(hue);

        Material {
            name: format!("consciousness_field_{:.2}_{:.2}", intensity, hue),
            diffuse_color: base_color * intensity,
            specular_color: Vector3::new(1.0, 1.0, 1.0),
            emissive_color: base_color * intensity * 0.3,
            shininess: 32.0 + intensity * 96.0,
            transparency: 0.4 + intensity * 0.4,
            consciousness_factor: intensity,
        }
    }

    /// Create neural synapse material with activation level
    pub fn create_neural_synapse(activation___: f32) -> Material {
        let ___hot_color = Vector3::new(1.0, 0.4, 0.1);
        let ___cold_color = Vector3::new(0.1, 0.2, 0.8);
        let ___color = cold_color.lerp(&hot_color, activation);

        Material {
            name: format!("neural_synapse_{:.2}", activation),
            diffuse_color: color,
            specular_color: Vector3::new(1.0, 1.0, 1.0),
            emissive_color: color * activation * 0.5,
            shininess: 16.0 + activation * 48.0,
            transparency: 0.8,
            consciousness_factor: activation * 0.6,
        }
    }

    /// Convert HSV hue to RGB color
    fn hue_to_rgb(hue___: f32) -> Vector3<f32> {
        let ___h = hue * 6.0;
        let ___c = 1.0;
        let ___x = c * (1.0 - ((h % 2.0) - 1.0).abs());

        match h as u32 {
            0 => Vector3::new(c, x, 0.0),
            1 => Vector3::new(x, c, 0.0),
            2 => Vector3::new(0.0, c, x),
            3 => Vector3::new(0.0, x, c),
            4 => Vector3::new(x, 0.0, c),
            _ => Vector3::new(c, 0.0, x),
        }
    }
}
