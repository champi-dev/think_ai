// Core types for Think AI

use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum CoreError {
    #[error("Initialization failed: {0}")]
    InitializationError(String),

    #[error("Operation failed: {0}")]
    OperationError(String),
}

pub type Result<T> = std::result::Result<T, CoreError>;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ComputeResult {
    pub value: serde_json::Value,
    pub metadata: serde_json::Value,
}

#[derive(Debug, Serialize)]
pub struct EngineStats {
    pub initialized: bool,
    pub operation_count: u64,
    pub cache_size: usize,
}
