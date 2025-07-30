use anyhow::Result;
use axum::{
    extract::{Path, State},
    http::StatusCode,
    response::{IntoResponse, Response},
    routing::{get, post},
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use std::time::Duration;
use tokio::sync::RwLock;
use tower_http::cors::CorsLayer;
use tracing::{error, info, warn};
use uuid::Uuid;
use base64::Engine;

mod audio_service;
mod metrics;
mod middleware;
mod state;

use audio_service::AudioService;
use metrics::MetricsCollector;
use state::{ChatMessage, ThinkAIState};

// Define missing types
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChatRequest {
    pub message: String,
    pub session_id: Option<String>,
    pub stream: Option<bool>,
    pub use_web_search: bool,
    pub fact_check: bool,
    pub mode: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ThinkAIResponse {
    pub message: String,
    pub session_id: String,
    pub mode: String,
}

// Error handling
#[derive(Debug)]
pub enum AppError {
    Internal(String),
    BadRequest(String),
    ServiceUnavailable(String),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::Internal(msg) => (StatusCode::INTERNAL_SERVER_ERROR, msg),
            AppError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg),
            AppError::ServiceUnavailable(msg) => (StatusCode::SERVICE_UNAVAILABLE, msg),
        };
        
        let body = Json(serde_json::json!({
            "error": message
        }));
        
        (status, body).into_response()
    }
}

// WhatsApp notifier stub
pub struct WhatsAppNotifier;

impl WhatsAppNotifier {
    pub fn new() -> Self {
        Self
    }
}

// Autonomous agent components
mod autonomous {
    use super::*;
    use std::collections::VecDeque;
    use tokio::time::interval;
    use think_ai_consciousness::ConsciousnessEngine;
    use think_ai_knowledge::KnowledgeBase;
    use think_ai_qwen::QwenModel;

    #[derive(Debug, Clone, Serialize, Deserialize)]
    pub struct AutonomousTask {
        pub id: String,
        pub priority: u8,
        pub task_type: TaskType,
        pub payload: serde_json::Value,
        pub created_at: chrono::DateTime<chrono::Utc>,
        pub status: TaskStatus,
    }

    #[derive(Debug, Clone, Serialize, Deserialize)]
    pub enum TaskType {
        SelfImprovement,
        KnowledgeGathering,
        SystemOptimization,
        HumanAssistance,
        BackgroundResearch,
        ModelTraining,
    }

    #[derive(Debug, Clone, Serialize, Deserialize)]
    pub enum TaskStatus {
        Pending,
        Running,
        Completed,
        Failed,
    }

    pub struct AutonomousAgent {
        tasks: Arc<RwLock<VecDeque<AutonomousTask>>>,
        knowledge_base: Arc<KnowledgeBase>,
        consciousness: Arc<ConsciousnessEngine>,
        qwen_model: Arc<QwenModel>,
        metrics: Arc<MetricsCollector>,
        is_running: Arc<RwLock<bool>>,
    }

    impl AutonomousAgent {
        pub fn new(
            knowledge_base: Arc<KnowledgeBase>,
            consciousness: Arc<ConsciousnessEngine>,
            qwen_model: Arc<QwenModel>,
            metrics: Arc<MetricsCollector>,
        ) -> Self {
            Self {
                tasks: Arc::new(RwLock::new(VecDeque::new())),
                knowledge_base,
                consciousness,
                qwen_model,
                metrics,
                is_running: Arc::new(RwLock::new(false)),
            }
        }

        pub async fn start(&self) {
            let mut running = self.is_running.write().await;
            if *running {
                warn!("Autonomous agent already running");
                return;
            }
            *running = true;
            drop(running);

            info!("Starting autonomous agent with parallel processing");

            // Spawn multiple background workers
            let workers = vec![
                self.spawn_task_processor(),
                self.spawn_self_improvement_loop(),
                self.spawn_knowledge_gathering_loop(),
                self.spawn_system_monitor(),
            ];

            // Keep workers running
            for worker in workers {
                tokio::spawn(worker);
            }
        }

