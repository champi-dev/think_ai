use axum::{
    extract::State,
    http::StatusCode,
    response::IntoResponse,
    Json,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use think_ai_quantum_gen::{QuantumGenerationEngine, GenerationRequest, ThreadType};
use uuid::Uuid;

#[derive(Debug, Deserialize)]
pub struct QuantumChatRequest {
    pub query: String,
    pub context_id: Option<Uuid>,
    pub thread_type: Option<String>,
    pub temperature: Option<f32>,
}

#[derive(Debug, Serialize)]
pub struct QuantumChatResponse {
    pub response: String,
    pub context_id: Uuid,
    pub thread_id: Uuid,
    pub generation_time_ms: u64,
    pub model: String,
    pub thread_type: String,
}

#[derive(Clone)]
pub struct QuantumChatState {
    pub generation_engine: Arc<QuantumGenerationEngine>,
}

/// Quantum chat handler - Always uses Qwen with isolated parallel processing
pub async fn quantum_chat(
    State(state): State<Arc<QuantumChatState>>,
    Json(request): Json<QuantumChatRequest>,
) -> impl IntoResponse {
    // Parse thread type
    let thread_type = match request.thread_type.as_deref() {
        Some("thinking") => ThreadType::Thinking,
        Some("dreaming") => ThreadType::Dreaming,
        Some("self_reflection") => ThreadType::SelfReflection,
        Some("knowledge_creation") => ThreadType::KnowledgeCreation,
        Some("training") => ThreadType::Training,
        _ => ThreadType::UserChat,
    };
    
    // Create generation request
    let gen_request = GenerationRequest {
        query: request.query,
        context_id: request.context_id,
        thread_type,
        temperature: request.temperature,
        max_tokens: None,
    };
    
    // Generate response using quantum engine (Qwen only, no fallback)
    match state.generation_engine.generate(gen_request).await {
        Ok(response) => {
            let chat_response = QuantumChatResponse {
                response: response.text,
                context_id: response.context_id,
                thread_id: response.thread_id,
                generation_time_ms: response.generation_time_ms,
                model: response.model_used,
                thread_type: format!("{:?}", thread_type),
            };
            
            (StatusCode::OK, Json(chat_response))
        }
        Err(e) => {
            eprintln!("Quantum generation error: {}", e);
            
            // Return error response
            let error_response = serde_json::json!({
                "error": "Quantum generation failed. Ensure Ollama is running with Qwen model.",
                "details": e.to_string()
            });
            
            (StatusCode::SERVICE_UNAVAILABLE, Json(error_response))
        }
    }
}

/// Get quantum generation statistics
pub async fn quantum_stats(
    State(state): State<Arc<QuantumChatState>>,
) -> impl IntoResponse {
    // This would need to be implemented in the QuantumGenerationEngine
    let stats = serde_json::json!({
        "status": "quantum generation active",
        "model": "qwen2.5:1.5b",
        "features": [
            "isolated parallel threads",
            "shared intelligence",
            "O(1) cache performance",
            "context persistence"
        ]
    });
    
    Json(stats)
}