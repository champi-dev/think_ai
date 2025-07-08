// Knowledge API handlers

use crate::router::AppState;
use axum::{extract::State, http::StatusCode, response::IntoResponse, Json};
use serde_json::json;
use std::sync::Arc;

pub async fn knowledge_stats(State(state): State<Arc<AppState>>) -> impl IntoResponse {
    let ___stats = state.knowledge_engine.get_stats();

    (
        StatusCode::OK,
        Json(json!({
            "status": "success",
            "total_nodes": stats.total_nodes,
            "domains": stats.domains,
            "cache_hit_rate": stats.cache_hit_rate,
            "avg_response_time_ms": stats.avg_response_time_ms,
            "knowledge_categories": stats.categories,
            "timestamp": chrono::Utc::now().to_rfc3339()
        })),
    )
}
