//! UI components for consciousness visualization interface
//! 
//! Provides O(1) component rendering and interaction handling

use wasm_bindgen::JsValue;
use web_sys::{Document, Element, HtmlElement, Window};
use std::collections::HashMap;

/// O(1) UI component registry with hash-based lookups
pub struct ComponentRegistry {
    components: HashMap<String, Box<dyn UIComponent>>,
    active_components: Vec<String>,
}

pub trait UIComponent {
    fn render(&self, container: &Element) -> Result<(), JsValue>;
    fn update(&mut self, data: &ComponentData) -> Result<(), JsValue>;
    fn handle_event(&mut self, event_type: &str, data: &str) -> Result<(), JsValue>;
    fn get_id(&self) -> &str;
}

#[derive(Debug, Clone)]
pub struct ComponentData {
    pub id: String,
    pub values: HashMap<String, String>,
}

impl ComponentRegistry {
    pub fn new() -> Self {
        Self {
            components: HashMap::new(),
            active_components: Vec::new(),
        }
    }

    /// O(1) component registration
    pub fn register_component(&mut self, component: Box<dyn UIComponent>) {
        let id = component.get_id().to_string();
        self.components.insert(id.clone(), component);
        self.active_components.push(id);
    }

    /// O(1) component retrieval by ID
    pub fn get_component(&mut self, id: &str) -> Option<&mut Box<dyn UIComponent>> {
        self.components.get_mut(id)
    }

    /// Render all active components
    pub fn render_all(&self, document: &Document) -> Result<(), JsValue> {
        for component_id in &self.active_components {
            if let Some(component) = self.components.get(component_id) {
                if let Some(container) = document.get_element_by_id(component_id) {
                    component.render(&container)?;
                }
            }
        }
        Ok(())
    }
}

/// Consciousness metrics display component
pub struct ConsciousnessMetrics {
    id: String,
    consciousness_level: f32,
    neural_activity: f32,
    memory_utilization: f32,
    processing_speed: f32,
}

impl ConsciousnessMetrics {
    pub fn new(id: String) -> Self {
        Self {
            id,
            consciousness_level: 0.0,
            neural_activity: 0.0,
            memory_utilization: 0.0,
            processing_speed: 0.0,
        }
    }

    pub fn update_metrics(
        &mut self,
        consciousness: f32,
        neural: f32,
        memory: f32,
        speed: f32,
    ) {
        self.consciousness_level = consciousness.clamp(0.0, 1.0);
        self.neural_activity = neural.clamp(0.0, 1.0);
        self.memory_utilization = memory.clamp(0.0, 1.0);
        self.processing_speed = speed.clamp(0.0, 1.0);
    }
}

impl UIComponent for ConsciousnessMetrics {
    fn render(&self, container: &Element) -> Result<(), JsValue> {
        let html = format!(
            r#"
            <div class="consciousness-metrics">
                <h3>Consciousness Metrics</h3>
                <div class="metric">
                    <label>Consciousness Level:</label>
                    <div class="progress-bar">
                        <div class="progress" style="width: {}%"></div>
                    </div>
                    <span class="value">{:.1}%</span>
                </div>
                <div class="metric">
                    <label>Neural Activity:</label>
                    <div class="progress-bar">
                        <div class="progress" style="width: {}%"></div>
                    </div>
                    <span class="value">{:.1}%</span>
                </div>
                <div class="metric">
                    <label>Memory Utilization:</label>
                    <div class="progress-bar">
                        <div class="progress" style="width: {}%"></div>
                    </div>
                    <span class="value">{:.1}%</span>
                </div>
                <div class="metric">
                    <label>Processing Speed:</label>
                    <div class="progress-bar">
                        <div class="progress" style="width: {}%"></div>
                    </div>
                    <span class="value">{:.1}%</span>
                </div>
            </div>
            <style>
                .consciousness-metrics {{
                    background: rgba(0, 20, 40, 0.8);
                    border: 1px solid #00ffff;
                    border-radius: 8px;
                    padding: 16px;
                    color: #ffffff;
                    font-family: 'Courier New', monospace;
                }}
                .metric {{
                    margin: 8px 0;
                    display: flex;
                    align-items: center;
                    gap: 12px;
                }}
                .metric label {{
                    width: 140px;
                    font-size: 12px;
                }}
                .progress-bar {{
                    flex: 1;
                    height: 16px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 8px;
                    overflow: hidden;
                }}
                .progress {{
                    height: 100%;
                    background: linear-gradient(90deg, #00ffff, #ff00ff);
                    transition: width 0.3s ease;
                }}
                .value {{
                    width: 40px;
                    text-align: right;
                    font-size: 12px;
                }}
            </style>
            "#,
            self.consciousness_level * 100.0,
            self.consciousness_level * 100.0,
            self.neural_activity * 100.0,
            self.neural_activity * 100.0,
            self.memory_utilization * 100.0,
            self.memory_utilization * 100.0,
            self.processing_speed * 100.0,
            self.processing_speed * 100.0,
        );

        container.set_inner_html(&html);
        Ok(())
    }

    fn update(&mut self, data: &ComponentData) -> Result<(), JsValue> {
        if let Some(consciousness) = data.values.get("consciousness_level") {
            self.consciousness_level = consciousness.parse().unwrap_or(0.0);
        }
        if let Some(neural) = data.values.get("neural_activity") {
            self.neural_activity = neural.parse().unwrap_or(0.0);
        }
        if let Some(memory) = data.values.get("memory_utilization") {
            self.memory_utilization = memory.parse().unwrap_or(0.0);
        }
        if let Some(speed) = data.values.get("processing_speed") {
            self.processing_speed = speed.parse().unwrap_or(0.0);
        }
        Ok(())
    }

    fn handle_event(&mut self, _event_type: &str, _data: &str) -> Result<(), JsValue> {
        // Metrics component is read-only
        Ok(())
    }

    fn get_id(&self) -> &str {
        &self.id
    }
}

/// Interactive query interface component
pub struct QueryInterface {
    id: String,
    current_query: String,
    response_history: Vec<(String, String)>,
    is_processing: bool,
}

impl QueryInterface {
    pub fn new(id: String) -> Self {
        Self {
            id,
            current_query: String::new(),
            response_history: Vec::new(),
            is_processing: false,
        }
    }

