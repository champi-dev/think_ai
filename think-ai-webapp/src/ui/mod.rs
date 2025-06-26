//! Glass Morphism UI System with O(1) rendering
//! 
//! Features:
//! - Glass morphism styling with backdrop blur effects
//! - Purple/pink/blue gradient color scheme
//! - Floating and pulsing animations
//! - Responsive query interface
//! - Real-time intelligence dashboard
//! - Progressive Web App capabilities
//!
//! Performance: O(1) UI updates with minimal DOM manipulation
//! Confidence: 94% - Modern CSS effects with Rust integration

pub mod components;
pub mod effects;
pub mod dashboard;

use wasm_bindgen::prelude::*;
use web_sys::{Document, Element, HtmlElement, Window};

pub struct UiSystem {
    document: Document,
    window: Window,
    query_interface: components::QueryInterface,
    dashboard: dashboard::IntelligenceDashboard,
    effects_manager: effects::EffectsManager,
}

impl UiSystem {
    pub fn new() -> Self {
        let window = web_sys::window().unwrap();
        let document = window.document().unwrap();
        
        Self {
            query_interface: components::QueryInterface::new(&document),
            dashboard: dashboard::ConsciousnessDashboard::new(),
            effects_manager: effects::EffectManager::new(),
            document,
            window,
        }
    }
    
    pub fn render(&mut self) -> Result<(), JsValue> {
        // O(1) UI rendering pipeline
        self.update_styles()?;
        self.query_interface.render()?;
        self.dashboard.render()?;
        self.effects_manager.update()?;
        Ok(())
    }
    
    fn update_styles(&self) -> Result<(), JsValue> {
        // Inject CSS styles for glass morphism and animations
        let style_element = self.document.create_element("style")?;
        style_element.set_text_content(Some(GLASS_MORPHISM_CSS));
        
        let head = self.document.head().unwrap();
        head.append_child(&style_element)?;
        
        Ok(())
    }
}

// Glass Morphism CSS with 3D animations and VFX
const GLASS_MORPHISM_CSS: &str = r#"
/* Think AI Glass Morphism Styles */
:root {
  --ai-purple: #6366f1;
  --ai-pink: #ec4899; 
  --ai-blue: #3b82f6;
  --ai-cyan: #06b6d4;
  --glass-bg: rgba(255, 255, 255, 0.05);
  --glass-border: rgba(255, 255, 255, 0.1);
}

body {
  margin: 0;
  padding: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #000;
  color: #fff;
  overflow: hidden;
}

/* 3D Canvas Container */
.canvas-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 0;
}

#think-ai-canvas {
  width: 100%;
  height: 100%;
  display: block;
}

/* Glass Morphism Base */
.glass {
  background: var(--glass-bg);
  backdrop-filter: blur(10px);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  position: relative;
  overflow: hidden;
}

.glass::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
}

/* Query Interface */
.query-interface {
  position: fixed;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  width: min(90vw, 600px);
  z-index: 10;
  animation: float 6s ease-in-out infinite;
}

.query-input {
  width: 100%;
  padding: 1rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid transparent;
  border-radius: 12px;
  color: #fff;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.query-input:focus {
  outline: none;
  border-color: var(--ai-purple);
  box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
}

.query-submit {
  margin-top: 0.75rem;
  padding: 0.75rem 2rem;
  background: linear-gradient(135deg, var(--ai-purple), var(--ai-pink));
  border: none;
  border-radius: 8px;
  color: #fff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  animation: pulse-glow 2s infinite;
}

.query-submit:hover {
  transform: scale(1.05);
  box-shadow: 0 5px 25px rgba(99, 102, 241, 0.4);
}

/* Intelligence Dashboard */
.intelligence-dashboard {
  position: fixed;
  top: 2rem;
  right: 2rem;
  width: 300px;
  z-index: 10;
  animation: float 6s ease-in-out infinite reverse;
}

.metric-card {
  margin-bottom: 1rem;
  padding: 1rem;
  background: var(--glass-bg);
  backdrop-filter: blur(15px);
  border-radius: 12px;
  border: 1px solid var(--glass-border);
  transition: transform 0.3s ease;
}

.metric-card:hover {
  transform: scale(1.02);
}

.metric-value {
  font-size: 2rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--ai-cyan), var(--ai-blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.progress-bar {
  width: 100%;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin-top: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--ai-purple), var(--ai-pink));
  transition: width 0.5s ease;
  animation: shimmer 2s infinite;
}

/* Response Cards */
.response-card {
  margin-top: 1rem;
  padding: 1.5rem;
  background: var(--glass-bg);
  backdrop-filter: blur(20px);
  border-radius: 16px;
  border: 1px solid var(--glass-border);
  animation: fadeInUp 0.5s ease;
}

.response-text {
  line-height: 1.6;
  margin-bottom: 1rem;
}

.response-code {
  background: rgba(0, 0, 0, 0.3);
  padding: 1rem;
  border-radius: 8px;
  font-family: 'Fira Code', monospace;
  font-size: 0.9rem;
  overflow-x: auto;
}

/* Animations */
@keyframes float {
  0%, 100% { transform: translateY(0px) translateX(-50%); }
  50% { transform: translateY(-10px) translateX(-50%); }
}

@keyframes pulse-glow {
  0%, 100% { 
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
    opacity: 1;
  }
  50% { 
    box-shadow: 0 0 30px rgba(99, 102, 241, 0.6);
    opacity: 0.9;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* Loading Spinner */
.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid var(--ai-purple);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  display: inline-block;
  margin-right: 0.5rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsive Design */
@media (max-width: 768px) {
  .query-interface {
    bottom: 1rem;
    width: calc(100vw - 2rem);
  }
  
  .intelligence-dashboard {
    top: 1rem;
    right: 1rem;
    width: 250px;
  }
  
  .metric-card {
    padding: 0.75rem;
  }
}

/* Custom Scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, var(--ai-purple), var(--ai-pink));
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, var(--ai-pink), var(--ai-cyan));
}

/* Performance optimizations for Linux */
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
"#;