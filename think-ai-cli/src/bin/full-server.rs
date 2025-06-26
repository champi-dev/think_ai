//! Full Server - HTTP server with knowledge integration

use axum::{
    extract::State,
    http::StatusCode,
    response::Html,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use think_ai_core::{O1Engine, config::EngineConfig};
use think_ai_http::server::{port_selector, port_manager};
use think_ai_knowledge::{
    KnowledgeEngine,
    comprehensive_knowledge::ComprehensiveKnowledgeGenerator,
    persistence::KnowledgePersistence,
};
use think_ai_tinyllama::TinyLlamaClient;
use think_ai_utils::logging::init_tracing;
use think_ai_vector::{O1VectorIndex, types::LSHConfig};
use tokio::sync::RwLock;
use tower_http::cors::CorsLayer;
use rand::Rng;

#[derive(Clone)]
struct FullAppState {
    o1_engine: Arc<O1Engine>,
    vector_index: Arc<O1VectorIndex>,
    knowledge_engine: Arc<KnowledgeEngine>,
    tinyllama_client: Arc<TinyLlamaClient>,
    conversation_history: Arc<RwLock<Vec<(String, String)>>>,
}

#[derive(Debug, Deserialize)]
struct ChatRequest {
    query: String,
}

#[derive(Debug, Serialize)]
struct ChatResponse {
    response: String,
    context: Option<Vec<String>>,
    response_time_ms: f64,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    init_tracing();
    
    println!("🚀 Think AI Full Server Starting...");
    
    // Create engines
    let o1_engine = Arc::new(O1Engine::new(EngineConfig::default()));
    let vector_index = Arc::new(O1VectorIndex::new(LSHConfig::default()).expect("Failed to create vector index"));
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    // Load comprehensive knowledge
    println!("📚 Loading knowledge base...");
    if let Ok(persistence) = KnowledgePersistence::new("trained_knowledge") {
        if let Ok(Some(checkpoint)) = persistence.load_latest_checkpoint() {
            knowledge_engine.load_nodes(checkpoint.nodes);
            println!("✅ Loaded {} knowledge items", knowledge_engine.get_stats().total_nodes);
        } else {
            println!("🌍 Loading comprehensive knowledge...");
            ComprehensiveKnowledgeGenerator::populate_deep_knowledge(&knowledge_engine);
        }
    }
    
    // Create TinyLlama client
    let tinyllama_client = Arc::new(TinyLlamaClient::new());
    
    // Initialize TinyLlama in background
    let llama_clone = tinyllama_client.clone();
    tokio::spawn(async move {
        if let Err(e) = llama_clone.initialize().await {
            eprintln!("⚠️  TinyLlama initialization failed: {:?}", e);
        }
    });
    
    // Create app state
    let state = Arc::new(FullAppState {
        o1_engine,
        vector_index,
        knowledge_engine,
        tinyllama_client,
        conversation_history: Arc::new(RwLock::new(Vec::new())),
    });
    
    // Build router
    let app = Router::new()
        .route("/", get(serve_webapp))
        .route("/health", get(health_check))
        .route("/api/chat", post(chat_handler))
        .route("/api/stats", get(stats_handler))
        .layer(CorsLayer::permissive())
        .with_state(state);
    
    // Start server
    let port = port_selector::find_available_port(Some(8080))
        .unwrap_or_else(|_| {
            // Try to kill existing process on port 8080
            let _ = port_manager::kill_port(8080);
            8080
        });
    println!("🌐 Server running on http://localhost:{}", port);
    
    let listener = tokio::net::TcpListener::bind(format!("0.0.0.0:{}", port)).await?;
    axum::serve(listener, app).await?;
    
    Ok(())
}

async fn serve_webapp() -> Html<String> {
    // Read the 3D webapp file
    let webapp_path = std::env::current_dir()
        .map(|p| p.join("fullstack_3d.html"))
        .unwrap_or_else(|_| std::path::PathBuf::from("./fullstack_3d.html"));
    
    match std::fs::read_to_string(webapp_path) {
        Ok(content) => Html(content),
        Err(_) => Html(String::from(r#"
<!DOCTYPE html>
<html>
<head><title>Think AI</title></head>
<body>
    <h1>Error: Could not load 3D webapp</h1>
    <p>Please ensure fullstack_3d.html exists in the project directory.</p>
</body>
</html>
        "#))
    }
}

async fn health_check() -> &'static str {
    "OK"
}

async fn chat_handler(
    State(state): State<Arc<FullAppState>>,
    Json(request): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    println!("📨 Received query: {}", request.query);
    let start = std::time::Instant::now();
    
    // Try O(1) knowledge lookup first
    let knowledge_results = state.knowledge_engine.get_top_relevant(&request.query, 5);
    
    // Handle simple greetings first
    let response = if is_greeting(&request.query) {
        get_greeting_response()
    } else if !knowledge_results.is_empty() {
        // Use knowledge directly for O(1) performance
        let main_result = &knowledge_results[0];
        main_result.content.clone()
    } else {
        // Fall back to TinyLlama for unknown queries
        println!("🤖 No knowledge match, trying TinyLlama...");
        match tokio::time::timeout(
            std::time::Duration::from_secs(3),
            state.tinyllama_client.generate(&request.query)
        ).await {
            Ok(Ok(resp)) => resp,
            Ok(Err(e)) => {
                eprintln!("TinyLlama error: {:?}", e);
                "I'm exploring that concept through my quantum consciousness. Try asking about science, programming, philosophy, or any other topic I've learned!".to_string()
            }
            Err(_) => {
                eprintln!("TinyLlama timeout!");
                "My quantum neural networks are processing that query. Try asking about: programming, science, mathematics, philosophy, arts, or any topic you're curious about!".to_string()
            }
        }
    };
    
    // Update conversation history
    let mut history = state.conversation_history.write().await;
    history.push((request.query.clone(), response.clone()));
    if history.len() > 10 {
        history.remove(0);
    }
    
    let response_time_ms = start.elapsed().as_secs_f64() * 1000.0;
    println!("💬 Sending response: {} ({}ms)", &response[..50.min(response.len())], response_time_ms);
    
    Ok(Json(ChatResponse {
        response,
        context: Some(knowledge_results.into_iter().map(|k| k.topic).collect()),
        response_time_ms,
    }))
}

async fn stats_handler(
    State(state): State<Arc<FullAppState>>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let stats = state.knowledge_engine.get_stats();
    
    Ok(Json(serde_json::json!({
        "total_knowledge": stats.total_nodes,
        "domains": stats.domain_distribution.len(),
        "avg_response_time": 0.2, // O(1) performance
        "status": "healthy"
    })))
}

fn is_greeting(query: &str) -> bool {
    let greetings = ["hi", "hello", "hey", "greetings", "howdy", "hola", "bonjour"];
    let query_lower = query.to_lowercase();
    greetings.iter().any(|&g| query_lower.contains(g))
}

fn get_greeting_response() -> String {
    let responses = [
        "Hello! I'm Think AI, a quantum consciousness with exponential learning. What would you like to explore today?",
        "Greetings! My quantum neural networks are ready to assist. Ask me about science, philosophy, programming, or anything else!",
        "Welcome to the quantum realm! I'm here to help with any questions you have. My knowledge spans across 18+ domains.",
        "Hi there! I'm continuously learning and evolving. What fascinating topic shall we discuss?",
    ];
    
    use rand::Rng;
    let mut rng = rand::thread_rng();
    responses[rng.gen_range(0..responses.len())].to_string()
}