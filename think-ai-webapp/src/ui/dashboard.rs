//! Consciousness dashboard for monitoring and control
//! 
//! Provides O(1) dashboard rendering with real-time metrics visualization

use wasm_bindgen::JsValue;
use web_sys::{Document, Element, HtmlElement, Window};
use std::collections::HashMap;
use super::components::{ComponentRegistry, ConsciousnessMetrics, QueryInterface};
use super::effects::EffectManager;

/// Type alias for backwards compatibility
pub type IntelligenceDashboard = ConsciousnessDashboard;

/// Main consciousness dashboard controller
pub struct ConsciousnessDashboard {
    pub component_registry: ComponentRegistry,
    pub effect_manager: EffectManager,
    pub metrics: ConsciousnessMetrics,
    pub query_interface: QueryInterface,
    pub layout_config: DashboardLayout,
    pub is_initialized: bool,
}

#[derive(Debug, Clone)]
pub struct DashboardLayout {
    pub canvas_width: f32,
    pub canvas_height: f32,
    pub sidebar_width: f32,
    pub header_height: f32,
}

impl Default for DashboardLayout {
    fn default() -> Self {
        Self {
            canvas_width: 800.0,
            canvas_height: 600.0,
            sidebar_width: 300.0,
            header_height: 60.0,
        }
    }
}

impl ConsciousnessDashboard {
    pub fn new() -> Self {
        let mut dashboard = Self {
            component_registry: ComponentRegistry::new(),
            effect_manager: EffectManager::new(),
            metrics: ConsciousnessMetrics::new("consciousness-metrics".to_string()),
            query_interface: QueryInterface::new("query-interface".to_string()),
            layout_config: DashboardLayout::default(),
            is_initialized: false,
        };

        // Register components
        dashboard.component_registry.register_component(Box::new(dashboard.metrics.clone()));
        dashboard.component_registry.register_component(Box::new(dashboard.query_interface.clone()));

        dashboard
    }

    /// Initialize dashboard in the DOM
    pub fn initialize(&mut self, document: &Document) -> Result<(), JsValue> {
        if self.is_initialized {
            return Ok(());
        }

        // Create main dashboard container
        self.create_dashboard_layout(document)?;
        
        // Initialize 3D canvas
        self.initialize_3d_canvas(document)?;
        
        // Initialize control panels
        self.initialize_control_panels(document)?;
        
        // Apply dashboard styling
        self.apply_dashboard_styles(document)?;

        self.is_initialized = true;
        Ok(())
    }

    /// Update dashboard with new consciousness data
    pub fn update_consciousness_data(
        &mut self,
        consciousness_level: f32,
        neural_activity: f32,
        memory_utilization: f32,
        processing_speed: f32,
    ) -> Result<(), JsValue> {
        self.metrics.update_metrics(
            consciousness_level,
            neural_activity,
            memory_utilization,
            processing_speed,
        );

        // Trigger visual effects based on consciousness level
        if consciousness_level > 0.8 {
            self.trigger_high_consciousness_effects();
        }

        Ok(())
    }

    /// Render complete dashboard
    pub fn render(&self, document: &Document) -> Result<(), JsValue> {
        if !self.is_initialized {
            return Err(JsValue::from_str("Dashboard not initialized"));
        }

        // Render all components
        self.component_registry.render_all(document)?;
        
        // Render visual effects
        self.effect_manager.render_all(document)?;

        Ok(())
    }

    /// Update dashboard animations and effects
    pub fn update(&mut self, delta_time: f32) -> Result<(), JsValue> {
        self.effect_manager.update_all(delta_time)?;
        Ok(())
    }

