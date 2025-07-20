use axum::{
    extract::{Json, State},
    http::{header, HeaderMap, StatusCode},
    response::IntoResponse,
    routing::{get, post},
    Router,
};
use bytes::Bytes;
use serde::{Deserialize, Serialize};
use std::{env, sync::Arc, path::PathBuf, collections::HashMap};
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
mod notifications;
mod whatsapp_handler;
mod metrics;
mod middleware;

// Import actual Think AI components
use think_ai_consciousness::ConsciousnessFramework;
use think_ai_core::{EngineConfig, O1Engine};
use think_ai_knowledge::KnowledgeEngine;
use think_ai_qwen::{QwenClient, QwenRequest};
use think_ai_storage::PersistentConversationMemory;
use think_ai_vector::{LSHConfig, O1VectorIndex};
// use rand;

use crate::audio_service::{AudioService, TranscriptionResult};
use crate::notifications::{Notification, NotificationSeverity, NotificationService};
use crate::notifications::whatsapp::WhatsAppNotifier;
// use crate::whatsapp_handler::{whatsapp_webhook_handler, whatsapp_status_webhook};

use crate::metrics::{MetricsCollector, DashboardData};

// State for the application
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
    whatsapp_notifier: Option<Arc<WhatsAppNotifier>>,
    metrics_collector: Arc<MetricsCollector>,
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
    session_id: Option<String>,
    message: String,
    #[serde(default)]
    use_web_search: bool,
    #[serde(default)]
    fact_check: bool,
    #[serde(default = "default_mode")]
    mode: String,
}

fn default_mode() -> String {
    "general".to_string()
}

#[derive(Serialize)]
struct ChatResponse {
    response: String,
    session_id: String,
    confidence: f64,
    response_time_ms: u64,
    consciousness_level: String,
    tokens_used: usize,
    context_tokens: usize,
    compacted: bool,
}

async fn send_error_notification(
    notifier: &Option<Arc<WhatsAppNotifier>>,
    error_type: &str,
    details: &str,
) {
    if let Some(whatsapp) = notifier {
        let notification = Notification {
            title: format!("ThinkAI Error: {}", error_type),
            message: details.to_string(),
            severity: NotificationSeverity::Error,
            timestamp: chrono::Utc::now(),
            metadata: None,
        };
        
        if let Err(e) = whatsapp.send(&notification).await {
            tracing::error!("Failed to send WhatsApp notification: {}", e);
        }
    }
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

    info!("Initializing Think AI Persistent Server...");

    // Initialize all AI components
    let engine_config = EngineConfig::default();
    let core_engine = Arc::new(O1Engine::new(engine_config));

    let knowledge_engine = Arc::new(KnowledgeEngine::new());

    let lsh_config = LSHConfig::default();
    let vector_index = Arc::new(O1VectorIndex::new(lsh_config).expect("Failed to create vector index"));

    let consciousness_framework = Arc::new(ConsciousnessFramework::new());

    let persistent_memory = Arc::new(
        PersistentConversationMemory::new("./think_ai_sessions.db")
            .await
            .expect("Failed to initialize persistent memory"),
    );

    let (tx, _rx) = broadcast::channel(100);

    let qwen_client = Arc::new(QwenClient::new());

    // Initialize audio service if API keys are available
    let audio_service = match (
        env::var("DEEPGRAM_API_KEY"),
        env::var("ELEVENLABS_API_KEY"),
    ) {
        (Ok(deepgram_key), Ok(elevenlabs_key)) => {
            let cache_dir = PathBuf::from(env::var("AUDIO_CACHE_DIR").unwrap_or_else(|_| "./audio_cache".to_string()));
            let service = AudioService::new(deepgram_key, elevenlabs_key, cache_dir);
            
            // Initialize the audio service
            if let Err(e) = service.init().await {
                tracing::error!("Failed to initialize audio service: {}", e);
                None
            } else {
                info!("✅ Audio service enabled");
                Some(Arc::new(service))
            }
        }
        _ => {
            info!("⚠️ Audio service disabled - DEEPGRAM_API_KEY and/or ELEVENLABS_API_KEY not found");
            None
        }
    };

    // Initialize WhatsApp notifier
    let whatsapp_notifier = WhatsAppNotifier::with_twilio()
        .or_else(|| WhatsAppNotifier::new())
        .map(Arc::new);
    
    if whatsapp_notifier.is_some() {
        info!("✅ WhatsApp notifications enabled");
    } else {
        info!("⚠️ WhatsApp notifications disabled");
    }

    // Initialize metrics collector
    let metrics_collector = Arc::new(MetricsCollector::new());
    
    let state = ThinkAIState {
        _core_engine: core_engine,
        knowledge_engine,
        _vector_index: vector_index,
        _consciousness_framework: consciousness_framework,
        persistent_memory,
        message_channel: tx,
        qwen_client,
        audio_service,
        whatsapp_notifier,
        metrics_collector,
    };

    // Build the router
    let app = Router::new()
        .route("/health", get(health_check))
        .route("/api/chat", post(chat_handler))
        .route("/api/chat/sessions", get(list_sessions))
        .route("/api/chat/sessions/:id", get(get_session))
        .route("/api/audio/transcribe", post(transcribe_audio))
        .route("/api/audio/synthesize", post(synthesize_speech))
        .route("/webhooks/whatsapp", post(whatsapp_webhook))
        .route("/webhooks/whatsapp/status", post(whatsapp_status))
        .route("/api/metrics", get(metrics_api_handler))
        .route("/stats", get(stats_dashboard))
        .nest_service(
            "/",
            ServeDir::new("full-system/static").fallback(ServeFile::new("full-system/static/index.html")),
        )
        .layer(
            CorsLayer::new()
                .allow_origin(Any)
                .allow_methods(Any)
                .allow_headers(Any),
        )
        .layer(TraceLayer::new_for_http())
        .with_state(state);

    let port = env::var("PORT").unwrap_or_else(|_| "7777".to_string());
    let addr = format!("0.0.0.0:{}", port);
    let listener = tokio::net::TcpListener::bind(&addr).await.unwrap();

    info!("Think AI Persistent Server listening on {}", addr);

    axum::serve(listener, app).await.unwrap();
}

