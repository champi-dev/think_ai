// Think AI LLM - True Language Model Integration
//!
// # Making Think AI a Real LLM
// This module adds actual text generation capabilities while maintaining
// O(1) performance for cached responses.
// # How It Works
// 1. Check O(1) cache for exact query match
// 2. If not found, generate with small LLM
// 3. Cache the response for future O(1) access
// 4. Return to user

pub mod model;
pub mod tokenizer;
pub mod generator;
pub mod cache;
pub mod hybrid_engine;
pub use model::LLMModel;
pub use tokenizer::Tokenizer;
pub use generator::{GenerationConfig, TextGenerator};
pub use cache::O1ResponseCache;
pub use hybrid_engine::HybridLLMEngine;
/// Result type for LLM operations
pub type Result<T> = std::result::Result<T, Box<dyn std::error::Error + Send + Sync>>;
/// LLM response with metadata
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct LLMResponse {
    /// Generated text
    pub text: String,
    /// Was this from cache? (O(1))
    pub from_cache: bool,
    /// Generation time in milliseconds
    pub generation_time_ms: u64,
    /// Model used
    pub model: String,
    /// Confidence score
    pub confidence: f32,
}
