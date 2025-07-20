use axum::{
    extract::{Json, State, Path, Query},
    http::{header, HeaderMap, StatusCode},
    middleware,
    response::IntoResponse,
    routing::{get, post},
    Router,
};
use serde::{Deserialize, Serialize};
use std::{env, sync::Arc};
use tokio::sync::broadcast;
use tower::ServiceBuilder;
use tower_http::{
    trace::TraceLayer,
};
use tracing::info;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
use uuid::Uuid;

mod audio_service;
mod security;

use crate::security::{
    auth::AuthMiddleware,
    SecurityConfig,
    security_middleware,
};

// Import Think AI components
use think_ai_consciousness::ConsciousnessFramework;
use think_ai_core::{EngineConfig, O1Engine};
use think_ai_knowledge::KnowledgeEngine;
use think_ai_qwen::{QwenClient, QwenRequest};
use think_ai_storage::PersistentConversationMemory;
use think_ai_vector::{LSHConfig, O1VectorIndex};

use crate::audio_service::{AudioService, SynthesisRequest, TranscriptionResult};

#[derive(Clone)]
struct ThinkAIState {
    _core_engine: Arc<O1Engine>,
    knowledge_engine: Arc<KnowledgeEngine>,
    _vector_index: Arc<O1VectorIndex>,
    _consciousness_framework: Arc<ConsciousnessFramework>,
    persistent_memory: Arc<PersistentConversationMemory>,
    message_channel: broadcast::Sender<ChatMessage>,
    qwen_client: Arc<QwenClient>,
    audio_service: Option<Arc<AudioService>>,
    security_config: Arc<SecurityConfig>,
}

#[derive(Clone, Serialize, Deserialize)]
struct ChatMessage {
    id: String,
    session_id: String,
    message: String,
    response: Option<String>,
    timestamp: u64,
}

#[derive(Deserialize)]
struct ChatRequest {
    session_id: String,
    message: String,
}

#[derive(Serialize)]
struct ChatResponse {
    id: String,
    response: String,
    thinking_process: Option<Vec<String>>,
}

#[derive(Deserialize)]
struct LoginRequest {
    username: String,
    password: String,
}

#[derive(Serialize)]
struct LoginResponse {
    token: String,
    expires_in: u64,
}

#[tokio::main]
async fn main() {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "think_ai_full=info,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    info!("Initializing Secure Think AI Server...");

    // Security configuration
    let secret_key = env::var("JWT_SECRET").unwrap_or_else(|_| "change-this-secret-key-in-production".to_string());
    let security_config = Arc::new(SecurityConfig::new(&secret_key));

    // Initialize components
    let engine_config = EngineConfig::default();
    let core_engine = Arc::new(O1Engine::new(engine_config));
    
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    let lsh_config = LSHConfig::default();
    let vector_index = Arc::new(O1VectorIndex::new(lsh_config));
    
    let consciousness_framework = Arc::new(ConsciousnessFramework::new());
    
    let persistent_memory = Arc::new(
        PersistentConversationMemory::new("./think_ai_sessions.db")
            .await
            .expect("Failed to initialize persistent memory"),
    );

    let (tx, _rx) = broadcast::channel(100);

    let qwen_client = Arc::new(QwenClient::new(env::var("GEMINI_API_KEY").ok()));

    let audio_service = if env::var("ENABLE_AUDIO").unwrap_or_default() == "true" {
        Some(Arc::new(AudioService::new(
            env::var("DEEPGRAM_API_KEY").ok(),
            env::var("ELEVEN_LABS_API_KEY").ok(),
        )))
    } else {
        None
    };

    let state = ThinkAIState {
        _core_engine: core_engine,
        knowledge_engine,
        _vector_index: vector_index,
        _consciousness_framework: consciousness_framework,
        persistent_memory,
        message_channel: tx,
        qwen_client,
        audio_service,
        security_config: security_config.clone(),
    };

    // Build the application with security layers
    let app = Router::new()
        // Public routes
        .route("/health", get(health_check))
        .route("/api/auth/login", post(login))
        
        // Protected API routes
        .nest("/api", protected_routes()
            .route_layer(middleware::from_fn_with_state(
                security_config.clone(),
                |req, next| AuthMiddleware::verify(req, next)
            ))
        )
        .layer(middleware::from_fn_with_state(
            security_config.clone(),
            security_middleware,
        ))
        
        // Static file serving
        .nest_service("/", tower_http::services::ServeDir::new("static"))
        
        // Global middleware
        .layer(
            ServiceBuilder::new()
                .layer(TraceLayer::new_for_http())
                .layer(SecurityConfig::cors_layer())
        )
        .with_state(state);

    let addr = format!("0.0.0.0:{}", env::var("PORT").unwrap_or_else(|_| "7777".to_string()));
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();
    
    info!("Secure Think AI server listening on {}", addr);
    
    axum::serve(listener, app).await.unwrap();
}