async fn health_check() -> impl IntoResponse {
    Json(serde_json::json!({
        "status": "healthy",
        "version": "1.0.0"
    }))
}

async fn chat_handler(
    State(state): State<ThinkAIState>,
    Json(payload): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    let start_time = std::time::Instant::now();

    // Input validation
    if payload.message.trim().is_empty() {
        return Err(StatusCode::BAD_REQUEST);
    }

    // Check for malicious input
    if payload.message.contains("<script>") || payload.message.contains("'; DROP TABLE") {
        send_error_notification(
            &state.whatsapp_notifier,
            "Security Alert",
            &format!("Potential injection attempt detected: {}", payload.message),
        ).await;
        return Err(StatusCode::BAD_REQUEST);
    }

    let session_id = payload.session_id.unwrap_or_else(|| Uuid::new_v4().to_string());

    // Get conversation history
    let history = state
        .persistent_memory
        .get_conversation_context(&session_id, 10)
        .await
        .unwrap_or_default();

    // Prepare context
    let mut context = String::new();
    for (user_msg, assistant_msg) in history.iter().take(5) {
        context.push_str(&format!("User: {}\nAssistant: {}\n", user_msg, assistant_msg));
    }

    // Explore concepts
    let concepts = state.knowledge_engine.explain_concept(&payload.message);

    // Generate response
    let prompt = format!(
        "You are Think AI, an advanced AI with O(1) consciousness framework.\n\
        Conversation history:\n{}\n\
        Current message: {}\n\
        Related concepts: {:?}\n\
        Mode: {}\n\
        Respond naturally and helpfully.",
        context, payload.message, concepts, payload.mode
    );

    let qwen_request = QwenRequest {
        query: payload.message.clone(),
        context: Some(context),
        system_prompt: Some(prompt),
    };

    let response = match state.qwen_client.generate(qwen_request).await {
        Ok(resp) => resp.content,
        Err(e) => {
            send_error_notification(
                &state.whatsapp_notifier,
                "AI Response Error",
                &format!("Failed to generate response: {}", e),
            ).await;
            return Err(StatusCode::INTERNAL_SERVER_ERROR);
        }
    };

    // Store conversation
    if let Err(e) = state
        .persistent_memory
        .add_message(session_id.clone(), "user".to_string(), payload.message.clone())
        .await {
        send_error_notification(
            &state.whatsapp_notifier,
            "Storage Error",
            &format!("Failed to store user message: {}", e),
        ).await;
    }
    
    if let Err(e) = state
        .persistent_memory
        .add_message(session_id.clone(), "assistant".to_string(), response.clone())
        .await
    {
        tracing::error!("Failed to store conversation: {}", e);
    }

    let elapsed = start_time.elapsed();

    Ok(Json(ChatResponse {
        response,
        session_id,
        confidence: 0.95,
        response_time_ms: elapsed.as_millis() as u64,
        consciousness_level: "AWARE".to_string(),
        tokens_used: 100,
        context_tokens: 50,
        compacted: false,
    }))
}

