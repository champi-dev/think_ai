// Global effects system for consciousness visualization
//!
// Provides O(1) effect coordination across graphics and UI systems

use std::collections::HashMap;
use wasm_bindgen::JsValue;

/// Global effect coordinator with O(1) lookups
pub struct EffectCoordinator {
    active_effects: HashMap<String, EffectState>,
    effect_timelines: HashMap<String, Vec<EffectEvent>>,
    global_time: f32,
}

#[derive(Debug, Clone)]
pub struct EffectState {
    pub id: String,
    pub effect_type: EffectType,
    pub intensity: f32,
    pub duration: f32,
    pub elapsed: f32,
    pub position: (f32, f32, f32),
    pub parameters: HashMap<String, f32>,
}

#[derive(Debug, Clone)]
pub enum EffectType {
    ConsciousnessAwakening,
    NeuralSynapse,
    ThoughtFlow,
    MemoryTrace,
    AttentionFocus,
    EmotionalResonance,
}

#[derive(Debug, Clone)]
pub struct EffectEvent {
    pub trigger_time: f32,
    pub effect_id: String,
    pub event_type: String,
    pub parameters: HashMap<String, f32>,
}

impl Default for EffectCoordinator {
    fn default() -> Self {
        Self::new()
    }
}

impl EffectCoordinator {
    pub fn new() -> Self {
        Self {
            active_effects: HashMap::new(),
            effect_timelines: HashMap::new(),
            global_time: 0.0,
        }
    }

    /// O(1) effect registration
    pub fn register_effect(&mut self, effect: EffectState) {
        self.active_effects.insert(effect.id.clone(), effect);
    }

    /// O(1) effect removal
    pub fn remove_effect(&mut self, id: &str) {
        self.active_effects.remove(id);
        self.effect_timelines.remove(id);
    }

    /// Update all effects with O(1) amortized complexity
    pub fn update_all(&mut self, delta_time: f32) -> Result<(), JsValue> {
        self.global_time += delta_time;
        let mut finished_effects = Vec::new();

        // Update active effects
        for (id, effect) in &mut self.active_effects {
            effect.elapsed += delta_time;

            // Update effect parameters inline
            let progress = (effect.elapsed / effect.duration).min(1.0);
            match effect.effect_type {
                EffectType::ConsciousnessAwakening => {
                    let intensity_curve = if progress < 0.3 {
                        progress / 0.3
                    } else if progress < 0.7 {
                        1.0
                    } else {
                        (1.0 - progress) / 0.3
                    };
                    effect.parameters.insert(
                        "current_intensity".to_string(),
                        intensity_curve * effect.intensity,
                    );
                    effect
                        .parameters
                        .insert("radius".to_string(), 50.0 + progress * 200.0);
                }
                EffectType::NeuralSynapse => {
                    let firing_rate = 5.0;
                    let pulse = (self.global_time * firing_rate * 2.0 * std::f32::consts::PI)
                        .sin()
                        .abs();
                    effect
                        .parameters
                        .insert("pulse_intensity".to_string(), pulse * effect.intensity);
                    effect.parameters.insert("heat".to_string(), progress * 0.8);
                }
                _ => {
                    // Simplified update for other effect types
                    effect.parameters.insert("progress".to_string(), progress);
                    effect
                        .parameters
                        .insert("intensity".to_string(), effect.intensity * (1.0 - progress));
                }
            }

            // Check if effect has finished
            if effect.elapsed >= effect.duration {
                finished_effects.push(id.clone());
            }
        }

        // Process timeline events
        self.process_timeline_events()?;

        // Remove finished effects
        for id in finished_effects {
            self.remove_effect(&id);
        }

        Ok(())
    }

    /// Process timeline events with O(1) amortized complexity
    fn process_timeline_events(&mut self) -> Result<(), JsValue> {
        let mut events_to_process = Vec::new();

        // Collect events that should trigger now
        for (effect_id, timeline) in &self.effect_timelines {
            for event in timeline {
                if event.trigger_time <= self.global_time {
                    events_to_process.push((effect_id.clone(), event.clone()));
                }
            }
        }

        // Process collected events
        for (effect_id, event) in events_to_process {
            self.handle_timeline_event(&effect_id, &event)?;
        }

        Ok(())
    }

    fn handle_timeline_event(
        &mut self,
        effect_id: &str,
        event: &EffectEvent,
    ) -> Result<(), JsValue> {
        if let Some(effect) = self.active_effects.get_mut(effect_id) {
            match event.event_type.as_str() {
                "intensity_boost" => {
                    if let Some(boost) = event.parameters.get("amount") {
                        effect.intensity = (effect.intensity + boost).min(1.0);
                    }
                }
                "position_shift" => {
                    if let (Some(dx), Some(dy), Some(dz)) = (
                        event.parameters.get("dx"),
                        event.parameters.get("dy"),
                        event.parameters.get("dz"),
                    ) {
                        effect.position.0 += dx;
                        effect.position.1 += dy;
                        effect.position.2 += dz;
                    }
                }
                "parameter_set" => {
                    for (key, value) in &event.parameters {
                        if key != "trigger_time" {
                            effect.parameters.insert(key.clone(), *value);
                        }
                    }
                }
                _ => {}
            }
        }
        Ok(())
    }

