//! Types for vector search

use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum VectorError {
    #[error("Dimension mismatch: expected {expected}, got {actual}")]
    DimensionMismatch { expected: usize, actual: usize },
    
    #[error("Invalid configuration: {0}")]
    InvalidConfig(String),
    
    #[error("Vector not found")]
    NotFound,
}

pub type Result<T> = std::result::Result<T, VectorError>;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LSHConfig {
    pub dimension: usize,
    pub num_hash_tables: usize,
    pub num_hash_functions: usize,
    pub seed: u64,
}

impl Default for LSHConfig {
    fn default() -> Self {
        Self {
            dimension: 384,
            num_hash_tables: 10,
            num_hash_functions: 8,
            seed: 42,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SearchResult {
    pub index: usize,
    pub distance: f32,
    pub vector: Vec<f32>,
    pub metadata: serde_json::Value,
}