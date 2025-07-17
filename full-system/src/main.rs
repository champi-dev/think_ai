use axum::{
    extract::{ws::WebSocket, Path, Query, State, WebSocketUpgrade},
    http::{header, HeaderMap, StatusCode},
    response::{
        sse::{Event, KeepAlive},
        IntoResponse, Response, Sse,
    },
    routing::{get, post},
    Json, Router,
};
use axum_extra::extract::CookieJar;
use futures_util::{stream::Stream, SinkExt, StreamExt};
use serde::{Deserialize, Serialize};
use serde_json::json;
use std::{
    collections::HashMap,
    env,
    sync::{Arc, RwLock},
};
use tokio::sync::broadcast;
use tower_http::{
    cors::{Any, CorsLayer},
    services::{ServeDir, ServeFile},
    trace::TraceLayer,
};
use tracing::info;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use uuid::Uuid;

mod audio_service;
mod geolocation;

// Import actual Think AI components
use think_ai_consciousness::ConsciousnessFramework;
use think_ai_core::{EngineConfig, O1Engine};
use think_ai_knowledge::{KnowledgeDomain, KnowledgeEngine};
use think_ai_qwen::{QwenClient, QwenRequest};
use think_ai_utils::token_counter::count_tokens;
use think_ai_vector::{LSHConfig, O1VectorIndex};

use crate::audio_service::{AudioService, SynthesisRequest, TranscriptionResult};
use bytes::Bytes;

// State for the application
#[derive(Clone)]
struct ThinkAIState {
    _core_engine: Arc<O1Engine>,
    knowledge_engine: Arc<KnowledgeEngine>,
    _vector_index: Arc<O1VectorIndex>,
    _consciousness_framework: Arc<ConsciousnessFramework>,
    chat_sessions: Arc<RwLock<HashMap<String, ChatSession>>>,
    message_channel: broadcast::Sender<ChatMessage>,
    qwen_client: Arc<QwenClient>,
    audio_service: Option<Arc<AudioService>>,
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
    mode: Option<String>,
    use_web_search: Option<bool>,
    fact_check: Option<bool>,
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

    // Initialize audio service if API keys are available
    let audio_service = match (env::var("DEEPGRAM_API_KEY"), env::var("ELEVENLABS_API_KEY")) {
        (Ok(deepgram_key), Ok(elevenlabs_key)) => {
            let audio_cache_dir =
                env::var("AUDIO_CACHE_DIR").unwrap_or_else(|_| "./audio_cache".to_string());
            let service = AudioService::new(
                deepgram_key,
                elevenlabs_key,
                std::path::PathBuf::from(audio_cache_dir),
            );
            if let Err(e) = service.init().await {
                eprintln!("Failed to initialize audio service: {}", e);
                None
            } else {
                info!("✅ Audio service initialized successfully");
                Some(Arc::new(service))
            }
        }
        _ => {
            info!("⚠️ Audio service disabled - API keys not found");
            None
        }
    };

    // Initialize state
    let (tx, _rx) = broadcast::channel(100);
    let state = ThinkAIState {
        _core_engine: core_engine,
        knowledge_engine,
        _vector_index: vector_index,
        _consciousness_framework: consciousness_framework,
        chat_sessions: Arc::new(RwLock::new(HashMap::new())),
        message_channel: tx,
        qwen_client,
        audio_service,
    };

    // Build router
    let app = Router::new()
        // API routes
        .route("/api/health", get(api_health))
        .route("/api/chat", post(chat_handler))
        .route("/api/chat/stream", post(chat_stream_handler))
        .route("/api/chat/sessions", get(list_sessions))
        .route("/api/chat/sessions/:id", get(get_session))
        .route("/ws/chat", get(websocket_handler))
        .route("/api/search", get(search_handler))
        .route("/api/knowledge/domains", get(list_domains))
        .route("/api/knowledge/stats", get(system_stats))
        .route("/api/consciousness/level", get(consciousness_level))
        .route("/api/consciousness/thoughts", get(current_thoughts))
        // Audio endpoints
        .route("/api/audio/transcribe", post(transcribe_audio))
        .route("/api/audio/synthesize", post(synthesize_speech))
        // Geolocation endpoint
        .route("/api/detect-language", get(detect_language_from_ip))
        // Health check for the main service
        .route("/health", get(health_check))
        // Static file serving for the frontend
        .nest_service(
            "/",
            ServeDir::new("frontend/dist").fallback(ServeFile::new("frontend/dist/index.html")),
        )
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
}

