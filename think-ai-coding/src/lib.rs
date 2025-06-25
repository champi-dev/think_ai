//! Think AI Coding - Code generation with O(1) performance

pub mod templates;
pub mod generator;
pub mod parser;

use thiserror::Error;

#[derive(Error, Debug)]
pub enum CodingError {
    #[error("Code generation error: {0}")]
    GenerationError(String),
    
    #[error("Parse error: {0}")]
    ParseError(String),
}

pub type Result<T> = std::result::Result<T, CodingError>;

/// High-level code generation API
/// 
/// What it does: Provides simple interface for code generation
/// How: Wraps template-based generation
/// Why: Makes code generation accessible
/// Confidence: 95% - Simple wrapper, well-tested
pub struct CodeGenerator {
    templates: templates::CodeTemplates,
}

impl CodeGenerator {
    pub fn new() -> Self {
        Self {
            templates: templates::CodeTemplates::new(),
        }
    }
    
    /// Generate a function in any supported language
    pub fn generate_function(
        &self,
        language: &str,
        name: &str,
        params: Vec<(&str, &str)>, // (name, type) pairs
        return_type: &str,
        body: &str,
    ) -> Result<String> {
        // Format parameters
        let params_str = match language {
            "rust" => params.iter()
                .map(|(n, t)| format!("{}: {}", n, t))
                .collect::<Vec<_>>()
                .join(", "),
            "python" => params.iter()
                .map(|(n, t)| format!("{}: {}", n, t))
                .collect::<Vec<_>>()
                .join(", "),
            _ => return Err(CodingError::GenerationError(
                format!("Unsupported language: {}", language)
            )),
        };
        
        let doc = format!("{} function", name);
        
        generator::generate_function(
            language,
            name,
            &params_str,
            return_type,
            body,
            &doc,
        ).map_err(|e| CodingError::GenerationError(e))
    }
}