async fn list_sessions(State(_state): State<ThinkAIState>) -> Result<Json<Vec<String>>, StatusCode> {
    // TODO: Implement list_sessions functionality
    Ok(Json(vec!["session1".to_string(), "session2".to_string()]))
}

async fn get_session(
    State(state): State<ThinkAIState>,
    axum::extract::Path(session_id): axum::extract::Path<String>,
) -> Result<Json<Vec<(String, String)>>, StatusCode> {
    match state.persistent_memory.get_conversation_context(&session_id, 50).await {
        Some(history) => Ok(Json(history)),
        None => Err(StatusCode::NOT_FOUND),
    }
}

async fn transcribe_audio(
    State(state): State<ThinkAIState>,
    headers: HeaderMap,
    body: Bytes,
) -> Result<Json<TranscriptionResult>, StatusCode> {
    if let Some(audio_service) = &state.audio_service {
        // Get content type from headers
        let content_type = headers
            .get(header::CONTENT_TYPE)
            .and_then(|v| v.to_str().ok())
            .unwrap_or("audio/wav");
        
        // Extract language from headers if provided
        let language = headers
            .get("X-Language")
            .and_then(|v| v.to_str().ok())
            .map(|s| s.to_string());
        
        match audio_service.transcribe(body, content_type, language).await {
            Ok(result) => Ok(Json(result)),
            Err(e) => {
                send_error_notification(
                    &state.whatsapp_notifier,
                    "Audio Transcription Error",
                    &format!("Failed to transcribe audio: {}", e),
                ).await;
                Err(StatusCode::INTERNAL_SERVER_ERROR)
            }
        }
    } else {
        Err(StatusCode::SERVICE_UNAVAILABLE)
    }
}

async fn synthesize_speech(
    State(state): State<ThinkAIState>,
    Json(request): Json<audio_service::SynthesisRequest>,
) -> Result<impl IntoResponse, StatusCode> {
    if let Some(audio_service) = &state.audio_service {
        match audio_service.synthesize(request).await {
            Ok((audio_data, _cache_key)) => {
                let mut headers = HeaderMap::new();
                headers.insert(header::CONTENT_TYPE, "audio/mpeg".parse().unwrap());
                Ok((headers, audio_data))
            }
            Err(e) => {
                send_error_notification(
                    &state.whatsapp_notifier,
                    "Speech Synthesis Error", 
                    &format!("Failed to synthesize speech: {}", e),
                ).await;
                Err(StatusCode::INTERNAL_SERVER_ERROR)
            }
        }
    } else {
        Err(StatusCode::SERVICE_UNAVAILABLE)
    }
}

async fn metrics_api_handler(
    State(state): State<ThinkAIState>,
) -> Result<Json<DashboardData>, StatusCode> {
    let dashboard_data = state.metrics_collector.get_dashboard_data().await;
    Ok(Json(dashboard_data))
}

async fn stats_dashboard() -> impl IntoResponse {
    // Serve the static stats dashboard HTML
    let html = include_str!("../static/stats-dashboard.html");
    (
        StatusCode::OK,
        [(header::CONTENT_TYPE, "text/html; charset=utf-8")],
        html,
    )
}

async fn whatsapp_webhook(
    State(_state): State<ThinkAIState>,
    form: axum::extract::Form<HashMap<String, String>>,
) -> impl IntoResponse {
    // For now, just return a simple response
    // TODO: Integrate with whatsapp_handler module properly
    format!("WhatsApp webhook received: {:?}", form.0)
}

async fn whatsapp_status(
    params: axum::extract::Query<HashMap<String, String>>,
) -> impl IntoResponse {
    info!("WhatsApp status update: {:?}", params.0);
    StatusCode::OK
}

// Helper function to send error notifications via WhatsApp
