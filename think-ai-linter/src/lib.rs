//! Think AI O(1) Linter - Performance-focused code analyzer

pub mod rules;
pub mod analyzer;
pub mod fixer;
pub mod cache;

use thiserror::Error;

#[derive(Error, Debug)]
pub enum LintError {
    #[error("Parse error: {0}")]
    ParseError(String),
    
    #[error("Analysis error: {0}")]
    AnalysisError(String),
    
    #[error("Fix error: {0}")]
    FixError(String),
    
    #[error("IO error: {0}")]
    IoError(#[from] std::io::Error),
}

pub type Result<T> = std::result::Result<T, LintError>;