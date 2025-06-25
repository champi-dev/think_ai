//! O(1) router implementation

use axum::{Router, routing::{get, post}};
use std::sync::Arc;
use crate::handlers;

pub struct AppState {
    pub engine: Arc<think_ai_core::O1Engine>,
    pub vector_index: Arc<think_ai_vector::O1VectorIndex>,
}

pub fn create_router(state: Arc<AppState>) -> Router {
    Router::new()
        .route("/health", get(handlers::health))
        .route("/compute", post(handlers::compute))
        .route("/search", post(handlers::search))
        .route("/stats", get(handlers::stats))
        .with_state(state)
}