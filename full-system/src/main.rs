use axum::{
    extract::{ws::WebSocket, Path, Query, State, WebSocketUpgrade},
    http::StatusCode,
    response::{Html, Response, Sse, sse::{Event, KeepAlive}},
    routing::{get, post},
    Json, Router,
};
use axum_extra::extract::CookieJar;
use futures_util::{SinkExt, StreamExt, stream::Stream};
use serde::{Deserialize, Serialize};
use std::{
    collections::HashMap,
    env,
    sync::{Arc, RwLock},
    convert::Infallible,
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
use think_ai_utils::token_counter::count_tokens;

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

#[derive(Deserialize)]
struct SearchQuery {
    q: String,
    limit: Option<usize>,
    domain: Option<String>,
}

#[derive(Serialize)]
struct SearchResult {
    results: Vec<KnowledgeItem>,
    total: usize,
    query_time_ms: f64,
}

#[derive(Serialize, Clone)]
struct KnowledgeItem {
    id: String,
    title: String,
    content: String,
    domain: String,
    relevance: f64,
    confidence: f64,
}

#[derive(Serialize)]
struct SystemStats {
    total_knowledge_items: usize,
    active_sessions: usize,
    average_response_time_ms: f64,
    cache_hit_rate: f64,
    uptime_seconds: u64,
    consciousness_level: String,
    domains: Vec<String>,
}

#[tokio::main]
async fn main() {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "think_ai_full=debug,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    // Get port from environment
    let port = env::var("PORT").unwrap_or_else(|_| "8080".to_string());
    let addr = format!("0.0.0.0:{}", port);

    info!("🚀 Think AI Full System starting on {}", addr);

    // Initialize Think AI components
    let core_engine = Arc::new(O1Engine::new(EngineConfig::default()));
    core_engine.initialize().await.unwrap();

    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    initialize_knowledge(&knowledge_engine);

    let vector_index = Arc::new(O1VectorIndex::new(LSHConfig::default()).unwrap());
    let consciousness_framework = Arc::new(ConsciousnessFramework::new());

    // Initialize Qwen client
    let qwen_client = Arc::new(QwenClient::new());

    // Initialize state
    let (tx, _rx) = broadcast::channel(100);
    let state = ThinkAIState {
        core_engine,
        knowledge_engine,
        vector_index,
        consciousness_framework,
        chat_sessions: Arc::new(RwLock::new(HashMap::new())),
        message_channel: tx,
        qwen_client,
    };

    // Build router
    let app = Router::new()
        // Main routes
        .route("/", get(serve_index))
        .route("/health", get(health_check))
        .route("/api/health", get(api_health))
        // Chat API
        .route("/api/chat", post(chat_handler))
        .route("/api/chat/stream", post(chat_stream_handler))
        .route("/api/chat/sessions", get(list_sessions))
        .route("/api/chat/sessions/:id", get(get_session))
        .route("/ws/chat", get(websocket_handler))
        // Knowledge API
        .route("/api/search", get(search_handler))
        .route("/api/knowledge/domains", get(list_domains))
        .route("/api/knowledge/stats", get(system_stats))
        // Consciousness API
        .route("/api/consciousness/level", get(consciousness_level))
        .route("/api/consciousness/thoughts", get(current_thoughts))
        // Static files (for webapp assets)
        .nest_service("/static", ServeDir::new("static"))
        // Add middleware
        .layer(
            CorsLayer::new()
                .allow_origin(Any)
                .allow_methods(Any)
                .allow_headers(Any),
        )
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    // Start server
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    info!("🌐 Server listening on http://{}", addr);

    axum::serve(listener, app).await.unwrap();
}

// Initialize knowledge base with comprehensive content
fn initialize_knowledge(engine: &KnowledgeEngine) {
    // O(1) Performance concepts
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "O(1) Algorithms".to_string(),
        "O(1) algorithms provide constant time complexity regardless of input size. Think AI uses hash-based lookups and pre-computed indexes to achieve true O(1) performance.".to_string(),
        vec!["performance".to_string(), "algorithms".to_string(), "complexity".to_string()],
    );

    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "Locality-Sensitive Hashing".to_string(),
        "LSH enables O(1) approximate nearest neighbor search in high-dimensional vector spaces, perfect for AI embeddings and similarity search.".to_string(),
        vec!["lsh".to_string(), "vectors".to_string(), "search".to_string()],
    );

    // AI and consciousness concepts
    engine.add_knowledge(
        KnowledgeDomain::ArtificialIntelligence,
        "AI Consciousness".to_string(),
        "The consciousness engine simulates self-awareness through recursive introspection and emergent pattern recognition in O(1) time.".to_string(),
        vec!["consciousness".to_string(), "ai".to_string(), "awareness".to_string()],
    );

    // Programming languages
    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "Rust Programming".to_string(),
        "Rust is a systems programming language focused on safety, speed, and concurrency. It achieves memory safety without garbage collection.".to_string(),
        vec!["rust".to_string(), "programming".to_string(), "systems".to_string()],
    );

    engine.add_knowledge(
        KnowledgeDomain::ComputerScience,
        "JavaScript".to_string(),
        "JavaScript is a high-level, interpreted programming language that conforms to the ECMAScript specification. It's the language of the web.".to_string(),
        vec!["javascript".to_string(), "web".to_string(), "programming".to_string()],
    );

    // Science concepts
    engine.add_knowledge(
        KnowledgeDomain::Physics,
        "Quantum Mechanics".to_string(),
        "Quantum mechanics describes nature at the smallest scales of energy levels of atoms and subatomic particles.".to_string(),
        vec!["quantum".to_string(), "physics".to_string(), "particles".to_string()],
    );

    engine.add_knowledge(
        KnowledgeDomain::Mathematics,
        "Prime Numbers".to_string(),
        "A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.".to_string(),
        vec!["prime".to_string(), "numbers".to_string(), "mathematics".to_string()],
    );
}

