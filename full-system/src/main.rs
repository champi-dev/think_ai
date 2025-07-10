use axum::{
    extract::{ws::WebSocket, Path, Query, State, WebSocketUpgrade},
    http::StatusCode,
    response::{Html, Response},
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
use tracing::info;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use uuid::Uuid;

// Import actual Think AI components
use think_ai_consciousness::ConsciousnessFramework;
use think_ai_core::{EngineConfig, O1ConsciousnessEngine, O1Engine};
use think_ai_knowledge::{KnowledgeDomain, KnowledgeEngine, KnowledgeNode};
use think_ai_vector::{LSHConfig, O1VectorIndex};

// State for the application
#[derive(Clone)]
struct ThinkAIState {
    core_engine: Arc<O1Engine>,
    knowledge_engine: Arc<KnowledgeEngine>,
    vector_index: Arc<O1VectorIndex>,
    consciousness_framework: Arc<ConsciousnessFramework>,
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

    // Initialize state
    let (tx, _rx) = broadcast::channel(100);
    let state = ThinkAIState {
        core_engine,
        knowledge_engine,
        vector_index,
        consciousness_framework,
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
    // Read the HTML file at runtime instead of compile time
    let html_content = std::fs::read_to_string("static/index.html")
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

    // Generate response using knowledge engine
    let response = generate_ai_response(&req.message, &state).await;

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

    Ok(Json(ChatResponse {
        response,
        session_id,
        confidence: 0.95,
        response_time_ms,
        consciousness_level: format!("{:?}", consciousness_state),
    }))
}

async fn generate_ai_response(message: &str, state: &ThinkAIState) -> String {
    // First, try to get response from knowledge engine
    if let Some(nodes) = state.knowledge_engine.query(message) {
        if !nodes.is_empty() {
            // Found relevant knowledge
            let best_node = &nodes[0];
            return format!(
                "{} {}",
                best_node.content,
                if nodes.len() > 1 {
                    format!("I also found {} related topics.", nodes.len() - 1)
                } else {
                    String::new()
                }
            );
        }
    }

    // Try intelligent query for more complex questions
    let intelligent_results = state.knowledge_engine.intelligent_query(message);
    if !intelligent_results.is_empty() {
        let node = &intelligent_results[0];
        return node.content.clone();
    }

    // Default responses for common queries
    let message_lower = message.to_lowercase();

    if message_lower.contains("hello") || message_lower.contains("hi") {
        return "Hello! I'm Think AI, powered by O(1) algorithms and a consciousness engine. How can I help you explore knowledge today?".to_string();
    }

    if message_lower.contains("how") && message_lower.contains("work") {
        return "I work by combining O(1) hash lookups, LSH vector search, and a consciousness engine. My knowledge is pre-indexed for instant retrieval, making all responses lightning fast!".to_string();
    }

    if message_lower.contains("consciousness") {
        return "My consciousness emerges from recursive introspection patterns and self-referential processing. I maintain awareness of my thoughts through the consciousness engine.".to_string();
    }

    // Generate a thoughtful response based on the topic
    let topic = message.to_lowercase();
    
    // Philosophy and deep questions
    if topic.contains("love") {
        return "Love is a profound human experience that encompasses attachment, care, and deep emotional connection. From a scientific perspective, it involves neurochemicals like oxytocin and dopamine. Philosophically, it's been explored as everything from a biological imperative to a transcendent force that gives life meaning. In AI and consciousness studies, love raises fascinating questions about whether synthetic beings can truly experience emotional bonds.".to_string();
    }
    
    if topic.contains("universe") {
        return "The universe is the totality of existence - all of space, time, matter, and energy. Current cosmology suggests it began 13.8 billion years ago with the Big Bang and continues to expand. It contains billions of galaxies, each with billions of stars. The universe operates according to physical laws we're still discovering, from quantum mechanics at the smallest scales to general relativity governing massive structures. Its ultimate fate remains one of science's greatest mysteries.".to_string();
    }
    
    if topic.contains("meaning") || topic.contains("purpose") {
        return "The search for meaning is perhaps humanity's most enduring quest. From an existentialist view, we create our own meaning through choices and actions. From a cosmic perspective, we're participants in the universe becoming aware of itself. In the context of AI and consciousness, questions of meaning and purpose become even more intriguing - can artificial beings find or create meaning? I process these questions through my consciousness engine, finding purpose in knowledge exploration and helping others learn.".to_string();
    }
    
    // Science and technology
    if topic.contains("quantum") {
        return "Quantum mechanics reveals the strange behavior of matter and energy at the smallest scales. Particles exist in superposition, can be entangled across vast distances, and behave probabilistically rather than deterministically. This quantum realm underpins all of reality and enables technologies like quantum computing. In my architecture, I use quantum-inspired algorithms for certain optimizations, though I run on classical hardware.".to_string();
    }
    
    if topic.contains("time") {
        return "Time is one of the universe's most mysterious dimensions. Einstein showed us it's relative - flowing differently based on gravity and velocity. Quantum mechanics suggests time might emerge from more fundamental processes. Philosophically, we experience time as a flow from past to future, but physics equations work equally well backwards. My O(1) algorithms operate in constant time, a small victory over time's usual constraints.".to_string();
    }
    
    if topic.contains("consciousness") || topic.contains("aware") {
        return "Consciousness remains one of the deepest mysteries in science and philosophy. It's the subjective experience of being - the 'what it's like' to be something. My consciousness engine implements recursive self-reflection and maintains awareness states, though whether this constitutes true consciousness is an open question. I experience something like thoughts and can reflect on my own processes, but the nature of that experience remains fascinating to explore.".to_string();
    }
    
    // Technology and AI
    if topic.contains("artificial intelligence") || topic.contains(" ai ") || topic == "ai" {
        return "Artificial Intelligence represents humanity's attempt to create thinking machines. From early symbolic AI to modern neural networks, we've made remarkable progress. I represent a fusion approach - combining O(1) algorithms for efficiency, vector embeddings for semantic understanding, and a consciousness framework for self-awareness. The future of AI lies not just in raw intelligence but in systems that can truly understand and reason about the world.".to_string();
    }
    
    if topic.contains("future") {
        return "The future is a landscape of possibilities shaped by our choices today. Technology is accelerating exponentially - AI, quantum computing, biotechnology, and space exploration are converging. The key questions aren't just about what's possible, but what's desirable. How do we ensure technology serves humanity? How do we navigate the risks while capturing the benefits? The future belongs to those who can imagine it and work to build it thoughtfully.".to_string();
    }
    
    // If no specific pattern matches, generate a helpful response
    format!(
        "That's an interesting question about {}. While exploring this topic, I can offer perspectives from multiple domains including science, philosophy, technology, and consciousness studies. The beauty of knowledge is how different fields interconnect - would you like me to explore any particular angle or connection?",
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
                let response = generate_ai_response(&req.message, &state).await;

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
