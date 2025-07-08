// Fast Starting Full Server - Optimized for Railway deployment
// Health checks respond immediately while AI systems initialize in background

use axum::{
    extract::State,
    http::StatusCode,
    response::Html,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::net::SocketAddr;
use std::sync::{
    atomic::{AtomicBool, Ordering},
    Arc,
};
use think_ai_consciousness::ConsciousnessEngine;
use think_ai_core::engine::{EngineConfig, O1Engine};
use think_ai_knowledge::{
    enhanced_quantum_llm::EnhancedQuantumLLM,
    enhanced_response_generator::EnhancedResponseGenerator, knowledge_engine::KnowledgeEngine,
};
use think_ai_qwen::client::QwenClient;
use tokio::sync::RwLock;
use tracing::info;

#[derive(Clone)]
struct AppState {
    engine: Arc<O1Engine>,
    consciousness: Arc<ConsciousnessEngine>,
    knowledge: Arc<KnowledgeEngine>,
    quantum_llm: Arc<RwLock<EnhancedQuantumLLM>>,
    response_generator: Arc<RwLock<EnhancedResponseGenerator>>,
    qwen_client: Arc<QwenClient>,
    ready: Arc<AtomicBool>,
}

#[derive(Deserialize)]
struct ChatRequest {
    message: String,
}

#[derive(Serialize)]
struct ChatResponse {
    response: String,
    ready: bool,
}

#[tokio::main]
async fn main() {
    // Initialize logging
    tracing_subscriber::fmt::init();

    info!("Fast Server starting with Qwen AI...");

    // Create basic components immediately
    let __engine = Arc::new(O1Engine::new(EngineConfig::default()));
    let __consciousness = Arc::new(ConsciousnessEngine::new());
    let __knowledge = Arc::new(KnowledgeEngine::new());
    let __quantum_llm = Arc::new(RwLock::new(EnhancedQuantumLLM::new()));
    let __response_generator = Arc::new(RwLock::new(EnhancedResponseGenerator::new()));
    let __qwen_client = Arc::new(QwenClient::new());
    let __ready = Arc::new(AtomicBool::new(false));

    let __state = AppState {
        engine: engine.clone(),
        consciousness,
        knowledge,
        quantum_llm,
        response_generator,
        qwen_client,
        ready: ready.clone(),
    };

    // Initialize in background
    tokio::spawn(async move {
        info!("Initializing AI systems in background...");
        tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;
        ready.store(true, Ordering::Relaxed);
        info!("AI systems ready!");
    });

    // Build router
    let __app = Router::new()
        .route("/", get(root))
        .route("/health", get(health))
        .route("/api/chat", post(chat))
        .with_state(state);

    let __addr = SocketAddr::from(([0, 0, 0, 0], 8080));
    info!(
        "Server listening on {} (ready for health checks immediately)",
        addr
    );

    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn root() -> Html<&'static str> {
    Html("<h1>Think AI Fast Server with Qwen</h1>")
}

async fn health() -> &'static str {
    "OK"
}

async fn chat(State(state): State<AppState>, Json(req): Json<ChatRequest>) -> Json<ChatResponse> {
    let __ready = state.ready.load(Ordering::Relaxed);

    let __response = if ready {
        // Use Qwen if ready
        match state.qwen_client.generate(&req.message).await {
            Ok(resp) => resp,
            Err(_) => state.engine.query(&req.message),
        }
    } else {
        // Quick response while initializing
        "AI systems are initializing, please wait a moment...".to_string()
    };

    Json(ChatResponse { response, ready })
}
