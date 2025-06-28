//! Chat handler for O(1) conversation interface

use axum::{
    extract::State,
    http::StatusCode,
    Json,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use crate::router::AppState;
use think_ai_knowledge::multi_candidate_selector::MultiCandidateSelector;

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
    
    // Use multi-candidate selection system to generate 10 different answers and select the best one
    let relevance_engine = state.knowledge_engine.get_intelligent_relevance();
    let multi_selector = MultiCandidateSelector::new(
        state.knowledge_engine.clone(),
        relevance_engine,
    );
    
    let best_answer = multi_selector.select_best_answer(query);
    
    // Format the response with Feynman-style explanation if applicable
    let formatted_response = if query.to_lowercase().contains("what is") || 
                               query.to_lowercase().contains("explain") ||
                               query.to_lowercase().contains("how does") {
        // Use Feynman explainer for conceptual queries
        let feynman_explanation = state.knowledge_engine.explain_concept(query);
        if !feynman_explanation.is_empty() && feynman_explanation.len() > best_answer.content.len() {
            feynman_explanation
        } else {
            best_answer.content
        }
    } else {
        best_answer.content
    };
    
    Ok(Json(ChatResponse {
        response: formatted_response,
        error: None,
    }))
}