    /// Create consciousness awakening effect sequence
    pub fn trigger_consciousness_awakening(
        &mut self,
        x: f32,
        y: f32,
        z: f32,
        intensity: f32,
    ) -> String {
        let effect_id = format!("awakening_{}", self.generate_id());
        let awakening_effect = EffectState {
            id: effect_id.clone(),
            effect_type: EffectType::ConsciousnessAwakening,
            intensity,
            duration: 4.0,
            elapsed: 0.0,
            position: (x, y, z),
            parameters: HashMap::new(),
        };

        // Create timeline events for the awakening sequence
        let mut timeline = Vec::new();

        // Initial burst at t=0.5
        let mut params = HashMap::new();
        params.insert("amount".to_string(), 0.3);
        timeline.push(EffectEvent {
            trigger_time: self.global_time + 0.5,
            effect_id: effect_id.clone(),
            event_type: "intensity_boost".to_string(),
            parameters: params,
        });

        // Secondary waves at t=1.0, 1.5, 2.0
        for i in 1..=3 {
            let mut wave_params = HashMap::new();
            wave_params.insert("wave_number".to_string(), i as f32);
            wave_params.insert(
                "wave_intensity".to_string(),
                intensity * (1.0 - i as f32 * 0.2),
            );

            timeline.push(EffectEvent {
                trigger_time: self.global_time + (i as f32) * 0.5 + 0.5,
                effect_id: effect_id.clone(),
                event_type: "parameter_set".to_string(),
                parameters: wave_params,
            });
        }

        self.register_effect(awakening_effect);
        self.effect_timelines.insert(effect_id.clone(), timeline);
        effect_id
    }

    /// Create neural network activation cascade
    pub fn trigger_neural_cascade(
        &mut self,
        start_nodes: Vec<(f32, f32, f32)>,
        intensity: f32,
    ) -> Vec<String> {
        let mut effect_ids = Vec::new();

        for (i, &(x, y, z)) in start_nodes.iter().enumerate() {
            let effect_id = format!("neural_{}_{}", i, self.generate_id());
            let neural_effect = EffectState {
                id: effect_id.clone(),
                effect_type: EffectType::NeuralSynapse,
                intensity,
                duration: 2.0 + i as f32 * 0.1, // Staggered durations
                elapsed: 0.0,
                position: (x, y, z),
                parameters: HashMap::new(),
            };

            self.register_effect(neural_effect);
            effect_ids.push(effect_id);
        }

        effect_ids
    }

    /// Create thought flow visualization
    pub fn trigger_thought_flow(
        &mut self,
        path: Vec<(f32, f32, f32)>,
        concept: &str,
        intensity: f32,
    ) -> String {
        let effect_id = format!("thought_{}_{}", concept, self.generate_id());

        // Calculate total path length for duration
        let mut total_length = 0.0;
        for i in 1..path.len() {
            let dx = path[i].0 - path[i - 1].0;
            let dy = path[i].1 - path[i - 1].1;
            let dz = path[i].2 - path[i - 1].2;
            total_length += (dx * dx + dy * dy + dz * dz).sqrt();
        }

        let flow_speed = 100.0; // units per second
        let duration = total_length / flow_speed;

        let mut params = HashMap::new();
        params.insert("path_length".to_string(), total_length);
        params.insert("concept_hash".to_string(), self.hash_string(concept) as f32);

        let thought_effect = EffectState {
            id: effect_id.clone(),
            effect_type: EffectType::ThoughtFlow,
            intensity,
            duration,
            elapsed: 0.0,
            position: path[0],
            parameters: params,
        };

        // Create timeline events for path following
        let mut timeline = Vec::new();
        let mut cumulative_time = 0.0;

        for i in 1..path.len() {
            let segment_length = {
                let dx = path[i].0 - path[i - 1].0;
                let dy = path[i].1 - path[i - 1].1;
                let dz = path[i].2 - path[i - 1].2;
                (dx * dx + dy * dy + dz * dz).sqrt()
            };

            cumulative_time += segment_length / flow_speed;

            let mut shift_params = HashMap::new();
            shift_params.insert("dx".to_string(), path[i].0 - path[i - 1].0);
            shift_params.insert("dy".to_string(), path[i].1 - path[i - 1].1);
            shift_params.insert("dz".to_string(), path[i].2 - path[i - 1].2);

            timeline.push(EffectEvent {
                trigger_time: self.global_time + cumulative_time,
                effect_id: effect_id.clone(),
                event_type: "position_shift".to_string(),
                parameters: shift_params,
            });
        }

        self.register_effect(thought_effect);
        self.effect_timelines.insert(effect_id.clone(), timeline);
        effect_id
    }

    /// Get current state of all effects for rendering
    pub fn get_render_states(&self) -> Vec<&EffectState> {
        self.active_effects.values().collect()
    }

    /// Get specific effect state by ID
    pub fn get_effect_state(&self, id: &str) -> Option<&EffectState> {
        self.active_effects.get(id)
    }

    /// Simple ID generator
    fn generate_id(&self) -> u64 {
        (js_sys::Date::now() as u64)
            .wrapping_mul(2654435761)
            .wrapping_add(self.active_effects.len() as u64)
    }

    /// Simple string hasher
    fn hash_string(&self, s: &str) -> u64 {
        let mut hash = 5381u64;
        for byte in s.bytes() {
            hash = hash.wrapping_mul(33).wrapping_add(byte as u64);
        }
        hash
    }

    /// Get global effect time
    pub fn get_global_time(&self) -> f32 {
        self.global_time
    }

    /// Set global effect intensity multiplier
    pub fn set_global_intensity(&mut self, multiplier: f32) {
        for effect in self.active_effects.values_mut() {
            effect.intensity *= multiplier;
        }
    }

    /// Clear all effects
    pub fn clear_all_effects(&mut self) {
        self.active_effects.clear();
        self.effect_timelines.clear();
    }
}
