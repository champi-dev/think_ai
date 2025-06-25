//! Statistics handler

use axum::{extract::State, Json};
use serde_json::json;
use std::sync::Arc;
use crate::router::AppState;

pub async fn stats(
    State(state): State<Arc<AppState>>,
) -> Json<serde_json::Value> {
    let engine_stats = state.engine.stats();
    let vector_count = state.vector_index.len();
    
    Json(json!({
        "engine": {
            "initialized": engine_stats.initialized,
            "operations": engine_stats.operation_count,
            "cache_size": engine_stats.cache_size,
        },
        "vector_index": {
            "count": vector_count,
        }
    }))
}