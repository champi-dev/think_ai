// Vector search handler

use crate::router::AppState;
use axum::{extract::State, Json};
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Deserialize)]
pub struct SearchRequest {
    pub vector: Vec<f32>,
    pub k: usize,
}

#[derive(Serialize)]
pub struct SearchResponse {
    pub success: bool,
    pub results: Vec<SearchResult>,
}

#[derive(Serialize)]
pub struct SearchResult {
    pub index: usize,
    pub distance: f32,
    pub metadata: serde_json::Value,
}

pub async fn search(
    State(state): State<Arc<AppState>>,
    Json(req): Json<SearchRequest>,
) -> Json<SearchResponse> {
    match state.vector_index.search(req.vector, req.k) {
        Ok(results) => Json(SearchResponse {
            success: true,
            results: results
                .into_iter()
                .map(|r| SearchResult {
                    index: r.index,
                    distance: r.distance,
                    metadata: r.metadata,
                })
                .collect(),
        }),
        Err(_) => Json(SearchResponse {
            success: false,
            results: vec![],
        }),
    }
}
