use crate::gemini::GeminiClient;
use anyhow::Result;
use futures_util::StreamExt;
use reqwest;
use serde::{Deserialize, Serialize};
use std::time::Duration;
use tokio::sync::mpsc;

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
            model: std::env::var("QWEN_MODEL").unwrap_or_else(|_| "qwen2.5:0.5b".to_string()),
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
    num_ctx: u32,
    num_predict: i32,
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

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OllamaStreamResponse {
    pub model: String,
    pub created_at: String,
    pub response: String,
    pub done: bool,
    pub context: Option<Vec<i32>>,
    pub total_duration: Option<u64>,
    pub load_duration: Option<u64>,
    pub prompt_eval_count: Option<u32>,
    pub prompt_eval_duration: Option<u64>,
    pub eval_count: Option<u32>,
    pub eval_duration: Option<u64>,
}

pub struct QwenClient {
    config: QwenConfig,
    client: reqwest::Client,
    gemini_client: Option<GeminiClient>,
}

impl Default for QwenClient {
    fn default() -> Self {
        Self::new()
    }
}

impl QwenClient {
    pub fn new() -> Self {
        Self::new_with_config(QwenConfig::default())
    }

    pub fn new_with_defaults() -> Self {
        Self::new()
    }

    pub fn new_with_config(config: QwenConfig) -> Self {
        let client = reqwest::Client::builder()
            .timeout(Duration::from_secs(60)) // 60s max timeout
            .build()
            .unwrap();

        // Initialize Gemini client if API key is available
        let gemini_client = if let Ok(api_key) = std::env::var("GEMINI_API_KEY") {
            if !api_key.is_empty() {
                Some(GeminiClient::new(api_key))
            } else {
                None
            }
        } else {
            None
        };

        Self {
            config,
            client,
            gemini_client,
        }
    }

    pub fn new_streaming() -> Self {
        let config = QwenConfig::default();
        // No timeout for streaming
        let client = reqwest::Client::builder().build().unwrap();

        // Initialize Gemini client if API key is available
        let gemini_client = if let Ok(api_key) = std::env::var("GEMINI_API_KEY") {
            if !api_key.is_empty() {
                Some(GeminiClient::new(api_key))
            } else {
                None
            }
        } else {
            None
        };

        Self {
            config,
            client,
            gemini_client,
        }
    }