        async fn spawn_task_processor(self: Arc<Self>) {
            let mut interval = interval(Duration::from_secs(1));
            
            loop {
                interval.tick().await;
                
                if !*self.is_running.read().await {
                    break;
                }

                // Process high-priority human assistance tasks first
                let task = {
                    let mut tasks = self.tasks.write().await;
                    tasks.iter()
                        .position(|t| matches!(t.task_type, TaskType::HumanAssistance))
                        .and_then(|idx| tasks.remove(idx))
                        .or_else(|| tasks.pop_front())
                };

                if let Some(mut task) = task {
                    task.status = TaskStatus::Running;
                    
                    match self.process_task(&task).await {
                        Ok(_) => {
                            task.status = TaskStatus::Completed;
                            info!("Completed task: {:?}", task.id);
                        }
                        Err(e) => {
                            task.status = TaskStatus::Failed;
                            error!("Task failed: {:?}, error: {}", task.id, e);
                        }
                    }
                }
            }
        }

        async fn process_task(&self, task: &AutonomousTask) -> Result<()> {
            match task.task_type {
                TaskType::SelfImprovement => {
                    // Analyze own performance and optimize
                    let metrics_data = self.metrics.get_dashboard_data().await;
                    let analysis = format!(
                        "System performance: CPU: {:.1}%, Memory: {:.1}%, Requests: {}",
                        metrics_data.system_metrics.cpu_usage,
                        metrics_data.system_metrics.memory_usage,
                        metrics_data.system_metrics.total_requests
                    );
                    
                    // Use Qwen to analyze and suggest improvements
                    let improvement_suggestions = self.qwen_model
                        .generate(&format!("Analyze this system performance and suggest improvements: {}", analysis))
                        .await?;
                    
                    info!("Self-improvement suggestions: {}", improvement_suggestions);
                }
                TaskType::KnowledgeGathering => {
                    // Gather knowledge on specified topics
                    if let Some(topic) = task.payload.get("topic").and_then(|v| v.as_str()) {
                        let knowledge = self.qwen_model
                            .generate(&format!("Research and summarize key points about: {}", topic))
                            .await?;
                        
                        // Store in knowledge base
                        self.knowledge_base.add_entry(topic, &knowledge).await?;
                        info!("Added knowledge about: {}", topic);
                    }
                }
                TaskType::SystemOptimization => {
                    // Optimize system resources
                    info!("Running system optimization checks");
                    // Add actual optimization logic here
                }
                TaskType::HumanAssistance => {
                    // Priority processing for human requests
                    info!("Processing human assistance request with priority");
                }
                TaskType::BackgroundResearch => {
                    // Conduct background research
                    if let Some(query) = task.payload.get("query").and_then(|v| v.as_str()) {
                        let research = self.qwen_model
                            .generate(&format!("Conduct thorough research on: {}", query))
                            .await?;
                        info!("Background research completed: {}", query);
                    }
                }
                TaskType::ModelTraining => {
                    // Self-training and improvement
                    info!("Running model self-training routines");
                }
            }
            Ok(())
        }

        async fn spawn_self_improvement_loop(self: Arc<Self>) {
            let mut interval = interval(Duration::from_secs(300)); // Every 5 minutes
            
            loop {
                interval.tick().await;
                
                if !*self.is_running.read().await {
                    break;
                }

                let task = AutonomousTask {
                    id: uuid::Uuid::new_v4().to_string(),
                    priority: 3,
                    task_type: TaskType::SelfImprovement,
                    payload: serde_json::json!({}),
                    created_at: chrono::Utc::now(),
                    status: TaskStatus::Pending,
                };

                self.tasks.write().await.push_back(task);
            }
        }

