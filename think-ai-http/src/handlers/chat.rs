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

#[derive(Debug, Deserialize)]
pub struct ChatRequest {
    #[serde(alias = "message")]
    query: String,
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
    
    // Use ComponentResponseGenerator with Turing test conversational components
    let response_generator = ComponentResponseGenerator::new(state.knowledge_engine.clone());
    let response = response_generator.generate_response(query);
    
    Ok(Json(ChatResponse {
        response,
        error: None,
    }))
}