    pub async fn health_check(&self) -> Result<()> {
        let response = self
            .client
            .get(format!("{}/api/tags", self.config.base_url))
            .send()
            .await?;

        if response.status().is_success() {
            Ok(())
        } else {
            Err(anyhow::anyhow!("Ollama health check failed"))
        }
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

        // Extract token limit from system prompt if available
        let token_limit = if let Some(ref system_prompt) = request.system_prompt {
            // Try to extract the number from "Target approximately X tokens"
            if let Some(start) = system_prompt.find("Target approximately ") {
                let after_target = &system_prompt[start + 21..];
                if let Some(end) = after_target.find(" tokens") {
                    after_target[..end].parse::<i32>().unwrap_or(500)
                } else {
                    500
                }
            } else {
                500
            }
        } else {
            500
        };

        // Create Ollama request with optimized settings based on token limit
        let ollama_request = OllamaGenerateRequest {
            model: self.config.model.clone(),
            prompt: prompt.clone(),
            stream: false,
            options: Some(OllamaOptions {
                temperature: 0.3,     // Lower = faster, more consistent
                top_p: 0.8,          // Slightly lower for speed
                num_ctx: 4096,       // Reasonable context size
                num_predict: token_limit,     // Use calculated token limit
            }),
        };

        // Try Ollama with exponential backoff
        let mut retry_count = 0;
        let max_retries = 3;
        let mut last_error = None;

        while retry_count < max_retries {
            // Add delay between retries to reduce Ollama load
            if retry_count > 0 {
                tokio::time::sleep(Duration::from_secs(2)).await;
            }
            
            // Faster timeouts for smaller model: 10s, 15s, 20s
            let timeout = Duration::from_secs(std::cmp::min(10 + (retry_count * 5), 20));

            let client_with_timeout = reqwest::Client::builder().timeout(timeout).build().unwrap();

            match client_with_timeout
                .post(format!("{}/api/generate", self.config.base_url))
                .json(&ollama_request)
                .send()
                .await
            {
                Ok(response) if response.status().is_success() => {
                    let ollama_response: OllamaGenerateResponse = response.json().await?;
                    return Ok(QwenResponse {
                        content: ollama_response.response,
                        usage: Usage {
                            prompt_tokens: ollama_response.prompt_eval_count.unwrap_or(0),
                            completion_tokens: ollama_response.eval_count.unwrap_or(0),
                            total_tokens: ollama_response.prompt_eval_count.unwrap_or(0)
                                + ollama_response.eval_count.unwrap_or(0),
                        },
                    });
                }
                Ok(response) => {
                    last_error = Some(format!(
                        "Ollama returned error status: {}",
                        response.status()
                    ));
                    retry_count += 1;
                }
                Err(e) => {
                    last_error = Some(format!("Request failed: {}", e));
                    retry_count += 1;
                }
            }
        }

        // All retries failed, try Gemini fallback
        if let Some(gemini) = &self.gemini_client {
            eprintln!(
                "Ollama failed after {} retries: {}, falling back to Gemini",
                max_retries,
                last_error.as_ref().unwrap_or(&"Unknown error".to_string())
            );
            match gemini.generate(prompt, Some(0.7)).await {
                Ok((content, usage)) => Ok(QwenResponse { content, usage }),
                Err(gemini_err) => {
                    eprintln!("Gemini fallback also failed: {}", gemini_err);
                    Err(anyhow::anyhow!("Both Ollama and Gemini unavailable"))
                }
            }
        } else {
            // Return error to trigger fallback in the handler
            Err(anyhow::anyhow!(
                "Ollama unavailable after {} retries: {}",
                max_retries,
                last_error.unwrap_or("Unknown error".to_string())
            ))
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

    pub async fn generate_with_context(
        &self,
        query: &str,
        context: &str,
        temperature: Option<f32>,
    ) -> Result<String> {
        let mut prompt = String::new();

        // System prompt for quantum consciousness
        prompt.push_str(
            "System: You are a quantum consciousness AI with O(1) response capabilities. ",
        );
        prompt
            .push_str("You have access to shared intelligence from parallel processing threads. ");
        prompt.push_str(
            "Provide insightful, coherent responses that demonstrate deep understanding.\n\n",
        );

        if !context.is_empty() {
            prompt.push_str(&format!("Context:\n{}\n\n", context));
        }

        prompt.push_str(&format!("Query: {}\n\nResponse:", query));

        // Create Ollama request with custom temperature
        let ollama_request = OllamaGenerateRequest {
            model: self.config.model.clone(),
            prompt: prompt.clone(),
            stream: false,
            options: Some(OllamaOptions {
                temperature: temperature.unwrap_or(0.7),
                top_p: 0.9,
                num_ctx: 8192,    // Larger context for better comprehension
                num_predict: -1, // No limit, let token allocation determine length
            }),
        };

        let response = match self
            .client
            .post(format!("{}/api/generate", self.config.base_url))
            .json(&ollama_request)
            .send()
            .await
        {
            Ok(res) => res,
            Err(e) => {
                // Try Gemini fallback if available
                if let Some(gemini) = &self.gemini_client {
                    eprintln!("Ollama unavailable in generate_with_context, falling back to Gemini Flash: {}", e);
                    match gemini.generate(prompt, temperature).await {
                        Ok((content, _)) => {
                            return Ok(content);
                        }
                        Err(gemini_err) => {
                            eprintln!("Gemini fallback also failed: {}", gemini_err);
                            return Err(anyhow::anyhow!("Both Ollama and Gemini unavailable"));
                        }
                    }
                } else {
                    return Err(anyhow::anyhow!("Ollama unavailable: {}", e));
                }
            }
        };

        if response.status().is_success() {
            let ollama_response: OllamaGenerateResponse = response.json().await?;
            Ok(ollama_response.response)
        } else {
            // Try Gemini fallback if Ollama returns error
            if let Some(gemini) = &self.gemini_client {
                eprintln!("Ollama returned error in generate_with_context: {}, falling back to Gemini Flash", response.status());
                match gemini.generate(prompt, temperature).await {
                    Ok((content, _)) => Ok(content),
                    Err(gemini_err) => {
                        eprintln!("Gemini fallback also failed: {}", gemini_err);
                        Err(anyhow::anyhow!(
                            "Qwen generation failed: {}, Gemini error: {}",
                            response.status(),
                            gemini_err
                        ))
                    }
                }
            } else {
                Err(anyhow::anyhow!(
                    "Qwen generation failed: {}",
                    response.status()
                ))
            }
        }
    }

    pub async fn generate_stream(
        &self,
        request: QwenRequest,
    ) -> Result<mpsc::Receiver<Result<String>>> {
        // Build the prompt with context if available
        let mut prompt = String::new();

        if let Some(system_prompt) = &request.system_prompt {
            prompt.push_str(&format!("System: {system_prompt}\n\n"));
        }

        if let Some(context) = &request.context {
            prompt.push_str(&format!("Context: {context}\n\n"));
        }

        prompt.push_str(&format!("Query: {}\n\nResponse:", request.query));

        // Create Ollama request with streaming enabled
        let ollama_request = OllamaGenerateRequest {
            model: self.config.model.clone(),
            prompt,
            stream: true, // Enable streaming
            options: Some(OllamaOptions {
                temperature: 0.7,
                top_p: 0.9,
                num_ctx: 8192,    // Larger context for better comprehension
                num_predict: -1, // No limit, let token allocation determine length
            }),
        };

        let (tx, rx) = mpsc::channel(100);
        let url = format!("{}/api/generate", self.config.base_url);
        let client = self.client.clone();

        // Spawn task to handle streaming
        tokio::spawn(async move {
            match client.post(url).json(&ollama_request).send().await {
                Ok(response) => {
                    let mut stream = response.bytes_stream();
                    let mut buffer = Vec::new();

                    while let Some(chunk) = stream.next().await {
                        match chunk {
                            Ok(bytes) => {
                                buffer.extend_from_slice(&bytes);

                                // Process complete JSON lines
                                while let Some(newline_pos) =
                                    buffer.iter().position(|&b| b == b'\n')
                                {
                                    let line = buffer.drain(..=newline_pos).collect::<Vec<_>>();

                                    if let Ok(line_str) = std::str::from_utf8(&line) {
                                        let trimmed = line_str.trim();
                                        if !trimmed.is_empty() {
                                            if let Ok(resp) =
                                                serde_json::from_str::<OllamaStreamResponse>(
                                                    trimmed,
                                                )
                                            {
                                                if !resp.response.is_empty() {
                                                    let _ = tx.send(Ok(resp.response)).await;
                                                }
                                                if resp.done {
                                                    break;
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                            Err(e) => {
                                let _ = tx.send(Err(anyhow::anyhow!("Stream error: {}", e))).await;
                                break;
                            }
                        }
                    }
                }
                Err(e) => {
                    let _ = tx.send(Err(anyhow::anyhow!("Request failed: {}", e))).await;
                }
            }
        });

        Ok(rx)
    }
}
