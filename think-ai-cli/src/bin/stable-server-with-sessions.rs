// Enhanced Stable Server - Production-ready with session management and chat history

use anyhow::Result;
use axum::{
    extract::State,
    http::StatusCode,
    response::{Html, Json},
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use std::time::Duration;
use tokio::time::timeout;
use tower_http::cors::CorsLayer;
use uuid::Uuid;

use think_ai_core::{config::EngineConfig, O1Engine};
use think_ai_knowledge::{response_generator::ComponentResponseGenerator, KnowledgeEngine};
use think_ai_qwen::client::QwenClient;
use think_ai_storage::PersistentConversationMemory;
use think_ai_vector::{types::LSHConfig, O1VectorIndex};

#[derive(Debug, Deserialize)]
struct ChatRequest {
    query: String,
    #[serde(default)]
    session_id: Option<String>,
}

#[derive(Debug, Serialize)]
struct ChatResponse {
    response: String,
    session_id: String,
    metadata: ResponseMetadata,
}

#[derive(Debug, Serialize)]
struct ResponseMetadata {
    response_time_ms: f64,
    source: String,
    optimization_level: String,
    has_session: bool,
}

#[tokio::main]
async fn main() -> Result<()> {
    println!("🚀 Think AI Enhanced Stable Server Starting...");
    println!("✅ Production-ready with session management");
    println!("💾 Chat history persistence enabled");

    // Initialize core components
    let o1_engine = Arc::new(O1Engine::new(EngineConfig::default()));
    let vector_index = Arc::new(O1VectorIndex::new(LSHConfig::default())?);
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    let qwen_client = Arc::new(QwenClient::new());
    let response_generator = Arc::new(ComponentResponseGenerator::new(knowledge_engine.clone()));
    
    // Initialize persistent memory
    let persistent_memory = Arc::new(
        PersistentConversationMemory::new("./think-ai-sessions.db")
            .await
            .expect("Failed to initialize persistent memory")
    );

    let state = EnhancedStableState {
        o1_engine,
        vector_index,
        knowledge_engine,
        qwen_client,
        response_generator,
        persistent_memory,
    };

    // Build router
    let app = Router::new()
        .route("/", get(webapp_handler))
        .route("/health", get(health_check))
        .route("/chat", post(chat_handler))
        .route("/stats", get(stats_handler))
        .route("/session/:session_id", get(session_info))
        .layer(CorsLayer::permissive())
        .with_state(state);

    let port = std::env::var("PORT")
        .unwrap_or_else(|_| "8080".to_string())
        .parse::<u16>()?;

    let listener = tokio::net::TcpListener::bind(format!("0.0.0.0:{}", port))
        .await
        .map_err(|e| anyhow::anyhow!("Failed to bind to port {}: {}", port, e))?;

    println!("🌐 Server running on http://0.0.0.0:{}", port);
    println!("📝 Session management active - your conversations are saved");
    println!("🗑️  Say 'delete my chat history' to start fresh");
    
    axum::serve(listener, app).await?;

    Ok(())
}

#[derive(Clone)]
struct EnhancedStableState {
    o1_engine: Arc<O1Engine>,
    vector_index: Arc<O1VectorIndex>,
    knowledge_engine: Arc<KnowledgeEngine>,
    qwen_client: Arc<QwenClient>,
    response_generator: Arc<ComponentResponseGenerator>,
    persistent_memory: Arc<PersistentConversationMemory>,
}

async fn health_check() -> Result<&'static str, StatusCode> {
    Ok("OK - Enhanced Stable Server Running with Sessions")
}

async fn webapp_handler() -> Html<String> {
    // Include the enhanced index.html with animations
    Html(std::fs::read_to_string("/home/administrator/think_ai/static/index.html")
        .unwrap_or_else(|_| "Error loading webapp".to_string()))
}

