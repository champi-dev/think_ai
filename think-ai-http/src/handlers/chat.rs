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
    #[serde(alias = "query")]
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
    let query = request.message.trim();
    
    // Handle greetings with O(1) response
    match query.to_lowercase().as_str() {
        "hi" | "hello" | "hey" => {
            return Ok(Json(ChatResponse {
                response: "Hello! I'm Think AI with a comprehensive knowledge base. What would you like to know?".to_string(),
                error: None,
            }));
        }
        _ => {}
    }
    
    // First try direct query to knowledge base
    if let Some(results) = state.knowledge_engine.query(query) {
        if !results.is_empty() {
            return Ok(Json(ChatResponse {
                response: results[0].content.clone(),
                error: None,
            }));
        }
    }
    
    // Try intelligent query for broader matches
    let results = state.knowledge_engine.intelligent_query(query);
    if !results.is_empty() {
        return Ok(Json(ChatResponse {
            response: results[0].content.clone(),
            error: None,
        }));
    }
    
    // Try to get top relevant results
    let relevant = state.knowledge_engine.get_top_relevant(query, 3);
    if !relevant.is_empty() {
        // Return the most relevant result
        return Ok(Json(ChatResponse {
            response: relevant[0].content.clone(),
            error: None,
        }));
    }
    
    // If still no results, provide helpful response
    let stats = state.knowledge_engine.get_stats();
    Ok(Json(ChatResponse {
        response: format!(
            "I don't have specific information about '{}' in my {} knowledge items. \
            Try asking about programming, science, mathematics, philosophy, or history!",
            query, stats.total_nodes
        ),
        error: None,
    }))
}