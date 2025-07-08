//! Compute endpoint handler

use axum::{extract::State, Json};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use crate::router::AppState;

#[derive(Deserialize)]
pub struct ComputeRequest {
    pub key: String,
    pub value: Option<serde_json::Value>,
}

#[derive(Serialize)]
pub struct ComputeResponse {
    pub success: bool,
    pub result: Option<serde_json::Value>,
}

pub async fn compute(
    State(state): State<Arc<AppState>>,
    Json(req): Json<ComputeRequest>,
) -> Json<ComputeResponse> {
    if let Some(value) = req.value {
        // Store computation
        let result = think_ai_core::ComputeResult {
            value: value.clone(),
            metadata: serde_json::json!({"timestamp": chrono::Utc::now()}),
        };
        state.engine.store(&req.key, result).await.ok();
    }
    
    // Retrieve computation
    let result = state.engine.compute(&req.key).await
        .map(|r| r.value.clone());
    
    Json(ComputeResponse {
        success: result.is_some(),
        result,
    })
}