use axum::{
    extract::State,
    http::StatusCode,
    response::Html,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use std::sync::Arc;
use think_ai_consciousness::ConsciousnessEngine;
use think_ai_core::engine::{EngineConfig, O1Engine};
use think_ai_knowledge::{
    enhanced_quantum_llm::EnhancedQuantumLLM,
    enhanced_response_generator::EnhancedResponseGenerator, knowledge_engine::KnowledgeEngine,
    qwen_knowledge_builder::QwenKnowledgeBuilder,
    realtime_knowledge_component::RealtimeKnowledgeComponent,
    simple_cache_component::SimpleCacheComponent,
};
use think_ai_qwen::client::QwenClient;
use tokio::sync::RwLock;
use tracing::info;

#[derive(Clone)]
struct FullAppState {
    engine: Arc<O1Engine>,
    consciousness: Arc<ConsciousnessEngine>,
    knowledge: Arc<KnowledgeEngine>,
    quantum_llm: Arc<RwLock<EnhancedQuantumLLM>>,
    response_generator: Arc<RwLock<EnhancedResponseGenerator>>,
    qwen_client: Arc<QwenClient>,
}

#[derive(Deserialize)]
struct ChatRequest {
    message: String,
}

#[derive(Serialize)]
struct ChatResponse {
    response: String,
    confidence: f64,
    processing_time_ms: f64,
}

#[tokio::main]
async fn main() {
    // Initialize logging
    tracing_subscriber::fmt::init();

    info!("Starting Full Server with Qwen AI...");

    // Initialize all components
    let __engine = Arc::new(O1Engine::new(EngineConfig::default()));
    let __consciousness = Arc::new(ConsciousnessEngine::new());
    let __knowledge = Arc::new(KnowledgeEngine::new());
    let __quantum_llm = Arc::new(RwLock::new(EnhancedQuantumLLM::new()));
    let __response_generator = Arc::new(RwLock::new(EnhancedResponseGenerator::new()));
    let __qwen_client = Arc::new(QwenClient::new());

    let __state = FullAppState {
        engine,
        consciousness,
        knowledge,
        quantum_llm,
        response_generator,
        qwen_client,
    };

    // Build router
    let __app = Router::new()
        .route("/", get(root))
        .route("/health", get(health))
        .route("/api/chat", post(chat))
        .with_state(state);

    let __addr = SocketAddr::from(([127, 0, 0, 1], 8080));
    info!("Server listening on {}", addr);

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn root() -> Html<&'static str> {
    Html("<h1>Think AI Full Server with Qwen</h1>")
}

async fn health() -> &'static str {
    "OK"
}

async fn chat(
    State(state): State<FullAppState>,
    Json(req): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    let __start = std::time::Instant::now();

    // Process with Qwen
    let __response = match state.qwen_client.generate(&req.message).await {
        Ok(resp) => resp,
        Err(_) => {
            // Fallback to O(1) engine
            state.engine.query(&req.message)
        }
    };

    let __processing_time_ms = start.elapsed().as_secs_f64() * 1000.0;

    Ok(Json(ChatResponse {
        response,
        confidence: 0.95,
        processing_time_ms,
    }))
}