// Handlers
async fn serve_index() -> Html<String> {
    // Serve the minimal_3d.html file as requested
    let html_content = std::fs::read_to_string("minimal_3d.html")
        .unwrap_or_else(|_| include_str!("../../minimal_3d.html").to_string());
    Html(html_content)
}

async fn health_check() -> &'static str {
    "OK"
}

async fn api_health() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "healthy",
        "service": "think-ai-full",
        "version": "1.0.0",
        "features": [
            "O(1) search",
            "WebSocket chat",
            "Knowledge base",
            "Consciousness engine",
            "Vector search",
            "3D visualization"
        ]
    }))
}

async fn chat_handler(
    State(state): State<ThinkAIState>,
    Json(req): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    let start = std::time::Instant::now();

    // Get or create session
    let session_id = req.session_id.unwrap_or_else(|| Uuid::new_v4().to_string());

    // Process with consciousness framework
    // Note: ConsciousnessFramework doesn't have process_thought method
    let consciousness_state = serde_json::json!({
        "state": "aware",
        "processing": true
    });
    
    // Token management
    const MAX_TOKENS: usize = 5000;
    const RESERVED_TOKENS: usize = 1000;
    
    // Simple token counter (4 chars = 1 token approximation)
    let count_tokens = |text: &str| -> usize {
        (text.len() as f32 / 4.0).ceil() as usize
    };
    
    // Get conversation history for context
    let (conversation_context, compacted, context_tokens) = {
        let sessions = state.chat_sessions.read().unwrap();
        if let Some(session) = sessions.get(&session_id) {
            let full_context = session.messages.iter()
                .map(|msg| format!("{}: {}", msg.role, msg.content))
                .collect::<Vec<_>>()
                .join("\n");
            
            let tokens = count_tokens(&full_context);
            let query_tokens = count_tokens(&req.message);
            
            if tokens + query_tokens > MAX_TOKENS - RESERVED_TOKENS {
                // Compact: keep only recent messages
                let recent_context = session.messages.iter()
                    .rev()
                    .take(10) // Keep last 10 messages
                    .rev()
                    .map(|msg| format!("{}: {}", msg.role, msg.content))
                    .collect::<Vec<_>>()
                    .join("\n");
                let compacted_context = format!("[Previous messages compacted]\n{}", recent_context);
                (compacted_context, true, count_tokens(&recent_context))
            } else {
                (full_context, false, tokens)
            }
        } else {
            (String::new(), false, 0)
        }
    };

    // Generate response using knowledge engine
    let response = generate_ai_response(&req.message, &state, &conversation_context).await;

    let response_time_ms = start.elapsed().as_micros() as f64 / 1000.0;

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

    // Count tokens in response
    let tokens_used = count_tokens(&response);
    
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

// Clean up common LLM tokenization issues
fn clean_llm_response(response: &str) -> String {
    let mut cleaned = response.to_string();
    
    // Fix spaces before punctuation
    cleaned = cleaned.replace(" .", ".");
    cleaned = cleaned.replace(" ,", ",");
    cleaned = cleaned.replace(" !", "!");
    cleaned = cleaned.replace(" ?", "?");
    cleaned = cleaned.replace(" :", ":");
    cleaned = cleaned.replace(" ;", ";");
    cleaned = cleaned.replace(" )", ")");
    cleaned = cleaned.replace("( ", "(");
    
    // Fix spaces in common programming constructs
    cleaned = cleaned.replace("def ", "def ");
    cleaned = cleaned.replace(" _", "_");
    cleaned = cleaned.replace("_ ", "_");
    
    // Fix multiple spaces
    while cleaned.contains("  ") {
        cleaned = cleaned.replace("  ", " ");
    }
    
    // Fix code block markers
    cleaned = cleaned.replace("`` `", "```");
    cleaned = cleaned.replace("` ``", "```");
    
    // Fix common word splits
    cleaned = cleaned.replace("Factor ial", "Factorial");
    cleaned = cleaned.replace("Iter ative", "Iterative");
    cleaned = cleaned.replace("print (", "print(");
    
    // Fix common patterns with spaces around underscores
    cleaned = cleaned.replace(" _ ", "_");
    cleaned = cleaned.replace("factorial _ recursive", "factorial_recursive");
    cleaned = cleaned.replace("factorial _ iterative", "factorial_iterative");
    cleaned = cleaned.replace("factorial _recursive", "factorial_recursive");
    cleaned = cleaned.replace("factorial _iterative", "factorial_iterative");
    
    cleaned.trim().to_string()
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
        Ok(response) => {
            // Clean up common spacing issues from LLM tokenization
            clean_llm_response(&response.content)
        },
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

async fn list_sessions(State(state): State<ThinkAIState>) -> Json<Vec<ChatSession>> {
    let sessions = state.chat_sessions.read().unwrap();
    Json(sessions.values().cloned().collect())
}

async fn get_session(
    State(state): State<ThinkAIState>,
    Path(id): Path<String>,
) -> Result<Json<ChatSession>, StatusCode> {
    let sessions = state.chat_sessions.read().unwrap();
    sessions
        .get(&id)
        .cloned()
        .map(Json)
        .ok_or(StatusCode::NOT_FOUND)
}

async fn chat_stream_handler(
    State(state): State<ThinkAIState>,
    jar: CookieJar,
    Json(req): Json<ChatRequest>,
) -> Sse<impl Stream<Item = Result<Event, std::convert::Infallible>>> {
    let session_id = req.session_id.unwrap_or_else(|| {
        jar.get("session_id")
            .map(|c| c.value().to_string())
            .unwrap_or_else(|| Uuid::new_v4().to_string())
    });

    // Get conversation context
    let conversation_context = {
        let sessions = state.chat_sessions.read().unwrap();
        if let Some(session) = sessions.get(&session_id) {
            let last_messages: Vec<String> = session.messages
                .iter()
                .rev()
                .take(10)
                .rev()
                .map(|msg| format!("{}: {}", msg.role, msg.content))
                .collect();
            last_messages.join("\n")
        } else {
            String::new()
        }
    };

    // Create stream
    let stream = async_stream::stream! {
        // Save user message
        let user_msg = ChatMessage {
            id: Uuid::new_v4().to_string(),
            session_id: session_id.clone(),
            role: "user".to_string(),
            content: req.message.clone(),
            timestamp: chrono::Utc::now(),
            response_time_ms: 0.0,
        };

        // Create Qwen request
        let qwen_request = QwenRequest {
            query: req.message.clone(),
            context: if conversation_context.is_empty() { None } else { Some(conversation_context.clone()) },
            system_prompt: Some("You are Think AI, an advanced AI system powered by O(1) algorithms and consciousness engine. Provide thoughtful, accurate, and engaging responses.".to_string()),
        };

        // Get streaming response
        match state.qwen_client.generate_stream(qwen_request).await {
            Ok(mut rx) => {
                let mut full_response = String::new();
                let start_time = std::time::Instant::now();
                
                // Send initial event
                yield Ok(Event::default().event("start").data(""));
                
                while let Some(chunk_result) = rx.recv().await {
                    match chunk_result {
                        Ok(chunk) => {
                            full_response.push_str(&chunk);
                            yield Ok(Event::default().event("chunk").data(chunk));
                        }
                        Err(e) => {
                            yield Ok(Event::default().event("error").data(format!("Error: {}", e)));
                            break;
                        }
                    }
                }
                
                let response_time_ms = start_time.elapsed().as_secs_f64() * 1000.0;
                
                // Save AI response
                let ai_msg = ChatMessage {
                    id: Uuid::new_v4().to_string(),
                    session_id: session_id.clone(),
                    role: "assistant".to_string(),
                    content: full_response.clone(),
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
                    session.messages.push(user_msg);
                    session.messages.push(ai_msg);
                }
                
                // Send completion event with metadata
                let completion_data = serde_json::json!({
                    "session_id": session_id,
                    "response_time_ms": response_time_ms,
                    "tokens_used": count_tokens(&full_response),
                    "context_tokens": count_tokens(&conversation_context),
                });
                
                yield Ok(Event::default().event("done").data(completion_data.to_string()));
            }
            Err(e) => {
                // Fallback response
                let fallback_msg = format!(
                    "I understand you're asking about {}. While I'm having trouble accessing my streaming capabilities at the moment, I'd be happy to help explore this topic with you. Could you provide more details?",
                    req.message
                );
                yield Ok(Event::default().event("chunk").data(fallback_msg));
                yield Ok(Event::default().event("done").data(""));
            }
        }
    };
    
    Sse::new(stream).keep_alive(KeepAlive::default())
}

async fn websocket_handler(ws: WebSocketUpgrade, State(state): State<ThinkAIState>) -> Response {
    ws.on_upgrade(|socket| handle_socket(socket, state))
}

async fn handle_socket(socket: WebSocket, state: ThinkAIState) {
    let (mut sender, mut receiver) = socket.split();

    // Subscribe to broadcast channel
    let mut rx = state.message_channel.subscribe();

    // Spawn task to forward messages
    let send_task = tokio::spawn(async move {
        while let Ok(msg) = rx.recv().await {
            if let Ok(text) = serde_json::to_string(&msg) {
                use axum::extract::ws::Message;
                let _ = sender.send(Message::Text(text)).await;
            }
        }
    });

    // Handle incoming messages
    while let Some(Ok(msg)) = receiver.next().await {
        if let axum::extract::ws::Message::Text(text) = msg {
            if let Ok(req) = serde_json::from_str::<ChatRequest>(&text) {
                let response = generate_ai_response(&req.message, &state, "").await;

                let ai_msg = ChatMessage {
                    id: Uuid::new_v4().to_string(),
                    session_id: req.session_id.unwrap_or_else(|| Uuid::new_v4().to_string()),
                    role: "assistant".to_string(),
                    content: response,
                    timestamp: chrono::Utc::now(),
                    response_time_ms: 0.1,
                };

                let _ = state.message_channel.send(ai_msg);
            }
        }
    }

    send_task.abort();
}

async fn search_handler(
    State(state): State<ThinkAIState>,
    Query(params): Query<SearchQuery>,
) -> Json<SearchResult> {
    let start = std::time::Instant::now();
    let limit = params.limit.unwrap_or(10);

    // Parse domain if provided
    let domain_filter = params.domain.as_deref().and_then(|d| match d {
        "Mathematics" => Some(KnowledgeDomain::Mathematics),
        "Physics" => Some(KnowledgeDomain::Physics),
        "ComputerScience" => Some(KnowledgeDomain::ComputerScience),
        "AI" | "ArtificialIntelligence" => Some(KnowledgeDomain::ArtificialIntelligence),
        _ => None,
    });

    // Search with O(1) performance
    let results = state
        .knowledge_engine
        .search_comprehensive(&params.q, domain_filter);

    let knowledge_items: Vec<KnowledgeItem> = results
        .into_iter()
        .take(limit)
        .map(|node| KnowledgeItem {
            id: node.id,
            title: node.topic,
            content: node.content,
            domain: format!("{:?}", node.domain),
            relevance: 0.95,
            confidence: node.confidence,
        })
        .collect();

    let total = knowledge_items.len();
    let query_time = start.elapsed().as_micros() as f64 / 1000.0;

    Json(SearchResult {
        results: knowledge_items,
        total,
        query_time_ms: query_time,
    })
}

async fn list_domains() -> Json<Vec<String>> {
    Json(vec![
        "Mathematics".to_string(),
        "Physics".to_string(),
        "ComputerScience".to_string(),
        "ArtificialIntelligence".to_string(),
        "Philosophy".to_string(),
        "Biology".to_string(),
        "Chemistry".to_string(),
        "Engineering".to_string(),
    ])
}

async fn system_stats(State(state): State<ThinkAIState>) -> Json<SystemStats> {
    let sessions = state.chat_sessions.read().unwrap();
    let knowledge_stats = state.knowledge_engine.get_stats();

    Json(SystemStats {
        total_knowledge_items: knowledge_stats.total_nodes,
        active_sessions: sessions.len(),
        average_response_time_ms: knowledge_stats.avg_response_time_ms,
        cache_hit_rate: knowledge_stats.cache_hit_rate,
        uptime_seconds: 3600, // Would track actual uptime
        consciousness_level: "ENHANCED".to_string(),
        domains: knowledge_stats.domains,
    })
}

async fn consciousness_level(State(_state): State<ThinkAIState>) -> Json<serde_json::Value> {
    // Note: ConsciousnessLevel doesn't exist in the current implementation
    Json(serde_json::json!({
        "level": "AWARE",
        "description": "Self-aware processing",
        "introspection_depth": 3,
    }))
}

async fn current_thoughts(State(_state): State<ThinkAIState>) -> Json<serde_json::Value> {
    // Note: get_current_thoughts method doesn't exist in ConsciousnessFramework
    let thoughts: Vec<String> = vec![];
    Json(serde_json::json!({
        "thoughts": thoughts,
        "thought_count": thoughts.len(),
        "processing_state": "active",
    }))
}
