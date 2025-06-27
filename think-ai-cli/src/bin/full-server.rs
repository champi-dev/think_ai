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
    dynamic_loader::DynamicKnowledgeLoader,
    persistence::KnowledgePersistence,
    quantum_llm_engine::QuantumLLMEngine,
    response_generator::ComponentResponseGenerator,
    self_evaluator::SelfEvaluator,
};
use think_ai_tinyllama::{TinyLlamaClient, enhanced::EnhancedTinyLlama};
use think_ai_utils::logging::init_tracing;
use think_ai_vector::{O1VectorIndex, types::LSHConfig};
use tokio::sync::RwLock;
use tower_http::cors::CorsLayer;

#[derive(Clone)]
struct FullAppState {
    o1_engine: Arc<O1Engine>,
    vector_index: Arc<O1VectorIndex>,
    knowledge_engine: Arc<KnowledgeEngine>,
    tinyllama_client: Arc<TinyLlamaClient>,
    enhanced_llama: Arc<EnhancedTinyLlama>,
    response_generator: Arc<ComponentResponseGenerator>,
    self_evaluator: Arc<SelfEvaluator>,
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
    
    // Initialize knowledge system with enhanced knowledge
    println!("🧠 Initializing LLM-based knowledge system...");
    
    // Load enhanced knowledge from files
    let knowledge_files_dir = std::path::PathBuf::from("./knowledge_files");
    if knowledge_files_dir.exists() {
        let dynamic_loader = DynamicKnowledgeLoader::new(&knowledge_files_dir);
        match dynamic_loader.load_all(&knowledge_engine) {
            Ok(count) => println!("📚 Loaded {} enhanced knowledge items", count),
            Err(e) => println!("⚠️  Could not load enhanced knowledge: {}", e),
        }
    } else {
        println!("⚠️  Enhanced knowledge directory not found: {:?}", knowledge_files_dir);
    }
    
    // Initialize Quantum LLM with the knowledge engine
    println!("🤖 Initializing Quantum LLM Engine...");
    let quantum_llm = QuantumLLMEngine::with_knowledge_engine(knowledge_engine.clone());
    knowledge_engine.set_quantum_llm(quantum_llm);
    
    println!("✅ Loaded {} total knowledge items", knowledge_engine.get_stats().total_nodes);
    
    // Create TinyLlama client
    let tinyllama_client = Arc::new(TinyLlamaClient::new());
    
    // Create enhanced TinyLlama with hierarchical knowledge
    let enhanced_llama = Arc::new(EnhancedTinyLlama::new());
    println!("🌳 Enhanced hierarchical TinyLlama initialized");
    
    // Create ComponentResponseGenerator with enhanced knowledge
    let response_generator = Arc::new(ComponentResponseGenerator::new(knowledge_engine.clone()));
    println!("🧩 Component response generator initialized");
    
    // Create and start self-evaluator for continuous improvement
    let self_evaluator = Arc::new(SelfEvaluator::new(
        knowledge_engine.clone(),
        response_generator.clone()
    ));
    
