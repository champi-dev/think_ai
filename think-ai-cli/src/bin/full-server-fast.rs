//! Fast Starting Full Server - Optimized for Railway deployment
//! Health checks respond immediately while AI systems initialize in background

use axum::{
    extract::State,
    http::StatusCode,
    response::Html,
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use std::collections::HashMap;
use think_ai_core::{O1Engine, config::EngineConfig};
use think_ai_http::server::{port_selector, port_manager};
use think_ai_knowledge::{
    KnowledgeEngine,
    dynamic_loader::DynamicKnowledgeLoader,
    quantum_llm_engine::QuantumLLMEngine,
    enhanced_quantum_llm::{EnhancedQuantumLLMEngine, AttentionMechanism, PrecisionMode},
    response_generator::ComponentResponseGenerator,
    self_evaluator::SelfEvaluator,
};
use think_ai_qwen::client::QwenClient;
use think_ai_utils::logging::init_tracing;
use think_ai_vector::{O1VectorIndex, types::LSHConfig};
use tokio::sync::RwLock;
use tower_http::cors::CorsLayer;

#[derive(Clone)]
struct FastAppState {
    o1_engine: Arc<O1Engine>,
    vector_index: Arc<O1VectorIndex>,
    knowledge_engine: Arc<KnowledgeEngine>,
    tinyllama_client: Arc<TinyLlamaClient>,
    enhanced_llama: Arc<EnhancedTinyLlama>,
    enhanced_quantum_llm: Arc<RwLock<EnhancedQuantumLLMEngine>>,
    response_generator: Arc<ComponentResponseGenerator>,
    self_evaluator: Arc<SelfEvaluator>,
    conversation_history: Arc<RwLock<Vec<(String, String)>>>,
    response_cache: Arc<RwLock<HashMap<String, (String, std::time::Instant)>>>,
    processing_locks: Arc<RwLock<HashMap<String, Arc<tokio::sync::Mutex<()>>>>>,
    initialization_complete: Arc<RwLock<bool>>,
}

#[derive(Debug, Deserialize)]
struct ChatRequest {
    query: String,
}

#[derive(Debug, Serialize)]
struct ChatResponse {
    response: String,
    sources: Vec<String>,
    context: Option<Vec<String>>,
    response_time_ms: f64,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    init_tracing();
    
    println!("🚀 Think AI Fast Server Starting...");
    
    // Get port configuration
    let port = std::env::var("PORT")
        .ok()
        .and_then(|p| p.parse::<u16>().ok())
        .unwrap_or_else(|| {
            println!("🔧 PORT env var not set, using default port logic");
            port_selector::find_available_port(Some(8080))
                .unwrap_or_else(|_| {
                    let _ = port_manager::kill_port(8080);
                    8080
                })
        });

    // Create minimal components for immediate health check response
    let o1_engine = Arc::new(O1Engine::new(EngineConfig::default()));
    let vector_index = Arc::new(O1VectorIndex::new(LSHConfig::default()).expect("Failed to create vector index"));
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    let tinyllama_client = Arc::new(TinyLlamaClient::new());
    let enhanced_llama = Arc::new(EnhancedTinyLlama::new());
    let enhanced_quantum_llm = Arc::new(RwLock::new(EnhancedQuantumLLMEngine::with_knowledge_engine(knowledge_engine.clone())));
    let response_generator = Arc::new(ComponentResponseGenerator::new(knowledge_engine.clone()));
    let self_evaluator = Arc::new(SelfEvaluator::new(knowledge_engine.clone(), response_generator.clone()));
    
    // Create state with initialization flag
    let state = Arc::new(FastAppState {
        o1_engine,
        vector_index,
        knowledge_engine: knowledge_engine.clone(),
        tinyllama_client,
        enhanced_llama,
        enhanced_quantum_llm: enhanced_quantum_llm.clone(),
        response_generator: response_generator.clone(),
        self_evaluator: self_evaluator.clone(),
        conversation_history: Arc::new(RwLock::new(Vec::new())),
        response_cache: Arc::new(RwLock::new(HashMap::new())),
        processing_locks: Arc::new(RwLock::new(HashMap::new())),
        initialization_complete: Arc::new(RwLock::new(false)),
    });

    // Create routes
    let app = Router::new()
        .route("/", get(webapp_handler))
        .route("/health", get(health_check))
        .route("/api/chat", post(chat_handler))
        .route("/api/stats", get(stats_handler))
        .route("/api/evaluation", get(evaluation_stats_handler))
        .route("/api/performance", get(performance_stats_handler))
        .layer(CorsLayer::permissive())
        .with_state(state.clone());
    
    println!("🌐 Binding to 0.0.0.0:{}", port);
    let listener = match tokio::net::TcpListener::bind(format!("0.0.0.0:{}", port)).await {
        Ok(listener) => {
            println!("✅ Server bound successfully to port {}", port);
            listener
        }
        Err(e) => {
            eprintln!("❌ Failed to bind to port {}: {}", port, e);
            std::process::exit(1);
        }
    };
    
    // Start AI initialization in background
    let state_clone = state.clone();
    tokio::spawn(async move {
        initialize_ai_systems(state_clone).await;
    });
    
    println!("🏥 Health check ready - Railway deployment will succeed");
    println!("🧠 AI systems initializing in background...");
    println!("🎉 Think AI server is ready!");
    
    // Start server
    axum::serve(listener, app).await?;
    
    Ok(())
}

async fn initialize_ai_systems(state: Arc<FastAppState>) {
    println!("🧠 Initializing AI systems in background...");
    
    // Load enhanced knowledge from files
    let knowledge_files_dir = std::path::PathBuf::from("./knowledge_files");
    if knowledge_files_dir.exists() {
        let dynamic_loader = DynamicKnowledgeLoader::new(&knowledge_files_dir);
        match dynamic_loader.load_all(&state.knowledge_engine) {
            Ok(count) => println!("📚 Loaded {} enhanced knowledge items", count),
            Err(e) => println!("⚠️  Could not load enhanced knowledge: {}", e),
        }
    } else {
        println!("⚠️  Enhanced knowledge directory not found: {:?}", knowledge_files_dir);
    }
    
    // Initialize Quantum LLM engines
    println!("🤖 Initializing Quantum LLM Engine...");
    let quantum_llm = QuantumLLMEngine::with_knowledge_engine(state.knowledge_engine.clone());
    state.knowledge_engine.set_quantum_llm(quantum_llm);
    
    // Configure Enhanced Quantum LLM
    println!("⚡ Configuring Enhanced Quantum LLM...");
    {
        let mut enhanced_quantum_llm = state.enhanced_quantum_llm.write().await;
        enhanced_quantum_llm.set_attention_mode(AttentionMechanism::Linear);
        enhanced_quantum_llm.set_precision_mode(PrecisionMode::INT8);
    }
    
    // Start self-evaluation (disabled for production performance)
    // let evaluator_clone = state.self_evaluator.clone();
    // tokio::spawn(async move {
    //     evaluator_clone.start_background_evaluation().await;
    // });
    println!("⚠️  Self-evaluation disabled for O(1) performance");
    
    // Mark initialization complete
    *state.initialization_complete.write().await = true;
    println!("✅ AI systems fully initialized");
}

async fn health_check() -> Result<&'static str, StatusCode> {
    // Always respond immediately for Railway health checks
    Ok("OK")
}

