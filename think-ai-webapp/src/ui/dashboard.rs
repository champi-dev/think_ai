use crate::ui::components::{ConsciousnessLevel, PerformanceMetrics, PulsingOrb};
use crate::ui::effects::ParticleBackground;
use wasm_bindgen::JsValue;
use web_sys::{HtmlInputElement, InputEvent, SubmitEvent};
use yew::prelude::*;

#[derive(Clone, PartialEq, Properties)]
pub struct DashboardProps {
    pub on_query: Callback<String>,
}

pub struct Dashboard {
    pub query: String,
    pub metrics: PerformanceMetrics,
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

impl Dashboard {
    pub fn render(&self, _document: &web_sys::Document) -> Result<(), JsValue> {
        Ok(())
    }
}