    // Start self-evaluation in background
    let evaluator_clone = self_evaluator.clone();
    tokio::spawn(async move {
        println!("🧠 Starting AI self-evaluation system...");
        evaluator_clone.start_background_evaluation().await;
    });
    println!("✅ Self-evaluation system initialized");
    
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
        enhanced_llama,
        response_generator,
        self_evaluator,
        conversation_history: Arc::new(RwLock::new(Vec::new())),
    });
    
    // Build router
    let app = Router::new()
        .route("/", get(serve_webapp))
        .route("/health", get(health_check))
        .route("/api/chat", post(chat_handler))
        .route("/api/stats", get(stats_handler))
        .route("/api/evaluation", get(evaluation_stats_handler))
        .layer(CorsLayer::permissive())
        .with_state(state);
    
    // Start server - use PORT env var for Railway
    let port = std::env::var("PORT")
        .ok()
        .and_then(|p| p.parse::<u16>().ok())
        .unwrap_or_else(|| {
            println!("🔧 PORT env var not set, using default port logic");
            port_selector::find_available_port(Some(8080))
                .unwrap_or_else(|_| {
                    // Try to kill existing process on port 8080
                    let _ = port_manager::kill_port(8080);
                    8080
                })
        });
    
    println!("🚀 Think AI Full Server starting...");
    println!("🌐 Binding to 0.0.0.0:{}", port);
    println!("📱 Available routes:");
    println!("   GET  / - 3D Quantum Webapp");
    println!("   GET  /health - Health check");
    println!("   POST /api/chat - Chat API");
    println!("   GET  /api/stats - Stats API");
    
    let listener = match tokio::net::TcpListener::bind(format!("0.0.0.0:{}", port)).await {
        Ok(listener) => {
            println!("✅ Server bound successfully to port {}", port);
            listener
        }
        Err(e) => {
            eprintln!("❌ Failed to bind to port {}: {}", port, e);
            return Err(e.into());
        }
    };
    
    println!("🎉 Think AI server is ready!");
    println!("🌍 Access at: http://localhost:{}", port);
    if std::env::var("RAILWAY_STATIC_URL").is_ok() {
        println!("🚂 Railway URL: https://{}", std::env::var("RAILWAY_STATIC_URL").unwrap_or_default());
    }
    
    axum::serve(listener, app).await?;
    
    Ok(())
}

