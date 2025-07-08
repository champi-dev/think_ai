//! Qwen AI Client Implementation

use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum QwenError {
    #[error("Request failed: {0}")]
    RequestFailed(String),
    
    #[error("Invalid response: {0}")]
    InvalidResponse(String),
    
    #[error("API error: {0}")]
    ApiError(String),
}

pub type Result<T> = std::result::Result<T, QwenError>;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QwenConfig {
    pub model: String,
    pub temperature: f32,
    pub max_tokens: usize,
}

impl Default for QwenConfig {
    fn default() -> Self {
        Self {
            model: "qwen2.5:1.5b".to_string(),
            temperature: 0.7,
            max_tokens: 2048,
        }
    }
}

#[derive(Debug, Serialize, Deserialize)]
pub struct QwenRequest {
    pub query: String,
    pub context: Option<String>,
    pub system_prompt: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct QwenResponse {
    pub content: String,
    pub model: String,
    pub usage: Option<Usage>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Usage {
    pub prompt_tokens: usize,
    pub completion_tokens: usize,
    pub total_tokens: usize,
}

pub struct QwenClient {
    config: QwenConfig,
}

impl QwenClient {
    pub fn new(config: QwenConfig) -> Self {
        Self { config }
    }
    
    pub fn new_with_defaults() -> Self {
        Self {
            config: QwenConfig::default(),
        }
    }
    
    pub async fn generate(&self, request: QwenRequest) -> Result<QwenResponse> {
        // For now, return a mock response to avoid external dependencies
        // In production, this would call the actual Qwen API
        
        let prompt = format!(
            "{}\n{}\nQuery: {}",
            request.system_prompt.unwrap_or_default(),
            request.context.unwrap_or_default(),
            request.query
        );
        
        // Mock response for development
        let response = QwenResponse {
            content: format!("Response to: {}", request.query),
            model: self.config.model.clone(),
            usage: Some(Usage {
                prompt_tokens: prompt.len() / 4,
                completion_tokens: 50,
                total_tokens: prompt.len() / 4 + 50,
            }),
        };
        
        Ok(response)
    }
    
    pub async fn generate_simple(&self, query: &str, context: Option<&str>) -> Result<String> {
        let request = QwenRequest {
            query: query.to_string(),
            context: context.map(|c| c.to_string()),
            system_prompt: None,
        };
        
        let response = self.generate(request).await?;
        Ok(response.content)
    }
}