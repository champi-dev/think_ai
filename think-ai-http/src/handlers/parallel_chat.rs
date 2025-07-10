// Parallel consciousness chat handler - uses Qwen with background threads

use crate::router::AppState;
use axum::{
    extract::{rejection::JsonRejection, State},
    http::StatusCode,
    response::IntoResponse,
    Json,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use think_ai_consciousness::parallel_consciousness::ParallelConsciousness;

#[derive(Debug, Deserialize)]
pub struct ParallelChatRequest {
    #[serde(alias = "message")]
    query: String,
    #[serde(default)]
    session_id: Option<String>,
}

#[derive(Debug, Serialize)]
pub struct ParallelChatResponse {
    response: String,
    consciousness_state: serde_json::Value,
    processing_time: f64,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<String>,
}

pub async fn parallel_chat(
    State(state): State<Arc<AppState>>,
    payload: Result<Json<ParallelChatRequest>, JsonRejection>,
) -> impl IntoResponse {
    let start = std::time::Instant::now();
    
    // Handle JSON parsing errors
    let Json(request) = match payload {
        Ok(json) => json,
        Err(e) => {
            let error_msg = match e {
                JsonRejection::JsonDataError(_) => "Invalid JSON format in request body",
                JsonRejection::MissingJsonContentType(_) => {
                    "Missing 'Content-Type: application/json' header"
                }
                _ => "Failed to parse request body",
            };
            return (
                StatusCode::BAD_REQUEST,
                Json(ParallelChatResponse {
                    response: String::new(),
                    consciousness_state: serde_json::json!({}),
                    processing_time: 0.0,
                    error: Some(error_msg.to_string()),
                }),
            )
                .into_response();
        }
    };
    
    // Validate request
    if request.query.is_empty() {
        return (
            StatusCode::BAD_REQUEST,
            Json(ParallelChatResponse {
                response: String::new(),
                consciousness_state: serde_json::json!({}),
                processing_time: 0.0,
                error: Some("Message cannot be empty".to_string()),
            }),
        )
            .into_response();
    }
    
    let query = request.query.trim();
    
    // Get or create parallel consciousness instance
    let consciousness = state.parallel_consciousness.clone();
    
    // Process message through parallel consciousness
    let response = consciousness.process_user_message(query).await;
    
    // Get consciousness state
    let consciousness_state = consciousness.get_consciousness_state();
    
    let processing_time = start.elapsed().as_secs_f64();
    
    (
        StatusCode::OK,
        Json(ParallelChatResponse {
            response,
            consciousness_state: serde_json::json!(consciousness_state),
            processing_time,
            error: None,
        }),
    )
        .into_response()
}

pub fn initialize_parallel_consciousness() -> Arc<ParallelConsciousness> {
    let consciousness = Arc::new(ParallelConsciousness::new());
    
    // Start all background threads
    consciousness.start();
    
    consciousness
}