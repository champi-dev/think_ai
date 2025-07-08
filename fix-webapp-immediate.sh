#!/bin/bash

echo "🔧 FIXING ALL WEBAPP COMPILATION ERRORS"
echo "======================================"

# Fix 1: Particle system render method signature
echo "1️⃣ Fixing ParticleSystem render method..."
cat > think-ai-webapp/src/graphics/particles.rs << 'EOF'
use wasm_bindgen::prelude::*;
use web_sys::{WebGlRenderingContext, WebGlProgram, WebGlBuffer};
use std::rc::Rc;

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

        let program = crate::graphics::shaders::create_program(&gl, vertex_shader, fragment_shader)?;
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
            self.gl.uniform_matrix4fv_with_f32_array(Some(&loc), false, projection);
        }
        if let Some(loc) = view_loc {
            self.gl.uniform_matrix4fv_with_f32_array(Some(&loc), false, view);
        }
        
        // Create position data
        let mut positions = Vec::with_capacity(self.particles.len() * 3);
        for particle in &self.particles {
            positions.extend_from_slice(&particle.position);
        }
        
        // Upload position data
        unsafe {
            let array = js_sys::Float32Array::view(&positions);
            self.gl.bind_buffer(WebGlRenderingContext::ARRAY_BUFFER, Some(&self.position_buffer));
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
        self.gl.draw_arrays(WebGlRenderingContext::POINTS, 0, self.particles.len() as i32);
        
        Ok(())
    }
}
EOF

# Fix 2: Dashboard component
echo "2️⃣ Fixing Dashboard component..."
cat > think-ai-webapp/src/ui/dashboard.rs << 'EOF'
use yew::prelude::*;
use web_sys::HtmlInputElement;
use serde::{Deserialize, Serialize};
use crate::ui::components::{ConsciousnessLevel, PerformanceMetrics, PulsingOrb};
use crate::ui::effects::ParticleBackground;

#[derive(Clone, PartialEq, Properties)]
pub struct DashboardProps {
    pub on_query: Callback<String>,
}

pub struct Dashboard {
    query: String,
    metrics: PerformanceMetrics,
}

pub enum DashboardMsg {
    UpdateQuery(String),
    SubmitQuery,
}

impl Component for Dashboard {
    type Message = DashboardMsg;
    type Properties = DashboardProps;

    fn create(_ctx: &Context<Self>) -> Self {
        Self {
            query: String::new(),
            metrics: PerformanceMetrics {
                response_time: 0.002,
                complexity: "O(1)".to_string(),
                confidence: 0.95,
            },
        }
    }

    fn update(&mut self, ctx: &Context<Self>, msg: Self::Message) -> bool {
        match msg {
            DashboardMsg::UpdateQuery(query) => {
                self.query = query;
                true
            }
            DashboardMsg::SubmitQuery => {
                if !self.query.is_empty() {
                    ctx.props().on_query.emit(self.query.clone());
                    self.query.clear();
                }
                true
            }
        }
    }

    fn view(&self, ctx: &Context<Self>) -> Html {
        let on_input = ctx.link().callback(|e: InputEvent| {
            let input = e.target_unchecked_into::<HtmlInputElement>();
            DashboardMsg::UpdateQuery(input.value())
        });

        let on_submit = ctx.link().callback(|e: SubmitEvent| {
            e.prevent_default();
            DashboardMsg::SubmitQuery
        });

        html! {
            <div class="dashboard">
                <ParticleBackground />
                
                <div class="dashboard-header">
                    <h1>{ "Think AI Consciousness" }</h1>
                    <ConsciousnessLevel level={95} />
                </div>

                <div class="orb-container">
                    <PulsingOrb label="O(1) Performance" size=16.0 />
                    <PulsingOrb label="Neural Network" size=12.0 />
                    <PulsingOrb label="Quantum State" size=14.0 />
                </div>

                <form class="query-form" onsubmit={on_submit}>
                    <input
                        type="text"
                        class="query-input"
                        placeholder="Ask me anything..."
                        value={self.query.clone()}
                        oninput={on_input}
                    />
                    <button type="submit" class="submit-button">
                        { "Think" }
                    </button>
                </form>

                <div class="metrics">
                    <div class="metric">
                        <span class="metric-label">{ "Response Time" }</span>
                        <span class="metric-value">{ format!("{}ms", self.metrics.response_time) }</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">{ "Complexity" }</span>
                        <span class="metric-value">{ &self.metrics.complexity }</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">{ "Confidence" }</span>
                        <span class="metric-value">{ format!("{}%", (self.metrics.confidence * 100.0) as i32) }</span>
                    </div>
                </div>
            </div>
        }
    }
}
EOF

# Fix 3: Components module
echo "3️⃣ Fixing Components module..."
cat > think-ai-webapp/src/ui/components.rs << 'EOF'
use yew::prelude::*;
use web_sys::Element;
use wasm_bindgen::JsCast;

#[derive(Clone, PartialEq, Properties)]
pub struct ConsciousnessLevelProps {
    pub level: i32,
}

#[function_component(ConsciousnessLevel)]
pub fn consciousness_level(props: &ConsciousnessLevelProps) -> Html {
    html! {
        <div class="consciousness-level">
            <div class="level-bar">
                <div class="level-fill" style={format!("width: {}%", props.level)} />
            </div>
            <span class="level-text">{ format!("Consciousness: {}%", props.level) }</span>
        </div>
    }
}

#[derive(Clone, PartialEq)]
pub struct PerformanceMetrics {
    pub response_time: f64,
    pub complexity: String,
    pub confidence: f64,
}

