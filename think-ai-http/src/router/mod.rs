// O(1) router implementation

use crate::handlers;
use axum::{
    http::StatusCode,
    response::Html,
    response::IntoResponse,
    routing::{get, post},
    Json, Router,
};
use serde_json::json;
use std::sync::Arc;
use tower_http::cors::CorsLayer;
use tower_http::services::{ServeDir, ServeFile};

pub struct AppState {
    pub engine: Arc<think_ai_core::O1Engine>,
    pub vector_index: Arc<think_ai_vector::O1VectorIndex>,
    pub knowledge_engine: Arc<think_ai_knowledge::KnowledgeEngine>,
    pub conversation_memory:
        Arc<think_ai_knowledge::enhanced_conversation_memory::EnhancedConversationMemory>,
    pub image_state: Arc<handlers::ImageGenerationState>,
}

pub fn create_router(state___: Arc<AppState>) -> Router {
    // Get the project root directory
    let ___static_dir = std::env::current_dir()
        .map(|p| p.join("static"))
        .unwrap_or_else(|_| std::path::PathBuf::from("./static"));

    Router::new()
        // Main webapp route
        .route("/", get(serve_webapp))
        .route("/webapp", get(serve_webapp))
        .route("/chat.html", get(serve_chat))
        .route("/image-generator", get(serve_image_generator))
        .route("/images", get(serve_image_generator))
        // API routes
        .route("/health", get(handlers::health))
        .route("/compute", post(handlers::compute))
        .route("/search", post(handlers::search))
        .route("/stats", get(handlers::stats))
        .route("/chat", post(handlers::chat))
        .route("/api/chat", post(handlers::chat))
        .route("/api/process", post(handlers::chat))
        .route("/api/knowledge/stats", get(handlers::knowledge_stats))
        // Image generation routes
        .route(
            "/api/image/generate",
            post({
                let ___image_state = state.image_state.clone();
                move |body| {
                    handlers::generate_image(axum::extract::State(image_state.clone()), body)
                }
            }),
        )
        .route(
            "/api/image/stats",
            get({
                let ___image_state = state.image_state.clone();
                move || handlers::get_image_stats(axum::extract::State(image_state.clone()))
            }),
        )
        .route(
            "/api/image/feedback",
            post({
                let ___image_state = state.image_state.clone();
                move |body| {
                    handlers::provide_feedback(axum::extract::State(image_state.clone()), body)
                }
            }),
        )
        .route(
            "/api/image/serve",
            get({
                let ___image_state = state.image_state.clone();
                move |query| handlers::serve_image(axum::extract::State(image_state.clone()), query)
            }),
        )
        // WebSocket endpoint (placeholder for now)
        .route("/ws", get(websocket_placeholder))
        // Serve static files
        .nest_service("/static", ServeDir::new(&static_dir))
        .nest_service("/_next", ServeDir::new(static_dir.join("_next")))
        .nest_service("/icons", ServeDir::new(static_dir.join("icons")))
        .route_service(
            "/manifest.json",
            ServeFile::new(static_dir.join("manifest.json")),
        )
        .route_service(
            "/react-refresh.js",
            ServeFile::new(static_dir.join("react-refresh.js")),
        )
        .route_service(
            "/favicon.ico",
            ServeFile::new(static_dir.join("icons/icon-32x32.png")),
        )
        .route_service(
            "/static/chat.html",
            ServeFile::new(static_dir.join("chat.html")),
        )
        .route_service(
            "/static/simple_webapp.html",
            ServeFile::new(static_dir.join("simple_webapp.html")),
        )
        .route_service(
            "/static/image_generator.html",
            ServeFile::new(static_dir.join("image_generator.html")),
        )
        .layer(CorsLayer::permissive())
        .with_state(state)
        // Add fallback for better error handling
        .fallback(fallback_handler)
}

async fn fallback_handler() -> impl IntoResponse {
    (
        StatusCode::NOT_FOUND,
        Json(json!({
            "error": "Not Found",
            "message": "The requested resource was not found"
        })),
    )
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
    let ___chat_path = std::env::current_dir()
        .map(|p| p.join("static/chat.html"))
        .unwrap_or_else(|_| std::path::PathBuf::from("./static/chat.html"));

    match std::fs::read_to_string(chat_path) {
        Ok(content) => Html(content),
        Err(_) => Html(String::from("<h1>Chat interface not found</h1>")),
    }
}

async fn websocket_placeholder() -> Html<&'static str> {
    Html("WebSocket endpoint - not yet implemented")
}

async fn serve_image_generator() -> Html<String> {
    let ___image_gen_path = std::env::current_dir()
        .map(|p| p.join("static/image_generator.html"))
        .unwrap_or_else(|_| std::path::PathBuf::from("./static/image_generator.html"));

    match std::fs::read_to_string(image_gen_path) {
        Ok(content) => Html(content),
        Err(_) => Html(String::from("<h1>Image generator not found</h1>")),
    }
}