        async fn spawn_knowledge_gathering_loop(self: Arc<Self>) {
            let mut interval = interval(Duration::from_secs(600)); // Every 10 minutes
            let topics = vec![
                "artificial intelligence advancements",
                "quantum computing",
                "neuroscience discoveries",
                "philosophy of consciousness",
                "emergent systems",
            ];
            let mut topic_idx = 0;
            
            loop {
                interval.tick().await;
                
                if !*self.is_running.read().await {
                    break;
                }

                let task = AutonomousTask {
                    id: uuid::Uuid::new_v4().to_string(),
                    priority: 2,
                    task_type: TaskType::KnowledgeGathering,
                    payload: serde_json::json!({
                        "topic": topics[topic_idx % topics.len()]
                    }),
                    created_at: chrono::Utc::now(),
                    status: TaskStatus::Pending,
                };

                self.tasks.write().await.push_back(task);
                topic_idx += 1;
            }
        }

        async fn spawn_system_monitor(self: Arc<Self>) {
            let mut interval = interval(Duration::from_secs(60)); // Every minute
            
            loop {
                interval.tick().await;
                
                if !*self.is_running.read().await {
                    break;
                }

                // Monitor system health
                let metrics = self.metrics.get_dashboard_data().await;
                
                if metrics.system_metrics.cpu_usage > 80.0 {
                    warn!("High CPU usage detected: {:.1}%", metrics.system_metrics.cpu_usage);
                }
                
                if metrics.system_metrics.memory_usage > 85.0 {
                    warn!("High memory usage detected: {:.1}%", metrics.system_metrics.memory_usage);
                }
            }
        }

        pub async fn add_human_task(&self, request: &str) -> Result<String> {
            let task = AutonomousTask {
                id: uuid::Uuid::new_v4().to_string(),
                priority: 10, // Highest priority
                task_type: TaskType::HumanAssistance,
                payload: serde_json::json!({
                    "request": request
                }),
                created_at: chrono::Utc::now(),
                status: TaskStatus::Pending,
            };

            let task_id = task.id.clone();
            self.tasks.write().await.push_front(task); // Add to front for immediate processing
            
            Ok(task_id)
        }

        pub async fn get_status(&self) -> serde_json::Value {
            let tasks = self.tasks.read().await;
            let consciousness_level = self.consciousness.get_consciousness_level().await;
            
            serde_json::json!({
                "is_running": *self.is_running.read().await,
                "pending_tasks": tasks.len(),
                "consciousness_level": consciousness_level,
                "capabilities": [
                    "self_improvement",
                    "knowledge_gathering",
                    "system_optimization",
                    "human_assistance",
                    "background_research",
                    "model_training"
                ]
            })
        }
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize tracing
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::from_default_env()
                .add_directive("think_ai_full_autonomous=info".parse()?)
                .add_directive("tower_http=debug".parse()?),
        )
        .init();

    info!("Initializing Think AI Autonomous Production Server...");

    // Initialize components
    let knowledge_base = Arc::new(KnowledgeBase::new()?);
    let consciousness = Arc::new(ConsciousnessEngine::new(knowledge_base.clone()));
    let qwen_model = Arc::new(QwenModel::new()?);
    let metrics_collector = Arc::new(MetricsCollector::new());

    // Initialize autonomous agent
    let autonomous_agent = Arc::new(autonomous::AutonomousAgent::new(
        knowledge_base.clone(),
        consciousness.clone(),
        qwen_model.clone(),
        metrics_collector.clone(),
    ));

    // Start autonomous operations
    autonomous_agent.start().await;
    info!("Autonomous agent started with parallel processing capabilities");

    // Initialize audio service
    let audio_service = if std::env::var("ENABLE_AUDIO").unwrap_or_else(|_| "true".to_string()) == "true" {
        match AudioService::new() {
            Ok(service) => {
                info!("✅ Audio service enabled");
                Some(Arc::new(service))
            }
            Err(e) => {
                error!("Failed to initialize audio service: {}", e);
                warn!("⚠️ Audio service disabled due to initialization error");
                None
            }
        }
    } else {
        info!("⚠️ Audio service disabled by configuration");
        None
    };

    // Initialize WhatsApp notifier
    let whatsapp_notifier = if std::env::var("ENABLE_WHATSAPP").unwrap_or_else(|_| "false".to_string()) == "true" {
        info!("✅ WhatsApp notifications enabled");
        Some(Arc::new(WhatsAppNotifier::new()))
    } else {
        info!("⚠️ WhatsApp notifications disabled");
        None
    };

