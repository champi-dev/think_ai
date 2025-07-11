use axum::{
    extract::{ws::WebSocket, Path, Query, State, WebSocketUpgrade},
    http::StatusCode,
    response::{Html, Response},
    routing::{get, post},
    Json, Router,
};
// No longer needed - removed unused imports
use serde::{Deserialize, Serialize};
use std::{
    collections::HashMap,
    env,
    sync::{Arc, RwLock},
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
use think_ai_utils::token_counter::{TokenCounter, ConversationCompactor};

// State for the application
#[derive(Clone)]
struct ThinkAIState {
    core_engine: Arc<O1Engine>,
    knowledge_engine: Arc<KnowledgeEngine>,
    vector_index: Arc<O1VectorIndex>,
    consciousness_framework: Arc<ConsciousnessFramework>,
    chat_sessions: Arc<RwLock<HashMap<String, ChatSession>>>,
    message_channel: broadcast::Sender<ChatMessage>,
    qwen_client: Arc<QwenClient>,
}

#[derive(Clone, Serialize, Deserialize)]
struct ChatSession {
    id: String,
    messages: Vec<ChatMessage>,
    created_at: chrono::DateTime<chrono::Utc>,
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
    tokens_used: usize,
    context_tokens: usize,
    compacted: bool,
}

async fn chat_handler(
    State(state): State<ThinkAIState>,
    Json(req): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    let start = std::time::Instant::now();

    // Get or create session
    let session_id = req.session_id.unwrap_or_else(|| Uuid::new_v4().to_string());

    // Process with consciousness framework
    let consciousness_state = serde_json::json!({
        "state": "aware",
        "processing": true
    });
    
    // Token management
    const MAX_TOKENS: usize = 5000;
    const RESERVED_TOKENS: usize = 1000; // For system prompt + query + response
    
    let token_counter = TokenCounter::new();
    let compactor = ConversationCompactor::new(MAX_TOKENS);
    
    // Get conversation history and manage token limits
    let (conversation_context, compacted, context_tokens) = {
        let sessions = state.chat_sessions.read().unwrap();
        if let Some(session) = sessions.get(&session_id) {
            let messages: Vec<(String, String)> = session.messages.iter()
                .map(|msg| (msg.role.clone(), msg.content.clone()))
                .collect();
            
            // Check if we need to compact
            let total_tokens = token_counter.count_conversation(&messages);
            let query_tokens = token_counter.count(&req.message);
            
            if total_tokens + query_tokens > MAX_TOKENS - RESERVED_TOKENS {
                // Need to compact the conversation
                let compacted_messages = compactor.compact(&messages, RESERVED_TOKENS + query_tokens);
                let context = compacted_messages.iter()
                    .map(|(role, content)| format!("{}: {}", role, content))
                    .collect::<Vec<_>>()
                    .join("\n");
                let tokens = token_counter.count(&context);
                (context, true, tokens)
            } else {
                let context = messages.iter()
                    .map(|(role, content)| format!("{}: {}", role, content))
                    .collect::<Vec<_>>()
                    .join("\n");
                let tokens = token_counter.count(&context);
                (context, false, tokens)
            }
        } else {
            (String::new(), false, 0)
        }
    };

    // Generate response using knowledge engine
    let response = generate_ai_response(&req.message, &state, &conversation_context).await;

    let response_time_ms = start.elapsed().as_micros() as f64 / 1000.0;

    // Count tokens in response
    let tokens_used = token_counter.count(&response);
    
    // Store message
    let user_msg = ChatMessage {
        id: Uuid::new_v4().to_string(),
        session_id: session_id.clone(),
        role: "user".to_string(),
        content: req.message,
        timestamp: chrono::Utc::now(),
        response_time_ms: 0.0,
    };

    let ai_msg = ChatMessage {
        id: Uuid::new_v4().to_string(),
        session_id: session_id.clone(),
        role: "assistant".to_string(),
        content: response.clone(),
        timestamp: chrono::Utc::now(),
        response_time_ms,
    };

    // Update session
    {
        let mut sessions = state.chat_sessions.write().unwrap();
        let session = sessions.entry(session_id.clone()).or_insert(ChatSession {
            id: session_id.clone(),
            messages: Vec::new(),
            created_at: chrono::Utc::now(),
        });
        session.messages.push(user_msg.clone());
        session.messages.push(ai_msg.clone());
    }

    // Broadcast messages
    let _ = state.message_channel.send(user_msg);
    let _ = state.message_channel.send(ai_msg);

    Ok(Json(ChatResponse {
        response,
        session_id,
        confidence: 0.95,
        response_time_ms,
        consciousness_level: format!("{:?}", consciousness_state),
        tokens_used,
        context_tokens,
        compacted,
    }))
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
        system_prompt: Some("You are Think AI, an advanced AI system powered by O(1) algorithms and consciousness engine. Provide thoughtful, accurate, and engaging responses.".to_string()),
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

async fn health() -> &'static str {
    "OK"
}

fn initialize_knowledge(engine: &KnowledgeEngine) {
    // Mathematics domain
    engine.add_knowledge(
        KnowledgeDomain::Mathematics,
        "Mathematics is the study of patterns, structures, and logical relationships.",
    );
    engine.add_knowledge(
        KnowledgeDomain::Mathematics,
        "Key areas include algebra, calculus, geometry, statistics, and number theory.",
    );

    // Science domain
    engine.add_knowledge(
        KnowledgeDomain::Science,
        "Science is the systematic study of the natural world through observation and experimentation.",
    );
    engine.add_knowledge(
        KnowledgeDomain::Science,
        "Major branches include physics, chemistry, biology, astronomy, and earth sciences.",
    );

    // Technology domain
    engine.add_knowledge(
        KnowledgeDomain::Technology,
        "Technology encompasses tools, techniques, and systems created to solve problems and improve human life.",
    );
    engine.add_knowledge(
        KnowledgeDomain::Technology,
        "Key areas include computer science, engineering, AI/ML, robotics, and biotechnology.",
    );

    // Philosophy domain
    engine.add_knowledge(
        KnowledgeDomain::Philosophy,
        "Philosophy examines fundamental questions about existence, knowledge, values, reason, and mind.",
    );
    engine.add_knowledge(
        KnowledgeDomain::Philosophy,
        "Major branches include metaphysics, epistemology, ethics, logic, and aesthetics.",
    );

    // History domain
    engine.add_knowledge(
        KnowledgeDomain::History,
        "History is the study of past events, cultures, and human experiences over time.",
    );
    engine.add_knowledge(
        KnowledgeDomain::History,
        "It helps us understand how societies evolved and provides context for current events.",
    );
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
    info!("Initializing Think AI Server with Token Management...");
    
    let config = EngineConfig::default();
    let mut core_engine = O1Engine::new(config);
    core_engine.initialize().await.unwrap();

    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    initialize_knowledge(&knowledge_engine);

    let vector_index = Arc::new(O1VectorIndex::new(LSHConfig::default()).unwrap());
    let consciousness_framework = Arc::new(ConsciousnessFramework::new());

    // Initialize Qwen client
    let qwen_client = Arc::new(QwenClient::new());

    // Create shared state
    let (tx, _rx) = broadcast::channel(100);
    let state = ThinkAIState {
        core_engine: Arc::new(core_engine),
        knowledge_engine,
        vector_index,
        consciousness_framework,
        chat_sessions: Arc::new(RwLock::new(HashMap::new())),
        message_channel: tx,
        qwen_client,
    };

    // Build router
    let app = Router::new()
        .route("/", get(|| async { Html(include_str!("../../minimal_3d.html")) }))
        .route("/health", get(health))
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
    info!("Think AI Server listening on {}", addr);
    info!("Token limit: 5000 tokens per request");
    info!("Conversation compaction enabled");
    
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    axum::serve(listener, app).await.unwrap();
}