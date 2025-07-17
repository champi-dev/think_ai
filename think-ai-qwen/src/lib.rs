// Think AI Qwen Integration
//!
// Provides integration with Qwen AI models for text generation

pub mod client;
pub mod gemini;
pub use client::{QwenClient, QwenConfig, QwenRequest, QwenResponse};

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_config_default() {
        let config = QwenConfig::default();
        assert_eq!(config.base_url, "http://localhost:11434");
        assert_eq!(config.model, "qwen2.5:3b");
        assert!(config.api_key.is_none());
    }
}