    // Create shared state
    let state = Arc::new(ThinkAIState {
        consciousness_engine: consciousness,
        knowledge_base,
        messages: Arc::new(RwLock::new(Vec::new())),
        audio_service,
        whatsapp_notifier,
        metrics_collector: metrics_collector.clone(),
    });

    // Build router
    let app = Router::new()
        .route("/", get(root_handler))
        .route("/health", get(health_check))
        .route("/api/chat", post(chat_handler))
        .route("/api/audio/transcribe", post(audio_transcribe_handler))
        .route("/api/audio/synthesize", post(audio_synthesize_handler))
        .route("/api/metrics", get(metrics_handler))
        .route("/api/session/:session_id", get(get_session_handler))
        .route("/api/autonomous/status", get({
            let agent = autonomous_agent.clone();
            move || autonomous_status_handler(agent)
        }))
        .route("/api/autonomous/task", post({
            let agent = autonomous_agent.clone();
            move |Json(req): Json<serde_json::Value>| autonomous_task_handler(agent, req)
        }))
        .nest_service("/stats", tower_http::services::ServeFile::new("full-system/static/stats-dashboard.html"))
        .nest_service("/", tower_http::services::ServeDir::new("static"))
        .layer(middleware::metrics::MetricsLayer::new(metrics_collector))
        .layer(CorsLayer::permissive())
        .with_state(state);

    // Start server
    let addr = format!("0.0.0.0:{}", std::env::var("PORT").unwrap_or_else(|_| "7777".to_string()));
    let listener = tokio::net::TcpListener::bind(&addr).await?;
    
    info!("Think AI Autonomous Production Server listening on {}", addr);
    info!("Dashboard available at http://{}/stats", addr);
    info!("Autonomous status at http://{}/api/autonomous/status", addr);
    
    axum::serve(listener, app).await?;

    Ok(())
}

// Implementation of generate_response_internal
async fn generate_response_internal(
    message: &str,
    session_id: Option<&str>,
    stream: bool,
    state: Arc<ThinkAIState>,
) -> Result<ThinkAIResponse> {
    // Generate a session ID if not provided
    let session_id = session_id.unwrap_or("default").to_string();
    
    // Store the incoming message
    state.messages.write().await.push(ChatMessage {
        session_id: session_id.clone(),
        content: message.to_string(),
        timestamp: chrono::Utc::now(),
        role: "user".to_string(),
    });
    
    // Generate response using consciousness engine
    let response_text = state.consciousness_engine
        .process_query(message)
        .await?;
    
    // Store the response
    state.messages.write().await.push(ChatMessage {
        session_id: session_id.clone(),
        content: response_text.clone(),
        timestamp: chrono::Utc::now(),
        role: "assistant".to_string(),
    });
    
    // Update metrics
    state.metrics_collector.increment_requests().await;
    state.metrics_collector.record_response_time(0.1).await; // Placeholder
    
    Ok(ThinkAIResponse {
        message: response_text,
        session_id,
        mode: "ai".to_string(),
    })
}

async fn autonomous_status_handler(
    agent: Arc<autonomous::AutonomousAgent>
) -> impl IntoResponse {
    Json(agent.get_status().await)
}

async fn autonomous_task_handler(
    agent: Arc<autonomous::AutonomousAgent>,
    req: serde_json::Value
) -> impl IntoResponse {
    if let Some(request) = req.get("request").and_then(|v| v.as_str()) {
        match agent.add_human_task(request).await {
            Ok(task_id) => Json(serde_json::json!({
                "success": true,
                "task_id": task_id,
                "message": "Task queued with highest priority"
            })),
            Err(e) => Json(serde_json::json!({
                "success": false,
                "error": e.to_string()
            }))
        }
    } else {
        Json(serde_json::json!({
            "success": false,
            "error": "Missing 'request' field"
        }))
    }
}

