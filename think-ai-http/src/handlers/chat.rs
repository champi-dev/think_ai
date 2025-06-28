//! Chat handler for O(1) conversation interface

use axum::{
    extract::State,
    http::StatusCode,
    Json,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use crate::router::AppState;
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
    Json(request): Json<ChatRequest>,
) -> Result<Json<ChatResponse>, StatusCode> {
    let query = request.query.trim();
    
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
    
    Ok(Json(ChatResponse {
        response,
        error: None,
    }))
}