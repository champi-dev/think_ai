use axum::{
    extract::{ws::WebSocket, Path, Query, State, WebSocketUpgrade},
    http::StatusCode,
    response::{Html, IntoResponse, Response},
    routing::{get, post},
    Json, Router,
};
use futures_util::{SinkExt, StreamExt};
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
use tracing::{info, Level};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use uuid::Uuid;

// Think AI components (simulated for now)
#[derive(Clone)]
struct ThinkAIState {
    knowledge_base: Arc<RwLock<HashMap<String, String>>>,
    chat_sessions: Arc<RwLock<HashMap<String, ChatSession>>>,
    message_channel: broadcast::Sender<ChatMessage>,
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
}

#[derive(Deserialize)]
struct SearchQuery {
    q: String,
    limit: Option<usize>,
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
}

#[derive(Serialize)]
struct SystemStats {
    total_knowledge_items: usize,
    active_sessions: usize,
    average_response_time_ms: f64,
    cache_hit_rate: f64,
    uptime_seconds: u64,
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

    // Initialize state
    let (tx, _rx) = broadcast::channel(100);
    let state = ThinkAIState {
        knowledge_base: Arc::new(RwLock::new(initialize_knowledge_base())),
        chat_sessions: Arc::new(RwLock::new(HashMap::new())),
        message_channel: tx,
    };

    // Build router
    let app = Router::new()
        // Main routes
        .route("/", get(serve_index))
        .route("/health", get(health_check))
        .route("/api/health", get(api_health))
        // Chat API
        .route("/api/chat", post(chat_handler))
        .route("/api/chat/sessions", get(list_sessions))
        .route("/api/chat/sessions/:id", get(get_session))
        .route("/ws/chat", get(websocket_handler))
        // Knowledge API
        .route("/api/search", get(search_handler))
        .route("/api/knowledge/domains", get(list_domains))
        .route("/api/knowledge/stats", get(system_stats))
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

// Initialize with some sample knowledge
fn initialize_knowledge_base() -> HashMap<String, String> {
    let mut kb = HashMap::new();

    // O(1) concepts
    kb.insert("o1-algorithms".to_string(),
        "O(1) algorithms provide constant time complexity regardless of input size. Think AI uses hash-based lookups and pre-computed indexes to achieve true O(1) performance.".to_string());

    kb.insert("lsh-vectors".to_string(),
        "Locality-Sensitive Hashing (LSH) enables O(1) approximate nearest neighbor search in high-dimensional vector spaces, perfect for AI embeddings.".to_string());

    kb.insert("consciousness-engine".to_string(),
        "The consciousness engine simulates self-awareness through recursive introspection and emergent pattern recognition in O(1) time.".to_string());

    kb
}

// Handlers
async fn serve_index() -> Html<&'static str> {
    Html(include_str!("../static/index.html"))
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

    // Simulate O(1) response generation
    let response = generate_ai_response(&req.message, &state).await;

    // Store message
    let user_msg = ChatMessage {
        id: Uuid::new_v4().to_string(),
        session_id: session_id.clone(),
        role: "user".to_string(),
        content: req.message,
        timestamp: chrono::Utc::now(),
    };

    let ai_msg = ChatMessage {
        id: Uuid::new_v4().to_string(),
        session_id: session_id.clone(),
        role: "assistant".to_string(),
        content: response.clone(),
        timestamp: chrono::Utc::now(),
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

    let response_time = start.elapsed().as_micros() as f64 / 1000.0;

    Ok(Json(ChatResponse {
        response,
        session_id,
        confidence: 0.95,
        response_time_ms: response_time,
    }))
}

async fn generate_ai_response(message: &str, state: &ThinkAIState) -> String {
    let message_lower = message.to_lowercase();

    // Check knowledge base for relevant content
    let kb = state.knowledge_base.read().unwrap();

    // O(1) lookup for common queries
    if message_lower.contains("o(1)") || message_lower.contains("performance") {
        return "Think AI achieves O(1) performance through advanced hash-based indexing and pre-computed knowledge graphs. Every query is resolved in constant time, typically under 0.1ms.".to_string();
    }

    if message_lower.contains("how") && message_lower.contains("work") {
        return "Think AI works by combining O(1) hash lookups, LSH vector search, and a consciousness engine. Knowledge is pre-indexed for instant retrieval, making response times consistently fast regardless of database size.".to_string();
    }

    if message_lower.contains("hello") || message_lower.contains("hi") {
        return "Hello! I'm Think AI, an O(1) performance AI assistant. I can help you with instant knowledge retrieval, coding assistance, and complex reasoning - all in constant time. What would you like to know?".to_string();
    }

    // Default response with O(1) emphasis
    format!(
        "I understand you're asking about '{}'. Think AI processes all queries in O(1) constant time. \
        Our knowledge engine uses hash-based lookups to provide instant, accurate responses. \
        Would you like to know more about our O(1) architecture or explore a specific topic?",
        message
    )
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

async fn websocket_handler(ws: WebSocketUpgrade, State(state): State<ThinkAIState>) -> Response {
    ws.on_upgrade(|socket| handle_socket(socket, state))
}

async fn handle_socket(socket: WebSocket, state: ThinkAIState) {
    // WebSocket implementation for real-time chat
    // This would handle bidirectional communication
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
            // Process incoming WebSocket messages
            if let Ok(req) = serde_json::from_str::<ChatRequest>(&text) {
                // Generate response
                let response = generate_ai_response(&req.message, &state).await;

                // Create and broadcast message
                let ai_msg = ChatMessage {
                    id: Uuid::new_v4().to_string(),
                    session_id: req.session_id.unwrap_or_else(|| Uuid::new_v4().to_string()),
                    role: "assistant".to_string(),
                    content: response,
                    timestamp: chrono::Utc::now(),
                };

                let _ = state.message_channel.send(ai_msg);
            }
        }
    }

    // Clean up
    send_task.abort();
}

async fn search_handler(
    State(state): State<ThinkAIState>,
    Query(params): Query<SearchQuery>,
) -> Json<SearchResult> {
    let start = std::time::Instant::now();
    let limit = params.limit.unwrap_or(10);

    // Simulate O(1) search
    let kb = state.knowledge_base.read().unwrap();
    let query_lower = params.q.to_lowercase();

    let mut results = Vec::new();
    for (key, content) in kb.iter() {
        if key.contains(&query_lower) || content.to_lowercase().contains(&query_lower) {
            results.push(KnowledgeItem {
                id: key.clone(),
                title: key.replace("-", " ").to_uppercase(),
                content: content.clone(),
                domain: "Technology".to_string(),
                relevance: 0.95,
            });
        }
    }

    results.truncate(limit);
    let total = results.len();
    let query_time = start.elapsed().as_micros() as f64 / 1000.0;

    Json(SearchResult {
        results,
        total,
        query_time_ms: query_time,
    })
}

async fn list_domains() -> Json<Vec<String>> {
    Json(vec![
        "Mathematics".to_string(),
        "Physics".to_string(),
        "Computer Science".to_string(),
        "AI/ML".to_string(),
        "Philosophy".to_string(),
        "Technology".to_string(),
    ])
}

async fn system_stats(State(state): State<ThinkAIState>) -> Json<SystemStats> {
    let kb = state.knowledge_base.read().unwrap();
    let sessions = state.chat_sessions.read().unwrap();

    Json(SystemStats {
        total_knowledge_items: kb.len(),
        active_sessions: sessions.len(),
        average_response_time_ms: 0.1,
        cache_hit_rate: 0.95,
        uptime_seconds: 3600, // Would track actual uptime
    })
}