fn protected_routes() -> Router<ThinkAIState> {
    Router::new()
        .route("/chat", post(chat_handler))
        .route("/sessions", get(get_sessions))
        .route("/sessions/:id", get(get_session))
        .route("/audio/transcribe", post(transcribe_audio))
        .route("/audio/synthesize", post(synthesize_speech))
}

async fn health_check() -> impl IntoResponse {
    Json(serde_json::json!({
        "status": "healthy",
        "version": "1.0.0",
        "secure": true
    }))
}

async fn login(
    State(state): State<ThinkAIState>,
    Json(payload): Json<LoginRequest>,
) -> Result<Json<LoginResponse>, StatusCode> {
    // In production, verify against database
    if payload.username == "admin" && payload.password == "secure_password" {
        let token = state.security_config.auth_config
            .create_token(&payload.username, vec!["admin".to_string()])
            .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
            
        Ok(Json(LoginResponse {
            token,
            expires_in: 86400, // 24 hours
        }))
    } else {
        Err(StatusCode::UNAUTHORIZED)
    }
}

async fn chat_handler(
    State(state): State<ThinkAIState>,
    Json(payload): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    // Validate input
    let validator = &state.security_config.validator;
    if validator.check_sql_injection(&payload.message) || validator.check_xss(&payload.message) {
        return Err(StatusCode::BAD_REQUEST);
    }

    let message_id = Uuid::new_v4().to_string();
    
    // Rate limiting check
    state.security_config.rate_limiter
        .check_rate_limit(&payload.session_id)
        .await
        .map_err(|_| StatusCode::TOO_MANY_REQUESTS)?;
    
    // Process with Think AI
    let thinking_process = state.knowledge_engine
        .explore_concept(&payload.message)
        .await;
    
    let qwen_request = QwenRequest {
        model: "gemini-1.5-flash".to_string(),
        prompt: format!(
            "You are Think AI, an advanced consciousness framework. \
            Respond to: {}\n\nContext: {:?}",
            payload.message, thinking_process
        ),
        max_tokens: Some(1000),
        temperature: Some(0.7),
        stream: Some(false),
    };
    
    let response = state.qwen_client
        .complete(&qwen_request)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    // Store conversation
    let chat_message = ChatMessage {
        id: message_id.clone(),
        session_id: payload.session_id.clone(),
        message: payload.message,
        response: Some(response.clone()),
        timestamp: chrono::Utc::now().timestamp() as u64,
    };
    
    state.persistent_memory
        .add_interaction(&payload.session_id, &chat_message.message, &response)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    let _ = state.message_channel.send(chat_message);
    
    Ok(Json(ChatResponse {
        id: message_id,
        response,
        thinking_process: Some(thinking_process),
    }))
}

async fn get_sessions(
    State(state): State<ThinkAIState>,
) -> Result<Json<Vec<String>>, StatusCode> {
    let sessions = state.persistent_memory
        .list_sessions()
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    Ok(Json(sessions))
}

async fn get_session(
    State(state): State<ThinkAIState>,
    Path(session_id): Path<String>,
) -> Result<impl IntoResponse, StatusCode> {
    let history = state.persistent_memory
        .get_conversation(&session_id)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    Ok(Json(history))
}

async fn transcribe_audio(
    State(state): State<ThinkAIState>,
    body: Bytes,
) -> Result<Json<TranscriptionResult>, StatusCode> {
    let audio_service = state.audio_service
        .ok_or(StatusCode::SERVICE_UNAVAILABLE)?;
    
    let result = audio_service
        .transcribe_audio(&body)
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    Ok(Json(result))
}

async fn synthesize_speech(
    State(state): State<ThinkAIState>,
    Json(request): Json<SynthesisRequest>,
) -> Result<impl IntoResponse, StatusCode> {
    let audio_service = state.audio_service
        .ok_or(StatusCode::SERVICE_UNAVAILABLE)?;
    
    let audio_data = audio_service
        .synthesize_speech(&request.text, request.voice.as_deref())
        .await
        .map_err(|_| StatusCode::INTERNAL_SERVER_ERROR)?;
    
    let mut headers = HeaderMap::new();
    headers.insert(header::CONTENT_TYPE, "audio/mpeg".parse().unwrap());
    
    Ok((headers, audio_data))
}