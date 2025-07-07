//! Chat handler for O(1) conversation interface

use axum::{
    extract::{State, rejection::JsonRejection},
    http::StatusCode,
    Json,
    response::IntoResponse,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use crate::router::AppState;
use crate::errors::ApiError;
use think_ai_knowledge::response_generator::ComponentResponseGenerator;
use std::collections::HashMap;

#[derive(Debug, Deserialize)]
pub struct ChatRequest {
    #[serde(alias = "message")]
    query: String,
    #[serde(default)]
    session_id: Option<String>,
}

#[derive(Debug, Serialize)]
pub struct ChatResponse {
    response: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    error: Option<String>,
}

pub async fn chat(
    State(state): State<Arc<AppState>>,
    payload: Result<Json<ChatRequest>, JsonRejection>,
) -> impl IntoResponse {
    // Handle JSON parsing errors
    let Json(request) = match payload {
        Ok(json) => json,
        Err(e) => {
            let error_msg = match e {
                JsonRejection::JsonDataError(_) => "Invalid JSON format in request body",
                JsonRejection::MissingJsonContentType(_) => "Missing 'Content-Type: application/json' header",
                _ => "Failed to parse request body",
            };
            return (
                StatusCode::BAD_REQUEST,
                Json(ChatResponse {
                    response: String::new(),
                    error: Some(error_msg.to_string()),
                })
            ).into_response();
        }
    };
    // Validate request
    if request.query.is_empty() {
        return (
            StatusCode::BAD_REQUEST,
            Json(ChatResponse {
                response: String::new(),
                error: Some("Message cannot be empty".to_string()),
            })
        ).into_response();
    }
    
    let query = request.query.trim();
    
    // Additional validation
    if query.is_empty() {
        return (
            StatusCode::BAD_REQUEST,
            Json(ChatResponse {
                response: String::new(),
                error: Some("Message cannot be empty after trimming".to_string()),
            })
        ).into_response();
    }
    
    // Limit query length to prevent abuse
    if query.len() > 2000 {
        return (
            StatusCode::BAD_REQUEST,
            Json(ChatResponse {
                response: String::new(),
                error: Some("Message too long (max 2000 characters)".to_string()),
            })
        ).into_response();
    }
    
    // Use ComponentResponseGenerator with conversation memory for long-term context
    let response_generator = ComponentResponseGenerator::new_with_memory(
        state.knowledge_engine.clone(),
        state.conversation_memory.clone()
    );
    
    // Get memory stats to see recent turns for context
    let memory_stats = state.conversation_memory.get_stats();
    let previous_response = if memory_stats.total_turns > 0 {
        // For now, we'll pass None since we need to refactor to get the last response
        // This will be improved when we add session-based memory tracking
        None
    } else {
        None
    };
    
    // Generate response with memory context
    let response = response_generator.generate_response_with_memory(query, previous_response);
    
    (
        StatusCode::OK,
        Json(ChatResponse {
            response,
            error: None,
        })
    ).into_response()
}