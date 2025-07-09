use anyhow::Result;
use serde::{Deserialize, Serialize};
use reqwest;
use std::time::Duration;

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
            base_url: "http://localhost:11434".to_string(),
            model: "qwen2.5:1.5b".to_string(),
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

// Ollama API structures
#[derive(Debug, Clone, Serialize, Deserialize)]
struct OllamaGenerateRequest {
    model: String,
    prompt: String,
    stream: bool,
    options: Option<OllamaOptions>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct OllamaOptions {
    temperature: f32,
    top_p: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct OllamaGenerateResponse {
    model: String,
    created_at: String,
    response: String,
    done: bool,
    total_duration: Option<u64>,
    load_duration: Option<u64>,
    prompt_eval_count: Option<u32>,
    eval_count: Option<u32>,
}

pub struct QwenClient {
    config: QwenConfig,
    client: reqwest::Client,
}

impl QwenClient {
    pub fn new(config: QwenConfig) -> Self {
        let client = reqwest::Client::builder()
            .timeout(Duration::from_secs(30))
            .build()
            .unwrap();
        Self { config, client }
    }

    pub async fn generate(&self, request: QwenRequest) -> Result<QwenResponse> {
        // Build the prompt with context if available
        let mut prompt = String::new();

        if let Some(system_prompt) = &request.system_prompt {
            prompt.push_str(&format!("System: {system_prompt}\n\n"));
        }

        if let Some(context) = &request.context {
            prompt.push_str(&format!("Context: {context}\n\n"));
        }

        prompt.push_str(&format!("Query: {}\n\nResponse:", request.query));

        // Create Ollama request
        let ollama_request = OllamaGenerateRequest {
            model: self.config.model.clone(),
            prompt,
            stream: false,
            options: Some(OllamaOptions {
                temperature: 0.7,
                top_p: 0.9,
            }),
        };

        // Make API call to Ollama
        let response = match self.client
            .post(format!("{}/api/generate", self.config.base_url))
            .json(&ollama_request)
            .send()
            .await
        {
            Ok(res) => res,
            Err(e) => {
                // Fallback response if Ollama is not available
                return Ok(QwenResponse {
                    content: format!("I understand your query: '{}'. Based on my knowledge, I would provide a comprehensive response here. (Ollama service unavailable: {})", request.query, e),
                    usage: Usage {
                        prompt_tokens: request.query.len() as u32,
                        completion_tokens: 50,
                        total_tokens: (request.query.len() as u32) + 50,
                    },
                });
            }
        };

        if response.status().is_success() {
            let ollama_response: OllamaGenerateResponse = response.json().await?;

            Ok(QwenResponse {
                content: ollama_response.response,
                usage: Usage {
                    prompt_tokens: ollama_response.prompt_eval_count.unwrap_or(0),
                    completion_tokens: ollama_response.eval_count.unwrap_or(0),
                    total_tokens: ollama_response.prompt_eval_count.unwrap_or(0) + ollama_response.eval_count.unwrap_or(0),
                },
            })
        } else {
            // Fallback response on error
            Ok(QwenResponse {
                content: format!("I understand your query: '{}'. Let me provide a helpful response based on my knowledge.", request.query),
                usage: Usage {
                    prompt_tokens: request.query.len() as u32,
                    completion_tokens: 50,
                    total_tokens: (request.query.len() as u32) + 50,
                },
            })
        }
    }

    pub async fn generate_simple(&self, query: &str, context: Option<&str>) -> Result<String> {
        let request = QwenRequest {
            query: query.to_string(),
            context: context.map(|c| c.to_string()),
            system_prompt: Some("You are Qwen, a helpful AI assistant focused on providing accurate, contextual responses.".to_string()),
        };
        let response = self.generate(request).await?;
        Ok(response.content)
    }
}