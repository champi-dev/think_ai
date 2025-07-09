#!/bin/bash
set -e

echo "Fixing webapp components module syntax errors..."

# Create a fixed version
cat > think-ai-webapp/src/ui/components.rs << 'EOF'
use wasm_bindgen::JsCast;
use web_sys::Element;
use yew::prelude::*;

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
    let style = format!(
        "width: {}px; height: {}px",
        props.size * 10.0,
        props.size * 10.0
    );
    
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
    
    fn update(&mut self, ctx: &Context<Self>, msg: ChatMsg) -> bool {
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
    
    fn update(&mut self, _ctx: &Context<Self>, msg: StreamMsg) -> bool {
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

echo "Components module fixed!"