//! O(1) router implementation

use axum::{Router, routing::{get, post}, response::Html};
use std::sync::Arc;
use crate::handlers;

pub struct AppState {
    pub engine: Arc<think_ai_core::O1Engine>,
    pub vector_index: Arc<think_ai_vector::O1VectorIndex>,
}

pub fn create_router(state: Arc<AppState>) -> Router {
    Router::new()
        // Main webapp route
        .route("/", get(serve_webapp))
        .route("/webapp", get(serve_webapp))
        
        // API routes
        .route("/health", get(handlers::health))
        .route("/compute", post(handlers::compute))
        .route("/search", post(handlers::search))
        .route("/stats", get(handlers::stats))
        
        // WebSocket endpoint (placeholder for now)
        .route("/ws", get(websocket_placeholder))
        
        .with_state(state)
}

async fn serve_webapp() -> Html<&'static str> {
    Html(include_str!("../../../webapp_homepage.html"))
}

async fn websocket_placeholder() -> Html<&'static str> {
    Html("WebSocket endpoint - not yet implemented")
}