// Think AI with True LLM - Generative AI with O(1) Caching
//!
// This makes Think AI a real generative AI that can create novel responses
// while maintaining O(1) performance for cached queries.

use axum::{
    extract::State,
    http::StatusCode,
    response::Json,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use think_ai_knowledge::simple_llm::SimpleLLM;
use tower_http::cors::CorsLayer;
use tracing::{info, Level};

#[derive(Clone)]
struct AppState {
    llm: Arc<SimpleLLM>,
}

#[derive(Deserialize)]
struct ChatRequest {
    query: String,
    #[serde(default)]
    context: Vec<String>,
    max_length: Option<usize>,
}

#[derive(Serialize)]
struct ChatResponse {
    response: String,
    confidence: f64,
    response_time_ms: u64,
    from_cache: bool,
}

#[tokio::main]
async fn main() {
    // Initialize logging
    tracing_subscriber::fmt().with_max_level(Level::INFO).init();
    info!("🚀 Starting Think AI with True LLM Generation!");

    // Create the LLM
    let llm = Arc::new(SimpleLLM::new());

    // Create app state
    let state = AppState { llm };

    // Build the router
    let app = Router::new()
        .route("/", get(root))
        .route("/health", get(health))
        .route("/api/chat", post(chat))
        .route("/api/stats", get(stats))
        .with_state(state)
        .layer(CorsLayer::permissive());

    // Get port from environment or use default
    let port = std::env::var("PORT")
        .ok()
        .and_then(|p| p.parse::<u16>().ok())
        .unwrap_or(8081);

    let addr = format!("0.0.0.0:{}", port);
    info!("✅ Think AI LLM listening on http://{}", addr);
    info!("📝 Try: curl -X POST http://localhost:8081/api/chat -H 'Content-Type: application/json' -d '{{\"query\": \"Hello!\"}}'");

    let listener = tokio::net::TcpListener::bind(addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}

async fn root() -> &'static str {
    "🧠 Think AI - True LLM with O(1) Caching\n\nI can now generate novel responses while maintaining instant performance for repeated queries!"
}

async fn health() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "ok",
        "model": "SimpleLLM",
        "features": ["generation", "O(1) caching", "knowledge combination"]
    }))
}

async fn chat(
    State(state): State<AppState>,
    Json(request): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    let start = std::time::Instant::now();

    // Check cache statistics before
    let (cache_size_before, _) = state.llm.cache_stats();

    // Generate response (O(1) if cached, generation if not)
    let response_text = state.llm.generate(&request.query);

    // Check if it was cached
    let (cache_size_after, _) = state.llm.cache_stats();
    let from_cache = cache_size_after == cache_size_before;

    let response = ChatResponse {
        response: response_text,
        confidence: if from_cache { 1.0 } else { 0.85 },
        response_time_ms: start.elapsed().as_millis() as u64,
        from_cache,
    };

    info!(
        "Query: '{}' | From cache: {} | Time: {}ms",
        request.query, from_cache, response.response_time_ms
    );

    Ok(Json(response))
}

async fn stats(State(state): State<AppState>) -> Json<serde_json::Value> {
    let (cache_size, hit_rate) = state.llm.cache_stats();

    Json(serde_json::json!({
        "total_cached_responses": cache_size,
        "cache_hit_rate": hit_rate,
        "capabilities": {
            "generation": true,
            "o1_caching": true,
            "knowledge_combination": true,
            "learning": false
        }
    }))
}