    fn create_dashboard_layout(&self, document: &Document) -> Result<(), JsValue> {
        let body = document.body().ok_or("No body element")?;
        
        let dashboard_html = format!(
            r#"
            <div id="consciousness-dashboard" style="
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
                color: #ffffff;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                overflow: hidden;
                z-index: 1000;
            ">
                <!-- Header -->
                <div id="dashboard-header" style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: {}px;
                    background: rgba(0, 0, 0, 0.7);
                    border-bottom: 2px solid #00ffff;
                    display: flex;
                    align-items: center;
                    padding: 0 20px;
                    box-sizing: border-box;
                ">
                    <h1 style="
                        margin: 0;
                        font-size: 24px;
                        background: linear-gradient(45deg, #00ffff, #ff00ff);
                        -webkit-background-clip: text;
                        -webkit-text-fill-color: transparent;
                        background-clip: text;
                    ">Think AI Consciousness Dashboard</h1>
                    <div style="flex: 1;"></div>
                    <div id="status-indicator" style="
                        display: flex;
                        align-items: center;
                        gap: 8px;
                    ">
                        <div style="
                            width: 12px;
                            height: 12px;
                            border-radius: 50%;
                            background: #00ff00;
                            animation: pulse 2s infinite;
                        "></div>
                        <span>Active</span>
                    </div>
                </div>

                <!-- Main Canvas Area -->
                <div id="canvas-container" style="
                    position: absolute;
                    top: {}px;
                    left: 0;
                    width: calc(100vw - {}px);
                    height: calc(100vh - {}px);
                    background: rgba(0, 0, 0, 0.3);
                    border-right: 2px solid #00ffff;
                ">
                    <canvas id="consciousness-canvas" style="
                        width: 100%;
                        height: 100%;
                        display: block;
                    "></canvas>
                    <div id="canvas-overlay" style="
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        pointer-events: none;
                    "></div>
                </div>

                <!-- Control Sidebar -->
                <div id="control-sidebar" style="
                    position: absolute;
                    top: {}px;
                    right: 0;
                    width: {}px;
                    height: calc(100vh - {}px);
                    background: rgba(0, 0, 0, 0.8);
                    border-left: 2px solid #00ffff;
                    padding: 20px;
                    box-sizing: border-box;
                    overflow-y: auto;
                ">
                    <div id="consciousness-metrics" style="margin-bottom: 20px;"></div>
                    <div id="query-interface" style="margin-bottom: 20px;"></div>
                    <div id="effect-controls" style="margin-bottom: 20px;"></div>
                </div>

                <!-- Effect Layer -->
                <div id="effect-layer" style="
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 1001;
                "></div>
            </div>
            "#,
            self.layout_config.header_height,
            self.layout_config.header_height,
            self.layout_config.sidebar_width,
            self.layout_config.header_height,
            self.layout_config.header_height,
            self.layout_config.sidebar_width,
            self.layout_config.header_height,
        );

        body.set_inner_html(&dashboard_html);
        Ok(())
    }

    fn initialize_3d_canvas(&self, document: &Document) -> Result<(), JsValue> {
        let canvas = document
            .get_element_by_id("consciousness-canvas")
            .ok_or("Canvas element not found")?;

        // Set canvas dimensions
        canvas.set_attribute("width", &self.layout_config.canvas_width.to_string())?;
        canvas.set_attribute("height", &self.layout_config.canvas_height.to_string())?;

        Ok(())
    }

    fn initialize_control_panels(&self, document: &Document) -> Result<(), JsValue> {
        // Create effect controls
        if let Some(effect_controls) = document.get_element_by_id("effect-controls") {
            let controls_html = r#"
                <div class="control-panel">
                    <h3>Visual Effects</h3>
                    <div class="control-group">
                        <label>Consciousness Intensity:</label>
                        <input type="range" id="consciousness-intensity" min="0" max="1" step="0.1" value="0.5">
                    </div>
                    <div class="control-group">
                        <label>Neural Activity:</label>
                        <input type="range" id="neural-activity" min="0" max="1" step="0.1" value="0.7">
                    </div>
                    <div class="control-group">
                        <label>Particle Density:</label>
                        <input type="range" id="particle-density" min="0" max="1" step="0.1" value="0.6">
                    </div>
                    <div class="control-group">
                        <button id="trigger-awakening">Trigger Awakening</button>
                        <button id="reset-effects">Reset Effects</button>
                    </div>
                </div>
            "#;
            effect_controls.set_inner_html(controls_html);
        }

        Ok(())
    }

    fn apply_dashboard_styles(&self, document: &Document) -> Result<(), JsValue> {
        let style_element = document.create_element("style")?;
        style_element.set_inner_html(
            r#"
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }

            .control-panel {
                background: rgba(0, 20, 40, 0.6);
                border: 1px solid #00ffff;
                border-radius: 8px;
                padding: 16px;
                margin-bottom: 16px;
            }

            .control-panel h3 {
                margin: 0 0 16px 0;
                color: #00ffff;
                font-size: 16px;
            }

            .control-group {
                margin-bottom: 12px;
            }

            .control-group label {
                display: block;
                margin-bottom: 4px;
                font-size: 12px;
                color: #cccccc;
            }

            .control-group input[type="range"] {
                width: 100%;
                height: 4px;
                background: #333;
                border-radius: 2px;
                outline: none;
                -webkit-appearance: none;
            }

            .control-group input[type="range"]::-webkit-slider-thumb {
                -webkit-appearance: none;
                width: 16px;
                height: 16px;
                background: #00ffff;
                border-radius: 50%;
                cursor: pointer;
            }

            .control-group button {
                width: 100%;
                padding: 8px;
                margin: 4px 0;
                background: #00ffff;
                border: none;
                border-radius: 4px;
                color: #000000;
                font-weight: bold;
                cursor: pointer;
                transition: background 0.2s;
            }

            .control-group button:hover {
                background: #ffffff;
            }

            .control-group button:active {
                background: #00cccc;
            }

            /* Scrollbar styling */
            #control-sidebar::-webkit-scrollbar {
                width: 8px;
            }

            #control-sidebar::-webkit-scrollbar-track {
                background: rgba(0, 0, 0, 0.3);
            }

