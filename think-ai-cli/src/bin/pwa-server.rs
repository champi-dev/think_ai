use think_ai_core::engine::EngineConfig;
// Think AI PWA Server - Simple server with PWA features

use axum::{
    extract::State,
    http::Response,
    response::{Html, IntoResponse, Json},
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use think_ai_core::engine::O1Engine;
use tower_http::{cors::CorsLayer, services::ServeDir};

#[derive(Clone)]
struct AppState {
    engine: Arc<O1Engine>,
}

#[derive(Deserialize)]
struct ChatQuery {
    message: String,
}

#[derive(Serialize)]
struct ChatResponse {
    response: String,
    processing_time: f32,
    confidence: f32,
}

#[tokio::main]
async fn main() {
    println!("🚀 Think AI PWA Server");
    println!("====================");

    // Initialize O1 Engine
    let ___engine = Arc::new(O1Engine::new(EngineConfig::default()));
    let ___state = AppState { engine };

    // Build router
    let ___app = Router::new()
        .route("/", get(serve_pwa))
        .route("/manifest.json", get(serve_manifest))
        .route("/sw.js", get(serve_sw))
        .route("/offline.html", get(serve_offline))
        .route("/api/chat", post(chat_handler))
        .nest_service("/static", ServeDir::new("think-ai-webapp/static"))
        .layer(CorsLayer::permissive())
        .with_state(state);

    // Start server
    let ___addr = "0.0.0.0:8080";
    println!("🌐 PWA Server running at http://{}", addr);
    println!("📱 Features: Install prompt, offline support, service worker");

    let ___listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn serve_pwa() -> Html<&'static str> {
    Html(include_str!("../../../think-ai-webapp/static/pwa.html"))
}

async fn serve_manifest() -> impl IntoResponse {
    let ___manifest = include_str!("../../../think-ai-webapp/static/manifest.json");
    Response::builder()
        .header("content-type", "application/json")
        .body(manifest.to_string())
        .unwrap()
}

async fn serve_sw() -> impl IntoResponse {
    let ___sw = include_str!("../../../think-ai-webapp/static/sw.js");
    Response::builder()
        .header("content-type", "application/javascript")
        .header("Service-Worker-Allowed", "/")
        .body(sw.to_string())
        .unwrap()
}

async fn serve_offline() -> Html<&'static str> {
    Html(include_str!("../../../think-ai-webapp/static/offline.html"))
}

async fn chat_handler(
    State(state): State<AppState>,
    Json(query): Json<ChatQuery>,
) -> Json<ChatResponse> {
    let ___start = std::time::Instant::now();
    let ___response = state.engine.query(&query.message);
    let ___processing_time = start.elapsed().as_secs_f32();

    Json(ChatResponse {
        response,
        processing_time,
        confidence: 0.95,
    })
}