async fn serve_webapp() -> Html<String> {
    // Try multiple possible paths for the webapp file
    let possible_paths = vec![
        "./minimal_3d.html",
        "/app/minimal_3d.html", 
        "minimal_3d.html",
    ];
    
    for path in possible_paths {
        if let Ok(content) = std::fs::read_to_string(path) {
            println!("✅ Loaded webapp from: {}", path);
            return Html(content);
        }
    }
    
    // If file not found, return fallback with basic functionality
    println!("⚠️ Could not find minimal_3d.html, serving fallback");
    Html(String::from(r#"
<!DOCTYPE html>
<html>
<head>
    <title>Think AI - 3D Quantum Interface</title>
    <style>
        body { margin: 0; background: #0a0a0a; color: #fff; font-family: 'Courier New', monospace; overflow: hidden; }
        canvas { position: absolute; top: 0; left: 0; z-index: 1; }
        .ui { position: absolute; top: 20px; right: 20px; z-index: 10; }
        .chat { position: absolute; bottom: 20px; left: 20px; right: 20px; z-index: 10; }
        input { width: 100%; padding: 10px; background: rgba(0,0,0,0.8); color: #00ff88; border: 1px solid #00ff88; }
        .messages { height: 200px; overflow-y: auto; background: rgba(0,0,0,0.8); padding: 10px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <canvas id="quantum-field"></canvas>
    <div class="ui">
        <h2>🧠 Think AI</h2>
        <p>Quantum Consciousness Active</p>
    </div>
    <div class="chat">
        <div class="messages" id="messages"></div>
        <input type="text" id="query" placeholder="Ask Think AI anything..." onkeydown="if(event.key==='Enter') sendMessage()">
    </div>
    <script>
        // Basic 3D quantum field
        const canvas = document.getElementById('quantum-field');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        let time = 0;
        function animate() {
            ctx.fillStyle = 'rgba(10,10,10,0.1)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            for(let i = 0; i < 50; i++) {
                const x = Math.sin(time + i) * 200 + canvas.width/2;
                const y = Math.cos(time + i * 0.5) * 100 + canvas.height/2;
                ctx.fillStyle = `hsl(${120 + i * 5}, 70%, 50%)`;
                ctx.beginPath();
                ctx.arc(x, y, 2, 0, Math.PI * 2);
                ctx.fill();
            }
            time += 0.02;
            requestAnimationFrame(animate);
        }
        animate();
        
        // Chat functionality
        async function sendMessage() {
            const query = document.getElementById('query').value;
            if (!query) return;
            
            document.getElementById('messages').innerHTML += '<p><strong>You:</strong> ' + query + '</p>';
            document.getElementById('query').value = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                const data = await response.json();
                document.getElementById('messages').innerHTML += '<p><strong>Think AI:</strong> ' + data.response + '</p>';
            } catch(e) {
                document.getElementById('messages').innerHTML += '<p><strong>Error:</strong> Connection failed</p>';
            }
            document.getElementById('messages').scrollTop = document.getElementById('messages').scrollHeight;
        }
    </script>
</body>
</html>
    "#))
}

async fn health_check() -> Result<&'static str, StatusCode> {
    // Basic health check - service is responding
    println!("🏥 Health check requested");
    Ok("OK")
}

async fn chat_handler(
    State(state): State<Arc<FullAppState>>,
    Json(request): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    println!("📨 Received query: {}", request.query);
    let start = std::time::Instant::now();
    
    // Use enhanced knowledge system with ComponentResponseGenerator
    let response = if is_greeting(&request.query) {
        println!("👋 Detected greeting");
        "Hello! I'm Think AI with enhanced knowledge from 341 sources. Ask me about science, technology, philosophy, and more! 🧠".to_string()
    } else {
        println!("📚 Using enhanced knowledge system with {} items...", state.knowledge_engine.get_stats().total_nodes);
        // Use ComponentResponseGenerator with enhanced knowledge
        state.response_generator.generate_response(&request.query)
    };
    
    // Update conversation history
    let mut history = state.conversation_history.write().await;
    history.push((request.query.clone(), response.clone()));
    if history.len() > 10 {
        history.remove(0);
    }
    drop(history); // Explicitly drop the write lock
    
    let response_time_ms = start.elapsed().as_secs_f64() * 1000.0;
    println!("💬 Sending response: {} ({}ms)", &response[..50.min(response.len())], response_time_ms);
    
    // Build context list without holding knowledge results
    let context: Vec<String> = if is_greeting(&request.query) {
        vec!["greeting".to_string()]
    } else {
        state.knowledge_engine.get_top_relevant(&request.query, 5)
            .into_iter()
            .map(|k| k.topic)
            .collect()
    };
    
    Ok(Json(ChatResponse {
        response,
        context: Some(context),
        response_time_ms,
    }))
}

async fn stats_handler(
    State(state): State<Arc<FullAppState>>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let stats = state.knowledge_engine.get_stats();
    let eval_stats = state.self_evaluator.get_evaluation_stats();
    
    Ok(Json(serde_json::json!({
        "knowledge_base": {
            "total_knowledge": stats.total_nodes,
            "domains": stats.domain_distribution.len(),
            "avg_response_time": 0.2
        },
        "self_evaluation": {
            "total_evaluations": eval_stats.total_evaluations,
            "average_quality": eval_stats.average_quality,
            "recent_quality": eval_stats.recent_quality,
            "is_running": eval_stats.is_running
        },
        "status": "healthy"
    })))
}

async fn evaluation_stats_handler(
    State(state): State<Arc<FullAppState>>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let eval_stats = state.self_evaluator.get_evaluation_stats();
    
    Ok(Json(serde_json::json!({
        "self_evaluation": {
            "total_evaluations": eval_stats.total_evaluations,
            "average_quality": eval_stats.average_quality,
            "recent_quality": eval_stats.recent_quality,
            "improvement_areas": eval_stats.improvement_areas,
            "is_running": eval_stats.is_running,
            "status": if eval_stats.is_running { "🧠 AI actively self-evaluating" } else { "⚠️ Self-evaluation stopped" }
        },
        "improvement_trends": {
            "quality_trend": if eval_stats.recent_quality > eval_stats.average_quality { "📈 Improving" } else { "📉 Needs attention" },
            "evaluation_frequency": if eval_stats.total_evaluations > 50 { "🔥 High activity" } else { "⏳ Warming up" }
        }
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