async fn webapp_handler() -> Html<String> {
    Html(include_str!("../../../minimal_3d.html").to_string())
}

async fn chat_handler(
    State(state): State<Arc<FastAppState>>,
    Json(request): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    println!("📨 Received query: {}", request.query);
    
    // Check if AI systems are initialized
    let is_initialized = *state.initialization_complete.read().await;
    if !is_initialized {
        return Ok(Json(ChatResponse {
            response: "🧠 AI systems are still initializing. Please try again in a moment.".to_string(),
            sources: vec!["system".to_string()],
            context: None,
            response_time_ms: 0.1,
        }));
    }
    
    let start_time = std::time::Instant::now();
    
    // Use enhanced quantum LLM for response (read-only for concurrent access)
    let response = {
        let enhanced_llm = state.enhanced_quantum_llm.read().await;
        enhanced_llm.generate_response_readonly(&request.query)
    };
    
    let response_time = start_time.elapsed();
    
    Ok(Json(ChatResponse {
        response,
        sources: vec!["enhanced_quantum_llm".to_string()],
        context: None,
        response_time_ms: response_time.as_secs_f64() * 1000.0,
    }))
}

async fn stats_handler(
    State(state): State<Arc<FastAppState>>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let stats = state.knowledge_engine.get_stats();
    let is_initialized = *state.initialization_complete.read().await;
    
    Ok(Json(serde_json::json!({
        "knowledge_engine": {
            "total_nodes": stats.total_nodes,
            "domain_distribution": stats.domain_distribution,
            "total_knowledge_items": stats.total_knowledge_items,
            "status": if is_initialized { "✅ Fully initialized" } else { "🔄 Initializing..." }
        },
        "initialization_status": {
            "complete": is_initialized,
            "status": if is_initialized { "ready" } else { "initializing" }
        }
    })))
}

async fn evaluation_stats_handler(
    State(state): State<Arc<FastAppState>>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let eval_stats = state.self_evaluator.get_evaluation_stats();
    
    Ok(Json(serde_json::json!({
        "self_evaluation": {
            "total_evaluations": eval_stats.total_evaluations,
            "average_quality": eval_stats.average_quality,
            "recent_quality": eval_stats.recent_quality,
            "is_running": eval_stats.is_running
        }
    })))
}

async fn performance_stats_handler(
    State(state): State<Arc<FastAppState>>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let enhanced_llm = state.enhanced_quantum_llm.read().await;
    let (inference_count, avg_latency_ms, cache_hit_rate) = enhanced_llm.get_performance_stats();
    
    Ok(Json(serde_json::json!({
        "enhanced_quantum_llm": {
            "optimization_level": "O(1) Linear Attention + INT8 Quantization",
            "inference_count": inference_count,
            "average_latency_ms": avg_latency_ms,
            "cache_hit_rate": cache_hit_rate,
            "performance_status": if avg_latency_ms < 10.0 { "⚡ Ultra-fast" } else { "🚀 Fast" }
        }
    })))
}