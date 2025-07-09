use anyhow::Result;
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QwenConfig {
    pub api_key: Option<String>,
    pub base_url: String,
    pub model: String,
}
impl Default for QwenConfig {
    fn default() -> Self {
        Self {
            api_key: None,
            base_url: "https://api.qwen.ai".to_string(),
            model: "qwen-turbo".to_string(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QwenRequest {
    pub query: String,
    pub context: Option<String>,
    pub system_prompt: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QwenResponse {
    pub content: String,
    pub usage: Usage,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Usage {
    pub prompt_tokens: u32,
    pub completion_tokens: u32,
    pub total_tokens: u32,
}

pub struct QwenClient {
    config: QwenConfig,
}

impl QwenClient {
    pub fn new(config: QwenConfig) -> Self {
        Self { config }
    }

    pub async fn generate(&self, request: QwenRequest) -> Result<QwenResponse> {
        // Simulate a response for now
        let response = QwenResponse {
            content: format!(
                "Response to: {} (model: {})",
                request.query, self.config.model
            ),
            usage: Usage {
                prompt_tokens: 10,
                completion_tokens: 20,
                total_tokens: 30,
            },
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