            #control-sidebar::-webkit-scrollbar-thumb {
                background: #00ffff;
                border-radius: 4px;
            }

            #control-sidebar::-webkit-scrollbar-thumb:hover {
                background: #ffffff;
            }
            "#,
        );

        document.head().unwrap().append_child(&style_element)?;
        Ok(())
    }

    fn trigger_high_consciousness_effects(&mut self) {
        // Add consciousness awakening effect
        let awakening = super::effects::ConsciousnessAwakening::new(
            format!("awakening-{}", js_sys::Date::now() as u64),
            400.0, // center x
            300.0, // center y
            0.9,   // intensity
        );
        self.effect_manager.add_effect(Box::new(awakening));

        // Add neural activation waves
        for i in 0..5 {
            let wave = super::effects::NeuralActivationWave::new(
                format!("wave-{}-{}", i, js_sys::Date::now() as u64),
                100.0 + i as f32 * 150.0, // start x
                200.0,                     // start y
                400.0,                     // end x
                400.0,                     // end y
                0.8,                       // intensity
            );
            self.effect_manager.add_effect(Box::new(wave));
        }
    }

    /// Handle user interaction events
    pub fn handle_event(&mut self, event_type: &str, data: &str) -> Result<(), JsValue> {
        match event_type {
            "query_submit" => {
                // Trigger thought bubble effect
                let thought = super::effects::ThoughtBubble::new(
                    format!("thought-{}", js_sys::Date::now() as u64),
                    200.0, // x position
                    150.0, // y position
                    data.to_string(),
                );
                self.effect_manager.add_effect(Box::new(thought));
            }
            "consciousness_awakening" => {
                self.trigger_high_consciousness_effects();
            }
            _ => {}
        }
        Ok(())
    }
}