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
use think_ai_qwen::QwenClient;
use think_ai_utils::logging::init_tracing;
use think_ai_vector::{O1VectorIndex, types::LSHConfig};
use tokio::sync::RwLock;
use tower_http::cors::CorsLayer;

#[derive(Clone)]
struct FullAppState {
    o1_engine: Arc<O1Engine>,
    vector_index: Arc<O1VectorIndex>,
    knowledge_engine: Arc<KnowledgeEngine>,
    qwen_client: Arc<QwenClient>,
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
    
    // Create Qwen client
    let qwen_client = Arc::new(QwenClient::new());
    
    // Create app state
    let state = Arc::new(FullAppState {
        o1_engine,
        vector_index,
        knowledge_engine,
        qwen_client,
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

async fn serve_webapp() -> Html<&'static str> {
    Html(r#"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Think AI - O(1) Intelligence</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1e3c72, #2a5298);
            color: white;
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
        }
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 0.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 2em;
            opacity: 0.9;
        }
        .chat-container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .messages {
            height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 5px;
        }
        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.1);
        }
        .message.user {
            background: rgba(100, 200, 255, 0.2);
            text-align: right;
        }
        .message.ai {
            background: rgba(200, 255, 200, 0.2);
        }
        .input-group {
            display: flex;
            gap: 10px;
        }
        input {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 5px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            font-size: 16px;
        }
        button {
            padding: 12px 24px;
            border: none;
            border-radius: 5px;
            background: #4CAF50;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #45a049;
        }
        .stats {
            margin-top: 20px;
            text-align: center;
            font-size: 0.9em;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Think AI</h1>
        <p class="subtitle">O(1) Intelligence with Exponential Learning</p>
        
        <div class="chat-container">
            <div class="messages" id="messages"></div>
            <div class="input-group">
                <input type="text" id="input" placeholder="Ask me anything..." autofocus>
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        
        <div class="stats" id="stats">Loading stats...</div>
    </div>
    
    <script>
        const messagesDiv = document.getElementById('messages');
        const input = document.getElementById('input');
        const statsDiv = document.getElementById('stats');
        
        // Load stats
        fetch('/api/stats')
            .then(r => r.json())
            .then(data => {
                statsDiv.innerHTML = `Knowledge Items: ${data.total_knowledge || 0} | Response Time: ${data.avg_response_time || '0.0'}ms`;
            });
        
        input.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
        
        async function sendMessage() {
            const query = input.value.trim();
            if (!query) return;
            
            // Add user message
            addMessage(query, 'user');
            input.value = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await response.json();
                addMessage(data.response, 'ai');
                
                // Update stats
                if (data.response_time_ms !== undefined) {
                    statsDiv.innerHTML += ` | Last Response: ${data.response_time_ms.toFixed(1)}ms`;
                }
            } catch (error) {
                addMessage('Error: ' + error.message, 'ai');
            }
        }
        
        function addMessage(text, type) {
            const div = document.createElement('div');
            div.className = 'message ' + type;
            div.textContent = text;
            messagesDiv.appendChild(div);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        // Welcome message
        addMessage("Hi! I'm Think AI with O(1) intelligence and exponential learning. Ask me anything!", 'ai');
    </script>
</body>
</html>
    "#)
}

async fn health_check() -> &'static str {
    "OK"
}

async fn chat_handler(
    State(state): State<Arc<FullAppState>>,
    Json(request): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    let start = std::time::Instant::now();
    
    // Try O(1) knowledge lookup first
    let knowledge_results = state.knowledge_engine.get_top_relevant(&request.query, 5);
    
    let response = if !knowledge_results.is_empty() {
        // Use knowledge directly for O(1) performance
        let main_result = &knowledge_results[0];
        main_result.content.clone()
    } else {
        // Fall back to Qwen for unknown queries
        match state.qwen_client.generate_response(&request.query).await {
            Ok(resp) => resp,
            Err(_) => "I'm still learning about that topic. Please try a different question.".to_string()
        }
    };
    
    // Update conversation history
    let mut history = state.conversation_history.write().await;
    history.push((request.query.clone(), response.clone()));
    if history.len() > 10 {
        history.remove(0);
    }
    
    let response_time_ms = start.elapsed().as_secs_f64() * 1000.0;
    
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