    pub fn add_exchange(&mut self, query: String, response: String) {
        self.response_history.push((query, response));
        if self.response_history.len() > 50 {
            self.response_history.remove(0);
        }
    }

    pub fn set_processing(&mut self, processing: bool) {
        self.is_processing = processing;
    }
}

impl UIComponent for QueryInterface {
    fn render(&self, container: &Element) -> Result<(), JsValue> {
        let history_html = self.response_history.iter()
            .rev()
            .take(10)
            .map(|(q, r)| format!(
                r#"
                <div class="exchange">
                    <div class="query">Q: {}</div>
                    <div class="response">A: {}</div>
                </div>
                "#, 
                q, r
            ))
            .collect::<Vec<_>>()
            .join("");

        let processing_indicator = if self.is_processing {
            r#"<div class="processing">Processing query...</div>"#
        } else {
            ""
        };

        let html = format!(
            r#"
            <div class="query-interface">
                <h3>Consciousness Query Interface</h3>
                <div class="history">
                    {}
                </div>
                {}
                <div class="input-area">
                    <input type="text" id="query-input" placeholder="Ask the consciousness..." value="{}">
                    <button id="query-submit" {}>Submit</button>
                </div>
            </div>
            <style>
                .query-interface {{
                    background: rgba(0, 20, 40, 0.9);
                    border: 1px solid #00ffff;
                    border-radius: 8px;
                    padding: 16px;
                    color: #ffffff;
                    font-family: 'Courier New', monospace;
                    max-height: 400px;
                    overflow-y: auto;
                }}
                .history {{
                    max-height: 250px;
                    overflow-y: auto;
                    margin-bottom: 16px;
                }}
                .exchange {{
                    margin: 8px 0;
                    padding: 8px;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 4px;
                }}
                .query {{
                    color: #00ffff;
                    margin-bottom: 4px;
                }}
                .response {{
                    color: #ffffff;
                    margin-left: 16px;
                }}
                .processing {{
                    color: #ffff00;
                    text-align: center;
                    margin: 8px 0;
                    animation: pulse 1s infinite;
                }}
                .input-area {{
                    display: flex;
                    gap: 8px;
                }}
                #query-input {{
                    flex: 1;
                    padding: 8px;
                    background: rgba(255, 255, 255, 0.1);
                    border: 1px solid #00ffff;
                    border-radius: 4px;
                    color: #ffffff;
                }}
                #query-submit {{
                    padding: 8px 16px;
                    background: #00ffff;
                    border: none;
                    border-radius: 4px;
                    color: #000000;
                    cursor: pointer;
                }}
                #query-submit:hover {{
                    background: #ffffff;
                }}
                #query-submit:disabled {{
                    background: #666666;
                    cursor: not-allowed;
                }}
                @keyframes pulse {{
                    0%, 100% {{ opacity: 1; }}
                    50% {{ opacity: 0.5; }}
                }}
            </style>
            "#,
            history_html,
            processing_indicator,
            self.current_query,
            if self.is_processing { "disabled" } else { "" }
        );

        container.set_inner_html(&html);
        Ok(())
    }

    fn update(&mut self, data: &ComponentData) -> Result<(), JsValue> {
        if let Some(query) = data.values.get("current_query") {
            self.current_query = query.clone();
        }
        if let Some(processing) = data.values.get("is_processing") {
            self.is_processing = processing == "true";
        }
        Ok(())
    }

    fn handle_event(&mut self, event_type: &str, data: &str) -> Result<(), JsValue> {
        match event_type {
            "submit_query" => {
                self.current_query = data.to_string();
                self.is_processing = true;
            }
            "query_response" => {
                if let Some(last_query) = self.response_history.last().map(|(q, _)| q.clone()) {
                    self.response_history.last_mut().unwrap().1 = data.to_string();
                }
                self.is_processing = false;
            }
            _ => {}
        }
        Ok(())
    }

    fn get_id(&self) -> &str {
        &self.id
    }
}