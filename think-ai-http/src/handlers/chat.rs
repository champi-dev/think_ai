// Chat handler for O(1) conversation interface with session context management

use crate::router::AppState;
use axum::{
    extract::{rejection::JsonRejection, State},
    http::StatusCode,
    response::IntoResponse,
    Json,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use think_ai_knowledge::response_generator::ComponentResponseGenerator;
use uuid::Uuid;

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
    session_id: String,
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
                JsonRejection::MissingJsonContentType(_) => {
                    "Missing 'Content-Type: application/json' header"
                }
                _ => "Failed to parse request body",
            };
            return (
                StatusCode::BAD_REQUEST,
                Json(ChatResponse {
                    response: String::new(),
                    session_id: String::new(),
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
            Json(ChatResponse {
                response: String::new(),
                session_id: request.session_id.clone().unwrap_or_default(),
                error: Some("Message cannot be empty".to_string()),
            }),
        )
            .into_response();
    }
    let query = request.query.trim();
    // Additional validation
    if query.is_empty() {
        return (
            StatusCode::BAD_REQUEST,
            Json(ChatResponse {
                response: String::new(),
                session_id: request.session_id.clone().unwrap_or_default(),
                error: Some("Message cannot be empty after trimming".to_string()),
            }),
        )
            .into_response();
    }

    // Limit query length to prevent abuse
    if query.len() > 2000 {
        return (
            StatusCode::BAD_REQUEST,
            Json(ChatResponse {
                response: String::new(),
                session_id: request.session_id.clone().unwrap_or_default(),
                error: Some("Message too long (max 2000 characters)".to_string()),
            }),
        )
            .into_response();
    }
    // Handle session ID - create new one if not provided
    let session_id = request.session_id.unwrap_or_else(|| Uuid::new_v4().to_string());
    
    // Use session ID to maintain conversation context
    let memory = state.conversation_memory.clone();
    
    // Add user message to conversation memory
    memory.add_message(
        session_id.clone(),
        "user".to_string(),
        query.to_string(),
    );
    
    // Get conversation history for context
    let previous_context = memory.get_conversation_context(&session_id, 10);
    
    // Use ComponentResponseGenerator with conversation memory for long-term context
    let response_generator = ComponentResponseGenerator::new_with_memory(
        state.knowledge_engine.clone(),
        state.conversation_memory.clone(),
    );
    
    // Generate response with conversation context
    let context_query = if let Some(context) = previous_context {
        if !context.is_empty() {
            let context_str = context
                .iter()
                .map(|(role, content)| format!("{}: {}", role, content))
                .collect::<Vec<_>>()
                .join("\n");
            format!("Previous conversation:\n{}\n\nCurrent query: {}", context_str, query)
        } else {
            query.to_string()
        }
    } else {
        query.to_string()
    };
    
    let response = response_generator.generate_response_with_memory(&context_query, None);
    
    // Add assistant response to conversation memory
    memory.add_message(
        session_id.clone(),
        "assistant".to_string(),
        response.clone(),
    );
    
    (
        StatusCode::OK,
        Json(ChatResponse {
            response,
            session_id,
            error: None,
        }),
    )
        .into_response()
}
