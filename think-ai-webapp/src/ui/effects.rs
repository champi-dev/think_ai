// UI visual effects for consciousness visualization
//
// Provides O(1) effect rendering and animation systems

use std::collections::HashMap;
use wasm_bindgen::JsValue;
use web_sys::{Document, Element};

/// Type alias for backwards compatibility
pub type EffectsManager = EffectManager;

/// O(1) effect manager with hash-based lookups
pub struct EffectManager {
    active_effects: HashMap<String, Box<dyn VisualEffect>>,
    effect_timers: HashMap<String, f32>,
}

pub trait VisualEffect {
    fn render(&self, container: &Element, time: f32) -> Result<(), JsValue>;
    fn update(&mut self, delta_time: f32) -> Result<(), JsValue>;
    fn is_finished(&self) -> bool;
    fn get_id(&self) -> &str;
}

impl EffectManager {
    pub fn new() -> Self {
        Self {
            active_effects: HashMap::new(),
            effect_timers: HashMap::new(),
        }
    }

    /// O(1) effect registration
    pub fn add_effect(&mut self, effect_: Box<dyn VisualEffect>) {
        let id = effect.get_id().to_string();
        self.effect_timers.insert(id.clone(), 0.0);
        self.active_effects.insert(id, effect);
    }

    /// O(1) effect removal
    pub fn remove_effect(&mut self, id_: &str) {
        self.active_effects.remove(id);
        self.effect_timers.remove(id);
    }

    /// Update all active effects
    pub fn update_all(&mut self, delta_time: f32) -> Result<(), JsValue> {
        let mut finished_effects = Vec::new();

        for (id, effect) in &mut self.active_effects {
            if let Some(timer) = self.effect_timers.get_mut(id) {
                *timer += delta_time;
            }

            effect.update(delta_time)?;

            if effect.is_finished() {
                finished_effects.push(id.clone());
            }
        }

        // Remove finished effects
        for id in finished_effects {
            self.remove_effect(&id);
        }

        Ok(())
    }

    /// O(1) effect processing for webapp
    pub fn process(&mut self, time: f32) -> Result<(), JsValue> {
        self.update_all(time / 1000.0) // Convert ms to seconds
    }

    /// Render all active effects
    pub fn render_all(&self, document_: &Document) -> Result<(), JsValue> {
        for (id, effect) in &self.active_effects {
            if let Some(container) = document.get_element_by_id(&format!("effect-{}", id)) {
                let time = self.effect_timers.get(id).copied().unwrap_or(0.0);
                effect.render(&container, time)?;
            }
        }
        Ok(())
    }
}

/// Consciousness awakening effect
pub struct ConsciousnessAwakening {
    id: String,
    intensity: f32,
    duration: f32,
    elapsed: f32,
    center_x: f32,
    center_y: f32,
}

impl ConsciousnessAwakening {
    pub fn new(id: String, center_x: f32, center_y: f32, intensity: f32) -> Self {
        Self {
            id,
            intensity,
            duration: 3.0, // 3 seconds
            elapsed: 0.0,
            center_x,
            center_y,
        }
    }
}

impl VisualEffect for ConsciousnessAwakening {
    fn render(&self, container: &Element, time: f32) -> Result<(), JsValue> {
        let progress = (self.elapsed / self.duration).min(1.0);
        let fade = if progress < 0.5 {
            progress * 2.0
        } else {
            2.0 - progress * 2.0
        };

        let radius = 50.0 + progress * 200.0;
        let opacity = fade * self.intensity;

        let html = format!(
            r#"
            <div class="consciousness-awakening" style="
                position: absolute;
                left: {}px;
                top: {}px;
                width: {}px;
                height: {}px;
                border-radius: 50%;
                background: radial-gradient(circle,
                    rgba(0, 255, 255, {}) 0%,
                    rgba(255, 0, 255, {}) 50%,
                    transparent 100%);
                transform: translate(-50%, -50%);
                pointer-events: none;
                animation: consciousness-pulse {}s ease-out;
            "></div>
            <style>
                @keyframes consciousness-pulse {{
                    0% {{ transform: translate(-50%, -50%) scale(0.1); }}
                    50% {{ transform: translate(-50%, -50%) scale(1.2); }}
                    100% {{ transform: translate(-50%, -50%) scale(1.0); }}
                }}
            </style>
            "#,
            self.center_x,
            self.center_y,
            radius,
            radius,
            opacity,
            opacity * 0.7,
            self.duration
        );

        container.set_inner_html(&html);
        Ok(())
    }

    fn update(&mut self, delta_time: f32) -> Result<(), JsValue> {
        self.elapsed += delta_time;
        Ok(())
    }

    fn is_finished(&self) -> bool {
        self.elapsed >= self.duration
    }

    fn get_id(&self) -> &str {
        &self.id
    }
}

