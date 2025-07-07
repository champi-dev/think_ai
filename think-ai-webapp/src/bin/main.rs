//! Think AI PWA Web Server

use think_ai_webapp::{server, ThinkAiWebapp};
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing_subscriber;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    tracing_subscriber::fmt::init();
    
    println!("🚀 Think AI PWA Server");
    println!("====================");
    
    // Initialize Think AI webapp engine
    let ai_webapp = Arc::new(RwLock::new(ThinkAiWebapp::new()));
    
    // Initialize consciousness state
    let consciousness_data = Arc::new(RwLock::new(server::ConsciousnessState {
        awareness_level: 0.95,
        processing_speed: 0.18,
        memory_utilization: 0.45,
        creativity_index: 0.88,
        active_thoughts: 42,
    }));
    
    // Create app state
    let app_state = server::AppState {
        ai_engine: ai_webapp,
        consciousness_data,
    };
    
    // Create router
    let app = server::create_webapp_router(app_state);
    
    // Start server
    let addr = "0.0.0.0:8080";
    println!("🌐 Starting PWA server on http://{}", addr);
    println!("📱 Features: Install prompt, offline support, service worker");
    println!("🔧 DevTools: Application tab to inspect PWA features");
    
    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;
    
    Ok(())
}