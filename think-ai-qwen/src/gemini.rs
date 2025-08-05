use anyhow::Result;
use reqwest;
use serde::{Deserialize, Serialize};
use std::time::Duration;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GeminiConfig {
    pub api_key: String,
    pub base_url: String,
    pub model: String,
}

impl Default for GeminiConfig {
    fn default() -> Self {
        Self {
            api_key: std::env::var("GEMINI_API_KEY").unwrap_or_default(),
            base_url: "https://generativelanguage.googleapis.com/v1beta".to_string(),
            model: "gemini-2.0-flash-exp".to_string(),
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct GeminiRequest {
    contents: Vec<Content>,
    generation_config: Option<GenerationConfig>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Content {
    parts: Vec<Part>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Part {
    text: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct GenerationConfig {
    temperature: f32,
    top_p: f32,
    max_output_tokens: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct GeminiResponse {
    candidates: Vec<Candidate>,
    usage_metadata: Option<UsageMetadata>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Candidate {
    content: Content,
    finish_reason: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct UsageMetadata {
    prompt_token_count: u32,
    candidates_token_count: u32,
    total_token_count: u32,
}

pub struct GeminiClient {
    config: GeminiConfig,
    #[allow(dead_code)]
    client: reqwest::Client,
}

impl GeminiClient {
    pub fn new(api_key: String) -> Self {
        let config = GeminiConfig {
            api_key,
            ..Default::default()
        };

        let client = reqwest::Client::builder()
            .timeout(Duration::from_secs(30)) // 30s max timeout for Gemini
            .build()
            .unwrap();

        Self { config, client }
    }

    pub fn new_with_config(config: GeminiConfig) -> Self {
        let client = reqwest::Client::builder()
            .timeout(Duration::from_secs(30)) // 30s max timeout for Gemini
            .build()
            .unwrap();

        Self { config, client }
    }

    pub async fn generate(
        &self,
        prompt: String,
        temperature: Option<f32>,
    ) -> Result<(String, crate::client::Usage)> {
        let request = GeminiRequest {
            contents: vec![Content {
                parts: vec![Part { text: prompt }],
            }],
            generation_config: Some(GenerationConfig {
                temperature: temperature.unwrap_or(0.7),
                top_p: 0.9,
                max_output_tokens: 2048,
            }),
        };

        let url = format!(
            "{}/models/{}:generateContent?key={}",
            self.config.base_url, self.config.model, self.config.api_key
        );

        // Try with exponential backoff
        let mut retry_count = 0;
        let max_retries = 3;
        let mut last_error = None;

        while retry_count < max_retries {
            // Exponential backoff: 10s, 20s, 30s (max)
            let timeout = Duration::from_secs(std::cmp::min(10 * (1 << retry_count), 30));

            let client_with_timeout = reqwest::Client::builder().timeout(timeout).build().unwrap();

            match client_with_timeout.post(&url).json(&request).send().await {
                Ok(response) if response.status().is_success() => {
                    let gemini_response: GeminiResponse = response.json().await?;

                    if let Some(candidate) = gemini_response.candidates.first() {
                        if let Some(part) = candidate.content.parts.first() {
                            let content = part.text.clone();

                            let usage = if let Some(usage_metadata) = gemini_response.usage_metadata
                            {
                                crate::client::Usage {
                                    prompt_tokens: usage_metadata.prompt_token_count,
                                    completion_tokens: usage_metadata.candidates_token_count,
                                    total_tokens: usage_metadata.total_token_count,
                                }
                            } else {
                                crate::client::Usage {
                                    prompt_tokens: 0,
                                    completion_tokens: 0,
                                    total_tokens: 0,
                                }
                            };

                            return Ok((content, usage));
                        }
                    }

                    last_error = Some("No response content from Gemini".to_string());
                    retry_count += 1;
                }
                Ok(response) => {
                    let error_text = response
                        .text()
                        .await
                        .unwrap_or_else(|_| "Unknown error".to_string());
                    last_error = Some(format!("Gemini API error: {}", error_text));
                    retry_count += 1;
                }
                Err(e) => {
                    last_error = Some(format!("Request failed: {}", e));
                    retry_count += 1;
                }
            }
        }

        Err(anyhow::anyhow!(
            "Gemini failed after {} retries: {}",
            max_retries,
            last_error.unwrap_or("Unknown error".to_string())
        ))
    }
}
