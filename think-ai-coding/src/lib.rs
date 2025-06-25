//! Think AI Coding - Code generation with O(1) performance

use thiserror::Error;

#[derive(Error, Debug)]
pub enum CodingError {
    #[error("Code generation error: {0}")]
    GenerationError(String),
}

pub type Result<T> = std::result::Result<T, CodingError>;