// Handlers
async fn health_check() -> &'static str {
    "OK"
}

async fn api_health() -> Json<serde_json::Value> {
    Json(serde_json::json!({
        "status": "healthy",
        "service": "think-ai-full",
        "version": "1.0.0",
    }))
}

// Detect language from IP
async fn detect_language_from_ip(headers: HeaderMap) -> Result<Json<serde_json::Value>, StatusCode> {
    // Try to get the real IP from various headers
    let ip = headers
        .get("x-forwarded-for")
        .and_then(|v| v.to_str().ok())
        .and_then(|s| s.split(',').next()) // Take first IP if multiple
        .or_else(|| {
            headers
                .get("x-real-ip")
                .and_then(|v| v.to_str().ok())
        })
        .unwrap_or("127.0.0.1");
    
    match geolocation::get_geolocation_info(ip).await {
        Ok(info) => Ok(Json(json!({
            "language": info.language,
            "country_code": info.country_code,
            "country_name": info.country_name,
            "city": info.city,
            "detected_from_ip": ip
        }))),
        Err(_) => Ok(Json(json!({
            "language": "en",
            "country_code": "US",
            "country_name": "United States",
            "detected_from_ip": ip,
            "fallback": true
        }))),
    }
}

#[axum::debug_handler]
async fn chat_handler(
    State(state): State<ThinkAIState>,
    Json(req): Json<ChatRequest>,
) -> Json<ChatResponse> {
    let start = std::time::Instant::now();

    // Get or create session
    let session_id = req.session_id.unwrap_or_else(|| Uuid::new_v4().to_string());

    // Get session history and add user message
    let (mut context, user_message) = {
        let mut sessions = state.chat_sessions.write().unwrap();
        let session = sessions
            .entry(session_id.clone())
            .or_insert_with(|| ChatSession {
                id: session_id.clone(),
                messages: Vec::new(),
                created_at: chrono::Utc::now(),
            });

        // Add user message to session
        let user_message = ChatMessage {
            id: Uuid::new_v4().to_string(),
            session_id: session_id.clone(),
            role: "user".to_string(),
            content: req.message.clone(),
            timestamp: chrono::Utc::now(),
            response_time_ms: 0.0,
        };
        session.messages.push(user_message.clone());

        // Build context from session history
        let mut context = String::new();
        for msg in session.messages.iter().rev().take(10) {
            context.push_str(&format!("{}: {}\n", msg.role, msg.content));
        }

        (context, user_message)
    }; // RwLock guard is dropped here

    // Get relevant knowledge for context
    let knowledge_results = state
        .knowledge_engine
        .query(&req.message)
        .unwrap_or_else(Vec::new);
    let knowledge_context = knowledge_results
        .iter()
        .take(2)
        .map(|node| format!("{}: {}", node.topic, node.content))
        .collect::<Vec<_>>()
        .join("\n\n");

    // Generate response using Qwen
    let qwen_request = QwenRequest {
        query: req.message.clone(),
        context: Some(format!("Session Context:\n{}\n\nRelevant Knowledge:\n{}", context, knowledge_context)),
        system_prompt: Some("You are Think AI, a helpful quantum-powered AI assistant. Provide thoughtful, accurate responses based on the context and knowledge provided.".to_string()),
    };

    let ai_response = match state.qwen_client.generate(qwen_request).await {
        Ok(response) => response.content,
        Err(e) => {
            eprintln!("Qwen error: {:?}", e);
            // Fallback to knowledge engine response
            if !knowledge_results.is_empty() {
                format!("I'm having trouble connecting to my AI model. However, based on my knowledge about {}: {}", 
                    knowledge_results[0].topic,
                    knowledge_results[0].content
                )
            } else {
                "I apologize, but I'm unable to process your request at the moment. Please try again later.".to_string()
            }
        }
    };

    let response_time_ms = start.elapsed().as_micros() as f64 / 1000.0;

    // Add AI response to session
    {
        let mut sessions = state.chat_sessions.write().unwrap();
        if let Some(session) = sessions.get_mut(&session_id) {
            let ai_message = ChatMessage {
                id: Uuid::new_v4().to_string(),
                session_id: session_id.clone(),
                role: "assistant".to_string(),
                content: ai_response.clone(),
                timestamp: chrono::Utc::now(),
                response_time_ms,
            };
            session.messages.push(ai_message);
        }
    }

    // Calculate tokens (approximate)
    let tokens_used = count_tokens(&ai_response);
    let context_tokens = count_tokens(&context);

    Json(ChatResponse {
        response: ai_response,
        session_id,
        confidence: 0.95,
        response_time_ms,
        consciousness_level: "aware".to_string(),
        tokens_used,
        context_tokens,
        compacted: false,
    })
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

    let state_clone = state.clone();
    let message = req.message.clone();

    let stream = async_stream::stream! {
        yield Ok(Event::default().event("start").data(""));

        // Get relevant knowledge for context
        let knowledge_results = state_clone.knowledge_engine.query(&message)
            .unwrap_or_else(Vec::new);
        let knowledge_context = knowledge_results.iter()
            .take(2)
            .map(|node| format!("{}: {}", node.topic, node.content))
            .collect::<Vec<_>>()
            .join("\n\n");

        // Generate response using Qwen with streaming
        let qwen_request = QwenRequest {
            query: message,
            context: Some(format!("Relevant Knowledge:\n{}", knowledge_context)),
            system_prompt: Some("You are Think AI, a helpful quantum-powered AI assistant. Provide thoughtful, accurate responses based on the context and knowledge provided.".to_string()),
        };

        match state_clone.qwen_client.generate(qwen_request).await {
            Ok(response) => {
                // Simulate streaming by sending response in chunks
                let words: Vec<&str> = response.content.split_whitespace().collect();
                let chunk_size = 3;

                for chunk in words.chunks(chunk_size) {
                    let chunk_text = chunk.join(" ") + " ";
                    yield Ok(Event::default().data(json!({
                        "chunk": chunk_text,
                        "done": false
                    }).to_string()));
                    tokio::time::sleep(tokio::time::Duration::from_millis(50)).await;
                }

                yield Ok(Event::default().data(json!({
                    "chunk": "",
                    "done": true,
                    "session_id": session_id
                }).to_string()));
            }
            Err(e) => {
                let fallback = format!("I'm having trouble with streaming. Error: {}", e);
                yield Ok(Event::default().data(json!({
                    "chunk": fallback,
                    "done": true,
                    "session_id": session_id
                }).to_string()));
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
    while let Some(Ok(msg)) = receiver.next().await {
        if sender.send(msg).await.is_err() {
            break;
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

async fn search_handler(
    State(state): State<ThinkAIState>,
    Query(params): Query<SearchQuery>,
) -> Json<SearchResult> {
    let results = vec![];
    Json(SearchResult {
        results,
        total: 0,
        query_time_ms: 0.0,
    })
}

async fn list_domains() -> Json<Vec<String>> {
    Json(vec![])
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
    Json(serde_json::json!({
        "level": "AWARE",
        "description": "Self-aware processing",
        "introspection_depth": 3,
    }))
}

async fn current_thoughts(State(_state): State<ThinkAIState>) -> Json<serde_json::Value> {
    let thoughts: Vec<String> = vec![];
    Json(serde_json::json!({
        "thoughts": thoughts,
        "thought_count": thoughts.len(),
        "processing_state": "active",
    }))
}

// Audio transcription handler
async fn transcribe_audio(
    State(state): State<ThinkAIState>,
    headers: HeaderMap,
    body: Bytes,
) -> Result<Json<TranscriptionResult>, StatusCode> {
    let audio_service = state
        .audio_service
        .as_ref()
        .ok_or(StatusCode::SERVICE_UNAVAILABLE)?;

    let content_type = headers
        .get(header::CONTENT_TYPE)
        .and_then(|v| v.to_str().ok())
        .unwrap_or("audio/webm");
        
    // Get language from custom header
    let language = headers
        .get("X-Language")
        .and_then(|v| v.to_str().ok())
        .map(|s| s.to_string());

    match audio_service.transcribe(body, content_type, language).await {
        Ok(result) => Ok(Json(result)),
        Err(e) => {
            eprintln!("Transcription error: {}", e);
            Err(StatusCode::INTERNAL_SERVER_ERROR)
        }
    }
}

// Speech synthesis handler
async fn synthesize_speech(
    State(state): State<ThinkAIState>,
    Json(request): Json<SynthesisRequest>,
) -> Result<impl IntoResponse, StatusCode> {
    let audio_service = state
        .audio_service
        .as_ref()
        .ok_or(StatusCode::SERVICE_UNAVAILABLE)?;

    match audio_service.synthesize(request).await {
        Ok((audio_data, _cache_key)) => Ok(([(header::CONTENT_TYPE, "audio/mpeg")], audio_data)),
        Err(e) => {
            eprintln!("Synthesis error: {}", e);
            Err(StatusCode::INTERNAL_SERVER_ERROR)
        }
    }
}