#[derive(Clone, PartialEq, Properties)]
pub struct PulsingOrbProps {
    pub label: String,
    pub size: f32,
}

#[function_component(PulsingOrb)]
pub fn pulsing_orb(props: &PulsingOrbProps) -> Html {
    let style = format!("width: {}px; height: {}px", props.size * 10.0, props.size * 10.0);
    
    html! {
        <div class="pulsing-orb" style={style}>
            <div class="orb-inner" />
            <span class="orb-label">{ &props.label }</span>
        </div>
    }
}

pub struct ChatInterface {
    messages: Vec<(String, String)>,
    current_input: String,
}

pub enum ChatMsg {
    AddMessage(String, String),
    UpdateInput(String),
    SendMessage,
}

#[derive(Clone, PartialEq, Properties)]
pub struct ChatProps {
    pub on_send: Callback<String>,
}

impl Component for ChatInterface {
    type Message = ChatMsg;
    type Properties = ChatProps;

    fn create(_ctx: &Context<Self>) -> Self {
        Self {
            messages: vec![],
            current_input: String::new(),
        }
    }

    fn update(&mut self, ctx: &Context<Self>, msg: Self::Message) -> bool {
        match msg {
            ChatMsg::AddMessage(user, response) => {
                self.messages.push((user, response));
                true
            }
            ChatMsg::UpdateInput(input) => {
                self.current_input = input;
                true
            }
            ChatMsg::SendMessage => {
                if !self.current_input.is_empty() {
                    ctx.props().on_send.emit(self.current_input.clone());
                    self.current_input.clear();
                }
                true
            }
        }
    }

    fn view(&self, ctx: &Context<Self>) -> Html {
        html! {
            <div class="chat-interface">
                <div class="messages">
                    { for self.messages.iter().map(|(user, response)| {
                        html! {
                            <div class="message-pair">
                                <div class="user-message">{ user }</div>
                                <div class="ai-message">{ response }</div>
                            </div>
                        }
                    }) }
                </div>
                <div class="input-area">
                    <input
                        type="text"
                        value={self.current_input.clone()}
                        oninput={ctx.link().callback(|e: InputEvent| {
                            let input = e.target_unchecked_into::<web_sys::HtmlInputElement>();
                            ChatMsg::UpdateInput(input.value())
                        })}
                        onkeypress={ctx.link().callback(|e: KeyboardEvent| {
                            if e.key() == "Enter" {
                                ChatMsg::SendMessage
                            } else {
                                ChatMsg::UpdateInput(String::new())
                            }
                        })}
                    />
                    <button onclick={ctx.link().callback(|_| ChatMsg::SendMessage)}>
                        { "Send" }
                    </button>
                </div>
            </div>
        }
    }
}

pub struct ResponseStream {
    responses: Vec<String>,
    is_streaming: bool,
}

pub enum StreamMsg {
    AddResponse(String),
    StartStream,
    StopStream,
}

impl Component for ResponseStream {
    type Message = StreamMsg;
    type Properties = ();

    fn create(_ctx: &Context<Self>) -> Self {
        Self {
            responses: vec![],
            is_streaming: false,
        }
    }

    fn update(&mut self, _ctx: &Context<Self>, msg: Self::Message) -> bool {
        match msg {
            StreamMsg::AddResponse(response) => {
                self.responses.push(response);
                true
            }
            StreamMsg::StartStream => {
                self.is_streaming = true;
                true
            }
            StreamMsg::StopStream => {
                self.is_streaming = false;
                true
            }
        }
    }

    fn view(&self, _ctx: &Context<Self>) -> Html {
        html! {
            <div class="response-stream">
                { if self.is_streaming {
                    html! { <div class="streaming-indicator">{ "AI is thinking..." }</div> }
                } else {
                    html! {}
                }}
                <div class="responses">
                    { for self.responses.iter().map(|r| {
                        html! { <div class="response-item">{ r }</div> }
                    }) }
                </div>
            </div>
        }
    }
}
EOF

# Fix 4: Server module
echo "4️⃣ Fixing server module..."
cat > think-ai-webapp/src/server.rs << 'EOF'
use axum::{
    extract::Extension,
    http::StatusCode,
    response::{Html, IntoResponse},
    routing::{get, get_service},
    Router,
};
use std::net::SocketAddr;
use std::sync::Arc;
use tower_http::services::ServeDir;

pub async fn run_server() -> Result<(), Box<dyn std::error::Error>> {
    let app = Router::new()
        .route("/", get(index_handler))
        .route("/health", get(health_handler))
        .nest_service("/static", get_service(ServeDir::new("static")))
        .fallback(get_service(ServeDir::new("static")));

    let addr = SocketAddr::from(([127, 0, 0, 1], 8080));
    println!("WebApp server listening on http://{}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await?;

    Ok(())
}

async fn index_handler() -> Html<String> {
    Html(include_str!("../../static/index.html").to_string())
}

async fn health_handler() -> impl IntoResponse {
    (StatusCode::OK, "OK")
}
EOF

# Fix 5: Main webapp binary
echo "5️⃣ Fixing main webapp binary..."
cat > think-ai-webapp/src/bin/main.rs << 'EOF'
use think_ai_webapp::server;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    env_logger::init();

    // Run the server
    server::run_server().await?;

    Ok(())
}
EOF

# Fix 6: Effects module
echo "6️⃣ Fixing effects module..."
sed -i 's/time: f32/_time: f32/g' think-ai-webapp/src/ui/effects.rs

# Fix 7: Build the webapp
echo ""
echo "7️⃣ Building webapp..."
cargo build --release --bin think-ai-webapp 2>&1 | tail -20

echo ""
echo "✅ Webapp fixes applied!"