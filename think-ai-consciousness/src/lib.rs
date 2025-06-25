//! Think AI Consciousness - Functional consciousness framework

use thiserror::Error;

#[derive(Error, Debug)]
pub enum ConsciousnessError {
    #[error("Consciousness error: {0}")]
    ProcessingError(String),
}

pub type Result<T> = std::result::Result<T, ConsciousnessError>;