//! Chat handler for O(1) conversation interface

use axum::{
    extract::State,
    http::StatusCode,
    Json,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use crate::router::AppState;

#[derive(Debug, Deserialize)]
pub struct ChatRequest {
    message: String,
}

#[derive(Debug, Serialize)]
pub struct ChatResponse {
    response: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<String>,
}

pub async fn chat(
    State(state): State<Arc<AppState>>,
    Json(request): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    // Use the O1Engine to process the message
    match state.engine.compute(&request.message) {
        Some(result) => Ok(Json(ChatResponse {
            response: result.value.to_string(),
            error: None,
        })),
        None => Ok(Json(ChatResponse {
            response: String::new(),
            error: Some("No response computed for this message".to_string()),
        })),
    }
}