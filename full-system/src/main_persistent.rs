use axum::{
    extract::{Json, Path, State},
    http::{StatusCode, header},
    response::{Html, Response, IntoResponse},
    routing::{get, post},
    Router,
};
// Removed CookieJar imports since we're using session-based persistence instead
use serde::{Deserialize, Serialize};
use std::{
    env,
    sync::Arc,
};
use tokio::sync::broadcast;
use tower_http::{
    cors::{Any, CorsLayer},
    services::ServeDir,
    trace::TraceLayer,
};
use tracing::info;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use uuid::Uuid;

// Import actual Think AI components
use think_ai_consciousness::ConsciousnessFramework;
use think_ai_core::{EngineConfig, O1ConsciousnessEngine, O1Engine};
use think_ai_knowledge::{KnowledgeDomain, KnowledgeEngine, KnowledgeNode};
use think_ai_qwen::{QwenClient, QwenRequest};
use think_ai_vector::{LSHConfig, O1VectorIndex};
use think_ai_storage::PersistentConversationMemory;

// State for the application
#[derive(Clone)]
struct ThinkAIState {
    core_engine: Arc<O1Engine>,
    knowledge_engine: Arc<KnowledgeEngine>,
    vector_index: Arc<O1VectorIndex>,
    consciousness_framework: Arc<ConsciousnessFramework>,
    persistent_memory: Arc<PersistentConversationMemory>,
    message_channel: broadcast::Sender<ChatMessage>,
    qwen_client: Arc<QwenClient>,
}

#[derive(Clone, Serialize, Deserialize)]
struct ChatMessage {
    id: String,
    session_id: String,
    role: String,
    content: String,
    timestamp: chrono::DateTime<chrono::Utc>,
    response_time_ms: f64,
}

#[derive(Deserialize)]
struct ChatRequest {
    message: String,
    session_id: Option<String>,
}

#[derive(Serialize)]
struct ChatResponse {
    response: String,
    session_id: String,
    confidence: f64,
    response_time_ms: f64,
    consciousness_level: String,
}

#[axum::debug_handler]
async fn chat_handler(
    State(state): State<ThinkAIState>,
    Json(req): Json<ChatRequest>,
) -> impl IntoResponse {
    let start = std::time::Instant::now();

    // Generate a user ID for session tracking
    let user_id = Uuid::new_v4().to_string();

    // Use session_id from request or create new one
    let session_id = req.session_id.unwrap_or_else(|| {
        // Create session ID that includes user ID for better tracking
        format!("{}_{}", user_id, Uuid::new_v4())
    });

    // Check if user wants to delete history
    if state.persistent_memory.check_delete_command(&session_id, &req.message).await {
        // Delete the session
        if let Err(e) = state.persistent_memory.delete_session(&session_id).await {
            tracing::error!("Failed to delete session: {}", e);
        }
        
        return Json(ChatResponse {
            response: "Your chat history has been deleted successfully. Starting fresh!".to_string(),
            session_id: format!("{}_{}", user_id, Uuid::new_v4()), // New session
            confidence: 1.0,
            response_time_ms: start.elapsed().as_micros() as f64 / 1000.0,
            consciousness_level: serde_json::json!({"state": "aware", "processing": true}).to_string(),
        });
    }

    // Process with consciousness framework
    let consciousness_state = serde_json::json!({
        "state": "aware",
        "processing": true
    });
    
    // Add user message to persistent memory
    if let Err(e) = state.persistent_memory.add_message(
        session_id.clone(),
        "user".to_string(),
        req.message.clone(),
    ).await {
        tracing::error!("Failed to add message to persistent memory: {}", e);
    }
    
    // Get conversation history for context
    let conversation_context = state.persistent_memory
        .get_conversation_context(&session_id, 20) // Get last 20 messages
        .await
        .map(|messages| {
            messages.iter()
                .map(|(role, content)| format!("{}: {}", role, content))
                .collect::<Vec<_>>()
                .join("\n")
        })
        .unwrap_or_default();

    // Generate response using knowledge engine
    let response = generate_ai_response(&req.message, &state, &conversation_context).await;

    let response_time_ms = start.elapsed().as_micros() as f64 / 1000.0;

    // Add assistant response to persistent memory
    if let Err(e) = state.persistent_memory.add_message(
        session_id.clone(),
        "assistant".to_string(),
        response.clone(),
    ).await {
        tracing::error!("Failed to add assistant message to persistent memory: {}", e);
    }

    // Broadcast message
    let _ = state.message_channel.send(ChatMessage {
        id: Uuid::new_v4().to_string(),
        session_id: session_id.clone(),
        role: "assistant".to_string(),
        content: response.clone(),
        timestamp: chrono::Utc::now(),
        response_time_ms,
    });

    Json(ChatResponse {
        response,
        session_id,
        confidence: 0.95,
        response_time_ms,
        consciousness_level: consciousness_state.to_string(),
    })
}