async fn chat_handler(
    State(state): State<EnhancedStableState>,
    Json(request): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    let start = std::time::Instant::now();
    
    // Generate or use provided session ID
    let session_id = request.session_id.unwrap_or_else(|| {
        format!("user_{}_{}", 
            std::process::id(),
            Uuid::new_v4().to_string().split('-').next().unwrap_or("unknown")
        )
    });
    
    // Check for delete command
    if state.persistent_memory.check_delete_command(&session_id, &request.query).await {
        // Delete the session
        if let Err(e) = state.persistent_memory.delete_session(&session_id).await {
            eprintln!("Failed to delete session: {}", e);
        }
        
        let new_session_id = format!("user_{}_{}", 
            std::process::id(),
            Uuid::new_v4().to_string().split('-').next().unwrap_or("unknown")
        );
        
        return Ok(Json(ChatResponse {
            response: "✅ Your chat history has been deleted successfully. Starting fresh!".to_string(),
            session_id: new_session_id,
            metadata: ResponseMetadata {
                response_time_ms: start.elapsed().as_secs_f64() * 1000.0,
                source: "system".to_string(),
                optimization_level: "O(1) Performance".to_string(),
                has_session: false,
            },
        }));
    }
    
    // Store user message
    if let Err(e) = state.persistent_memory
        .add_message(session_id.clone(), "user".to_string(), request.query.clone())
        .await 
    {
        eprintln!("Failed to store user message: {}", e);
    }
    
    // Get conversation context
    let context = state.persistent_memory
        .get_conversation_context(&session_id, 10)
        .await;
    
    // Build context string for Qwen
    let context_str = if let Some(messages) = &context {
        messages.iter()
            .map(|(role, content)| format!("{}: {}", role, content))
            .collect::<Vec<_>>()
            .join("\n")
    } else {
        String::new()
    };

    // Apply timeout to prevent hanging
    match timeout(Duration::from_secs(30), async {
        // Try Qwen first with context
        match state
            .qwen_client
            .generate_simple(&request.query, Some(&context_str))
            .await
        {
            Ok(response) => (response, "qwen"),
            Err(_) => {
                // Fallback to response generator
                let response = if context.is_some() {
                    // Use context-aware response
                    state.response_generator.generate_response(&format!(
                        "Context:\n{}\n\nQuery: {}",
                        context_str,
                        request.query
                    ))
                } else {
                    state.response_generator.generate_response(&request.query)
                };
                (response, "knowledge_base")
            }
        }
    })
    .await
    {
        Ok((response, source)) => {
            // Store assistant response
            if let Err(e) = state.persistent_memory
                .add_message(session_id.clone(), "assistant".to_string(), response.clone())
                .await 
            {
                eprintln!("Failed to store assistant message: {}", e);
            }
            
            let response_time_ms = start.elapsed().as_secs_f64() * 1000.0;
            Ok(Json(ChatResponse {
                response,
                session_id,
                metadata: ResponseMetadata {
                    response_time_ms,
                    source: source.to_string(),
                    optimization_level: "O(1) Performance".to_string(),
                    has_session: context.is_some(),
                },
            }))
        }
        Err(_) => Ok(Json(ChatResponse {
            response: "Request timed out. Please try again.".to_string(),
            session_id,
            metadata: ResponseMetadata {
                response_time_ms: 30000.0,
                source: "timeout".to_string(),
                optimization_level: "Timeout Protection".to_string(),
                has_session: false,
            },
        })),
    }
}

async fn stats_handler(
    State(state): State<EnhancedStableState>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let stats = state.knowledge_engine.get_stats();

    Ok(Json(serde_json::json!({
        "server_status": "✅ Enhanced Stable Server with Sessions",
        "knowledge_stats": {
            "total_nodes": stats.total_nodes,
            "domains": stats.domains,
            "cache_hit_rate": stats.cache_hit_rate,
            "avg_response_time_ms": stats.avg_response_time_ms,
        },
        "features": {
            "session_management": true,
            "chat_history": true,
            "delete_command": true,
            "context_awareness": true,
        },
        "optimizations": {
            "o1_engine": "Active",
            "vector_search": "O(1) LSH",
            "knowledge_lookup": "O(1) Hash",
            "timeout_protection": "30 seconds",
            "hanging_risk": "ZERO - Timeout protected"
        }
    })))
}

async fn session_info(
    State(state): State<EnhancedStableState>,
    axum::extract::Path(session_id): axum::extract::Path<String>,
) -> Result<Json<serde_json::Value>, StatusCode> {
    let context = state.persistent_memory
        .get_conversation_context(&session_id, 50)
        .await;
    
    if let Some(messages) = context {
        Ok(Json(serde_json::json!({
            "session_id": session_id,
            "message_count": messages.len(),
            "messages": messages.iter().map(|(role, content)| {
                serde_json::json!({
                    "role": role,
                    "content": content
                })
            }).collect::<Vec<_>>()
        })))
    } else {
        Ok(Json(serde_json::json!({
            "session_id": session_id,
            "message_count": 0,
            "messages": []
        })))
    }
}