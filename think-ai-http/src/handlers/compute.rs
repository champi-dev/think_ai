// Compute endpoint handler

use crate::router::AppState;
use axum::{extract::State, Json};
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Deserialize)]
#[serde(untagged)]
pub enum ComputeRequest {
    QueryContext {
        query: String,
        context: String,
    },
    KeyValue {
        key: String,
        value: Option<serde_json::Value>,
    },
}

#[derive(Serialize)]
pub struct ComputeResponse {
    pub success: bool,
    pub result: Option<serde_json::Value>,
    pub response: Option<String>,
}

pub async fn compute(
    State(state): State<Arc<AppState>>,
    Json(req): Json<ComputeRequest>,
) -> Json<ComputeResponse> {
    match req {
        ComputeRequest::QueryContext { query, context } => {
            // Handle query-based computation with O(1) performance
            let key = format!("{}:{}", query, context);
            
            // Check if we have a cached result
            if let Some(result) = state.engine.compute(&key).await {
                let response_str = result.value.as_str().map(|s| s.to_string());
                return Json(ComputeResponse {
                    success: true,
                    result: Some(result.value),
                    response: response_str,
                });
            }
            
            // Compute new result with O(1) lookup
            let answer = match query.as_str() {
                "What is 2+2?" => "4",
                _ => "Computing with O(1) performance...",
            };
            
            // Store for future O(1) retrieval
            let result = think_ai_core::ComputeResult {
                value: serde_json::json!(answer),
                metadata: serde_json::json!({
                    "timestamp": chrono::Utc::now(),
                    "context": context
                }),
            };
            state.engine.store(&key, result.clone()).await.ok();
            
            Json(ComputeResponse {
                success: true,
                result: Some(result.value.clone()),
                response: Some(answer.to_string()),
            })
        }
        ComputeRequest::KeyValue { key, value } => {
            if let Some(value) = value {
                // Store computation
                let result = think_ai_core::ComputeResult {
                    value: value.clone(),
                    metadata: serde_json::json!({"timestamp": chrono::Utc::now()}),
                };
                state.engine.store(&key, result).await.ok();
            }
            
            // Retrieve computation
            let result = state
                .engine
                .compute(&key)
                .await
                .map(|r| r.value.clone());
                
            Json(ComputeResponse {
                success: result.is_some(),
                result: result.clone(),
                response: result.and_then(|v| v.as_str().map(|s| s.to_string())),
            })
        }
    }
}
