// Health check handler

use axum::Json;
use serde_json::json;

pub async fn health() -> Json<serde_json::Value> {
    Json(json!({
        "status": "healthy",
        "service": "think-ai",
        "version": "0.1.0"
    }))
}