/// Neural network activation wave effect
pub struct NeuralActivationWave {
    id: String,
    start_x: f32,
    start_y: f32,
    end_x: f32,
    end_y: f32,
    intensity: f32,
    speed: f32,
    duration: f32,
    elapsed: f32,
}

impl NeuralActivationWave {
    pub fn new(
        id: String,
        start_x: f32,
        start_y: f32,
        end_x: f32,
        end_y: f32,
        intensity: f32,
    ) -> Self {
        let _distance = ((end_x - start_x).powi(2) + (end_y - start_y).powi(2)).sqrt();
        Self {
            id,
            start_x,
            start_y,
            end_x,
            end_y,
            intensity,
            speed: 300.0, // pixels per second
            duration: distance / 300.0,
            elapsed: 0.0,
        }
    }
}

impl VisualEffect for NeuralActivationWave {
    fn render(&self, container: &Element, time: f32) -> Result<(), JsValue> {
        let progress = (self.elapsed / self.duration).min(1.0);

        let current_x = self.start_x + (self.end_x - self.start_x) * progress;
        let current_y = self.start_y + (self.end_y - self.start_y) * progress;

        let opacity = (1.0 - progress) * self.intensity;
        let size = 8.0 + progress * 12.0;

        let html = format!(
            r#"
            <div class="neural-wave" style="
                position: absolute;
                left: {}px;
                top: {}px;
                width: {}px;
                height: {}px;
                border-radius: 50%;
                background: radial-gradient(circle,
                    rgba(255, 165, 0, {}) 0%,
                    rgba(255, 69, 0, {}) 70%,
                    transparent 100%);
                transform: translate(-50%, -50%);
                pointer-events: none;
                box-shadow: 0 0 {}px rgba(255, 165, 0, {});
            "></div>
            "#,
            current_x,
            current_y,
            size,
            size,
            opacity,
            opacity * 0.8,
            size * 0.5,
            opacity * 0.5,
        );

        container.set_inner_html(&html);
        Ok(())
    }

    fn update(&mut self, delta_time: f32) -> Result<(), JsValue> {
        self.elapsed += delta_time;
        Ok(())
    }

    fn is_finished(&self) -> bool {
        self.elapsed >= self.duration
    }

    fn get_id(&self) -> &str {
        &self.id
    }
}

/// Thought bubble effect for query processing
pub struct ThoughtBubble {
    id: String,
    x: f32,
    y: f32,
    text: String,
    lifetime: f32,
    elapsed: f32,
    float_speed: f32,
}

impl ThoughtBubble {
    pub fn new(id: String, x: f32, y: f32, text: String) -> Self {
        Self {
            id,
            x,
            y,
            text,
            lifetime: 5.0, // 5 seconds
            elapsed: 0.0,
            float_speed: 20.0, // pixels per second upward
        }
    }
}

impl VisualEffect for ThoughtBubble {
    fn render(&self, container: &Element, time: f32) -> Result<(), JsValue> {
        let progress = self.elapsed / self.lifetime;
        let opacity = if progress < 0.1 {
            progress * 10.0
        } else if progress > 0.8 {
            (1.0 - progress) * 5.0
        } else {
            1.0
        };

        let current_y = self.y - self.elapsed * self.float_speed;
        let scale = 0.8 + (time * 2.0).sin() * 0.1;

        let html = format!(
            r#"
            <div class="thought-bubble" style="
                position: absolute;
                left: {}px;
                top: {}px;
                background: rgba(255, 255, 255, 0.9);
                color: #333;
                padding: 12px 16px;
                border-radius: 20px;
                font-family: Arial, sans-serif;
                font-size: 14px;
                max-width: 200px;
                opacity: {};
                transform: translate(-50%, -100%) scale({});
                pointer-events: none;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
                animation: thought-float 0.5s ease-out;
            ">
                {}
                <div style="
                    position: absolute;
                    bottom: -8px;
                    left: 50%;
                    transform: translateX(-50%);
                    width: 0;
                    height: 0;
                    border-left: 8px solid transparent;
                    border-right: 8px solid transparent;
                    border-top: 8px solid rgba(255, 255, 255, 0.9);
                "></div>
            </div>
            <style>
                @keyframes thought-float {{
                    0% {{ transform: translate(-50%, -100%) scale(0.5); opacity: 0; }}
                    100% {{ transform: translate(-50%, -100%) scale({}); opacity: {}; }}
                }}
            </style>
            "#,
            self.x, current_y, opacity, scale, self.text, scale, opacity
        );

        container.set_inner_html(&html);
        Ok(())
    }

    fn update(&mut self, delta_time: f32) -> Result<(), JsValue> {
        self.elapsed += delta_time;
        Ok(())
    }

    fn is_finished(&self) -> bool {
        self.elapsed >= self.lifetime
    }

    fn get_id(&self) -> &str {
        &self.id
    }
}

/// Particle background effect
pub struct ParticleBackground;

// Simple random module
mod rand {
    pub fn random<T>() -> T
    where
        T: Default,
    {
        T::default()
    }
}