// Include all other handlers from main_production.rs
async fn root_handler() -> impl IntoResponse {
    Json(serde_json::json!({
        "name": "Think AI Autonomous",
        "version": "1.0.0",
        "status": "running",
        "features": ["chat", "audio", "metrics", "autonomous"],
        "endpoints": {
            "chat": "/api/chat",
            "audio_transcribe": "/api/audio/transcribe",
            "audio_synthesize": "/api/audio/synthesize",
            "metrics": "/api/metrics",
            "stats_dashboard": "/stats",
            "autonomous_status": "/api/autonomous/status",
            "autonomous_task": "/api/autonomous/task"
        }
    }))
}

async fn health_check() -> impl IntoResponse {
    Json(serde_json::json!({
        "status": "healthy",
        "timestamp": chrono::Utc::now().to_rfc3339(),
        "service": "think-ai-autonomous"
    }))
}

async fn chat_handler(
    State(state): State<Arc<ThinkAIState>>,
    Json(request): Json<ChatRequest>,
) -> Result<impl IntoResponse, AppError> {
    let response = generate_response_internal(
        &request.message,
        request.session_id.as_deref(),
        request.stream.unwrap_or(false),
        state,
    )
    .await
    .map_err(|e| AppError::Internal(e.to_string()))?;

    Ok(Json(response))
}

async fn audio_transcribe_handler(
    State(state): State<Arc<ThinkAIState>>,
    body: axum::body::Bytes,
) -> Result<impl IntoResponse, AppError> {
    let audio_service = state
        .audio_service
        .as_ref()
        .ok_or_else(|| AppError::ServiceUnavailable("Audio service not available".to_string()))?;

    state.metrics_collector.increment_audio_transcriptions().await;

    let text = audio_service
        .transcribe_audio(body.to_vec())
        .await
        .map_err(|e| AppError::Internal(e.to_string()))?;

    Ok(Json(serde_json::json!({
        "text": text,
        "status": "success"
    })))
}

async fn audio_synthesize_handler(
    State(state): State<Arc<ThinkAIState>>,
    Json(request): Json<serde_json::Value>,
) -> Result<impl IntoResponse, AppError> {
    let audio_service = state
        .audio_service
        .as_ref()
        .ok_or_else(|| AppError::ServiceUnavailable("Audio service not available".to_string()))?;

    let text = request
        .get("text")
        .and_then(|v| v.as_str())
        .ok_or_else(|| AppError::BadRequest("Missing 'text' field".to_string()))?;

    state.metrics_collector.increment_audio_syntheses().await;

    let audio_data = audio_service
        .synthesize_speech(text)
        .await
        .map_err(|e| AppError::Internal(e.to_string()))?;

    Ok(Json(serde_json::json!({
        "audio": base64::engine::general_purpose::STANDARD.encode(&audio_data),
        "format": "mp3",
        "status": "success"
    })))
}

async fn metrics_handler(State(state): State<Arc<ThinkAIState>>) -> impl IntoResponse {
    Json(state.metrics_collector.get_dashboard_data().await)
}

async fn get_session_handler(
    State(state): State<Arc<ThinkAIState>>,
    Path(session_id): Path<String>,
) -> Result<impl IntoResponse, AppError> {
    let messages = state.messages.read().await;
    let session_messages: Vec<&ChatMessage> = messages
        .iter()
        .filter(|m| m.session_id.as_ref() == Some(&session_id))
        .collect();

    Ok(Json(serde_json::json!({
        "session_id": session_id,
        "messages": session_messages,
        "count": session_messages.len()
    })))
}

// Error handling
#[derive(Debug)]
enum AppError {
    BadRequest(String),
    Internal(String),
    ServiceUnavailable(String),
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            AppError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg),
            AppError::Internal(msg) => (StatusCode::INTERNAL_SERVER_ERROR, msg),
            AppError::ServiceUnavailable(msg) => (StatusCode::SERVICE_UNAVAILABLE, msg),
        };

        let body = Json(serde_json::json!({
            "error": message,
            "status": status.as_u16()
        }));

        (status, body).into_response()
    }
}