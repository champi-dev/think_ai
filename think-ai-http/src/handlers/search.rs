// Vector search handler

use crate::router::AppState;
use axum::{extract::State, Json};
use serde::{Deserialize, Serialize};
use std::sync::Arc;

#[derive(Deserialize)]
#[serde(untagged)]
pub enum SearchRequest {
    TextQuery {
        query: String,
        limit: Option<usize>,
    },
    VectorQuery {
        vector: Vec<f32>,
        k: usize,
    },
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
    match req {
        SearchRequest::TextQuery { query, limit } => {
            // Convert text query to vector using simple hash-based embedding
            let mut vector = vec![0.0f32; 128]; // Standard embedding size
            for (i, ch) in query.chars().enumerate() {
                vector[i % 128] += ch as u32 as f32 / 1000.0;
            }
            
            // Normalize vector
            let norm: f32 = vector.iter().map(|x| x * x).sum::<f32>().sqrt();
            if norm > 0.0 {
                for v in &mut vector {
                    *v /= norm;
                }
            }
            
            let k = limit.unwrap_or(5);
            match state.vector_index.search(vector, k) {
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
        SearchRequest::VectorQuery { vector, k } => {
            match state.vector_index.search(vector, k) {
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
    }
}
