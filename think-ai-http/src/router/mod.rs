//! O(1) router implementation

use axum::{Router, routing::{get, post}, response::Html};
use std::sync::Arc;
use tower_http::cors::CorsLayer;
use tower_http::services::{ServeDir, ServeFile};
use crate::handlers;

pub struct AppState {
    pub engine: Arc<think_ai_core::O1Engine>,
    pub vector_index: Arc<think_ai_vector::O1VectorIndex>,
    pub knowledge_engine: Arc<think_ai_knowledge::KnowledgeEngine>,
    pub conversation_memory: Arc<think_ai_knowledge::conversation_memory::ConversationMemory>,
}

pub fn create_router(state: Arc<AppState>) -> Router {
    // Get the project root directory
    let static_dir = std::env::current_dir()
        .map(|p| p.join("static"))
        .unwrap_or_else(|_| std::path::PathBuf::from("./static"));
    
    Router::new()
        // Main webapp route
        .route("/", get(serve_webapp))
        .route("/webapp", get(serve_webapp))
        .route("/chat.html", get(serve_chat))
        
        // API routes
        .route("/health", get(handlers::health))
        .route("/compute", post(handlers::compute))
        .route("/search", post(handlers::search))
        .route("/stats", get(handlers::stats))
        .route("/chat", post(handlers::chat))
        .route("/api/chat", post(handlers::chat))
        .route("/api/process", post(handlers::chat))
        
        // WebSocket endpoint (placeholder for now)
        .route("/ws", get(websocket_placeholder))
        
        // Serve static files
        .nest_service("/_next", ServeDir::new(static_dir.join("_next")))
        .nest_service("/icons", ServeDir::new(static_dir.join("icons")))
        .route_service("/manifest.json", ServeFile::new(static_dir.join("manifest.json")))
        .route_service("/react-refresh.js", ServeFile::new(static_dir.join("react-refresh.js")))
        .route_service("/favicon.ico", ServeFile::new(static_dir.join("icons/icon-32x32.png")))
        
        .layer(CorsLayer::permissive())
        .with_state(state)
}

async fn serve_webapp() -> Html<&'static str> {
    // Use test version locally, production version in deployment
    if cfg!(debug_assertions) {
        Html(include_str!("../../../minimal_3d_test.html"))
    } else {
        Html(include_str!("../../../minimal_3d.html"))
    }
}

async fn serve_chat() -> Html<String> {
    let chat_path = std::env::current_dir()
        .map(|p| p.join("static/chat.html"))
        .unwrap_or_else(|_| std::path::PathBuf::from("./static/chat.html"));
    
    match std::fs::read_to_string(chat_path) {
        Ok(content) => Html(content),
        Err(_) => Html(String::from("<h1>Chat interface not found</h1>"))
    }
}

async fn websocket_placeholder() -> Html<&'static str> {
    Html("WebSocket endpoint - not yet implemented")
}