async fn generate_ai_response(message: &str, state: &ThinkAIState, conversation_context: &str) -> String {
    // Gather context from knowledge engine
    let mut context = String::new();

    // Try to get relevant knowledge from the knowledge engine
    if let Some(nodes) = state.knowledge_engine.query(message) {
        for (i, node) in nodes.iter().take(3).enumerate() {
            if i > 0 {
                context.push_str("\n");
            }
            context.push_str(&format!("Knowledge {}: {}", i + 1, node.content));
        }
    }

    // Also check intelligent query for additional context
    let intelligent_results = state.knowledge_engine.intelligent_query(message);
    if !intelligent_results.is_empty() && context.is_empty() {
        for (i, node) in intelligent_results.iter().take(2).enumerate() {
            if i > 0 {
                context.push_str("\n");
            }
            context.push_str(&format!("Related: {}", node.content));
        }
    }

    // Combine conversation context with knowledge context
    let full_context = if !conversation_context.is_empty() {
        if context.is_empty() {
            format!("Previous conversation:\n{}", conversation_context)
        } else {
            format!("Previous conversation:\n{}\n\nRelevant knowledge:\n{}", conversation_context, context)
        }
    } else {
        context
    };

    // Create Qwen request with context
    let qwen_request = QwenRequest {
        query: message.to_string(),
        context: if full_context.is_empty() { None } else { Some(full_context) },
        system_prompt: Some("You are Think AI, an advanced AI system with eternal memory. You remember all conversations with users unless explicitly asked to forget. Provide thoughtful, accurate, and engaging responses based on the conversation history.".to_string()),
    };

    // Try to generate response with Qwen
    match state.qwen_client.generate(qwen_request).await {
        Ok(response) => response.content,
        Err(e) => {
            // Log error and provide a simple fallback
            tracing::warn!("Qwen generation failed: {}", e);
            format!(
                "I understand you're asking about {}. While I'm having trouble accessing my full capabilities at the moment, I'd be happy to help explore this topic with you. Could you provide more details about what specific aspect interests you?",
                message
            )
        }
    }
}

#[tokio::main]
async fn main() {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info,think_ai=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    // Initialize engines
    info!("Initializing Think AI Persistent Server...");
    
    let config = EngineConfig::default();
    let core_engine = Arc::new(O1Engine::new(config));
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    let lsh_config = LSHConfig::default();
    let vector_index = Arc::new(O1VectorIndex::new(lsh_config).unwrap());
    let consciousness_framework = Arc::new(ConsciousnessFramework::new());
    
    // Initialize persistent memory
    let db_path = env::var("THINK_AI_DB_PATH").unwrap_or_else(|_| "./think_ai_sessions.db".to_string());
    let persistent_memory = Arc::new(
        PersistentConversationMemory::new(&db_path)
            .await
            .expect("Failed to initialize persistent memory")
    );
    
    let (tx, _rx) = broadcast::channel(100);
    let qwen_client = Arc::new(QwenClient::new());

    let state = ThinkAIState {
        core_engine,
        knowledge_engine,
        vector_index,
        consciousness_framework,
        persistent_memory,
        message_channel: tx,
        qwen_client,
    };

    // Build router
    let app = Router::new()
        .route("/", get(|| async { Html(include_str!("../../minimal_3d.html")) }))
        .route("/health", get(|| async { "OK" }))
        .route("/api/chat", post(chat_handler))
        .layer(
            CorsLayer::new()
                .allow_origin(Any)
                .allow_methods(Any)
                .allow_headers(Any),
        )
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    let addr = format!("0.0.0.0:{}", env::var("PORT").unwrap_or_else(|_| "8080".to_string()));
    info!("Think AI Persistent Server listening on {}", addr);
    
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}