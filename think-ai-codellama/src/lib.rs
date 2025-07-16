// CodeLlama Integration for Think AI - O(1) performance with local Ollama

use anyhow::{anyhow, Result};
use async_trait::async_trait;
use futures::StreamExt;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::{Duration, Instant};
use tracing::info;

/// Configuration for CodeLlama client
#[derive(Debug, Clone)]
pub struct CodeLlamaConfig {
    /// Ollama API endpoint
    pub endpoint: String,
    /// Model to use (e.g., "codellama:7b", "codellama:13b")
    pub model: String,
    /// Request timeout
    pub timeout: Duration,
    /// Maximum tokens to generate
    pub max_tokens: usize,
    /// Temperature for generation
    pub temperature: f32,
    /// Enable response caching for O(1) performance
    pub enable_cache: bool,
}

impl Default for CodeLlamaConfig {
    fn default() -> Self {
        Self {
            endpoint: "http://localhost:11434".to_string(),
            model: "codellama:7b".to_string(),
            timeout: Duration::from_secs(30),
            max_tokens: 2048,
            temperature: 0.1, // Lower temperature for more deterministic code generation
            enable_cache: true,
        }
    }
}

/// Request structure for Ollama API
#[derive(Debug, Serialize)]
struct OllamaRequest {
    model: String,
    prompt: String,
    stream: bool,
    options: OllamaOptions,
}

#[derive(Debug, Serialize)]
struct OllamaOptions {
    temperature: f32,
    num_predict: i32,
}

/// Response structure from Ollama API
#[derive(Debug, Deserialize)]
struct OllamaResponse {
    response: String,
    done: bool,
    context: Option<Vec<i32>>,
    total_duration: Option<i64>,
    prompt_eval_duration: Option<i64>,
}

/// Streaming response chunk
#[derive(Debug, Deserialize)]
struct OllamaStreamChunk {
    response: String,
    done: bool,
}

/// Performance metrics for O(1) optimization
#[derive(Debug, Clone)]
pub struct PerformanceMetrics {
    pub cache_hits: usize,
    pub cache_misses: usize,
    pub average_response_time_ms: f64,
    pub total_requests: usize,
}

/// Main CodeLlama client with O(1) caching
pub struct CodeLlamaClient {
    config: CodeLlamaConfig,
    client: reqwest::Client,
    /// O(1) response cache using hash map
    cache: tokio::sync::RwLock<HashMap<u64, String>>,
    /// Performance tracking
    metrics: tokio::sync::RwLock<PerformanceMetrics>,
}

impl CodeLlamaClient {
    /// Create new CodeLlama client with default configuration
    pub fn new() -> Result<Self> {
        Self::with_config(CodeLlamaConfig::default())
    }

    /// Create new CodeLlama client with custom configuration
    pub fn with_config(config: CodeLlamaConfig) -> Result<Self> {
        let client = reqwest::Client::builder().timeout(config.timeout).build()?;

        Ok(Self {
            config,
            client,
            cache: tokio::sync::RwLock::new(HashMap::new()),
            metrics: tokio::sync::RwLock::new(PerformanceMetrics {
                cache_hits: 0,
                cache_misses: 0,
                average_response_time_ms: 0.0,
                total_requests: 0,
            }),
        })
    }

    /// Hash function for O(1) cache lookup
    fn hash_prompt(&self, prompt: &str) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};

        let mut hasher = DefaultHasher::new();
        prompt.hash(&mut hasher);
        self.config.model.hash(&mut hasher);
        hasher.finish()
    }

    /// Check if the model is available
    pub async fn check_model_availability(&self) -> Result<bool> {
        let url = format!("{}/api/tags", self.config.endpoint);

        let response = self.client.get(&url).send().await?;

        if !response.status().is_success() {
            return Ok(false);
        }

        #[derive(Deserialize)]
        struct ModelList {
            models: Vec<Model>,
        }

        #[derive(Deserialize)]
        struct Model {
            name: String,
        }

        let models: ModelList = response.json().await?;
        Ok(models
            .models
            .iter()
            .any(|m| m.name.starts_with("codellama")))
    }

    /// Generate code with O(1) cached responses when possible
    pub async fn generate_code(&self, prompt: &str) -> Result<String> {
        let start_time = Instant::now();

        // O(1) cache lookup
        if self.config.enable_cache {
            let cache_key = self.hash_prompt(prompt);
            let cache = self.cache.read().await;
            if let Some(cached_response) = cache.get(&cache_key) {
                // Update metrics
                let mut metrics = self.metrics.write().await;
                metrics.cache_hits += 1;
                metrics.total_requests += 1;

                info!("Cache hit for prompt (O(1) performance)");
                return Ok(cached_response.clone());
            }
        }

        // Cache miss - generate new response
        info!("Generating new code response with CodeLlama");

        let request = OllamaRequest {
            model: self.config.model.clone(),
            prompt: format!(
                "You are an expert programmer. Generate ONLY raw code as output. No explanations, no markdown formatting, just pure executable code with comments. The code should be clean, efficient, and well-commented.\n\nRequest: {}\n\nCode:",
                prompt
            ),
            stream: false,
            options: OllamaOptions {
                temperature: self.config.temperature,
                num_predict: self.config.max_tokens as i32,
            },
        };

        let url = format!("{}/api/generate", self.config.endpoint);
        let response = self.client.post(&url).json(&request).send().await?;

        if !response.status().is_success() {
            let error_text = response.text().await?;
            return Err(anyhow!("CodeLlama API error: {}", error_text));
        }

        let ollama_response: OllamaResponse = response.json().await?;
        let generated_code = ollama_response.response;

        // Cache the response for O(1) future lookups
        if self.config.enable_cache {
            let cache_key = self.hash_prompt(prompt);
            let mut cache = self.cache.write().await;
            cache.insert(cache_key, generated_code.clone());
        }

        // Update metrics
        let elapsed_ms = start_time.elapsed().as_millis() as f64;
        let mut metrics = self.metrics.write().await;
        metrics.cache_misses += 1;
        metrics.total_requests += 1;
        metrics.average_response_time_ms =
            (metrics.average_response_time_ms * (metrics.total_requests - 1) as f64 + elapsed_ms)
                / metrics.total_requests as f64;

        Ok(generated_code)
    }

    /// Generate code with streaming response
    pub async fn generate_code_stream(
        &self,
        prompt: &str,
    ) -> Result<impl futures::Stream<Item = Result<String>>> {
        let request = OllamaRequest {
            model: self.config.model.clone(),
            prompt: format!(
                "You are an expert programmer. Generate clean, efficient, and well-commented code.\n\n{}",
                prompt
            ),
            stream: true,
            options: OllamaOptions {
                temperature: self.config.temperature,
                num_predict: self.config.max_tokens as i32,
            },
        };

        let url = format!("{}/api/generate", self.config.endpoint);
        let response = self.client.post(&url).json(&request).send().await?;

        if !response.status().is_success() {
            let error_text = response.text().await?;
            return Err(anyhow!("CodeLlama API error: {}", error_text));
        }

        let stream = response.bytes_stream().map(|chunk| {
            chunk
                .map_err(|e| anyhow!("Stream error: {}", e))
                .and_then(|bytes| {
                    let text = String::from_utf8_lossy(&bytes);
                    serde_json::from_str::<OllamaStreamChunk>(&text)
                        .map(|chunk| chunk.response)
                        .map_err(|e| anyhow!("Parse error: {}", e))
                })
        });

        Ok(stream)
    }

    /// Get performance metrics
    pub async fn get_metrics(&self) -> PerformanceMetrics {
        self.metrics.read().await.clone()
    }

    /// Clear the cache
    pub async fn clear_cache(&self) {
        let mut cache = self.cache.write().await;
        cache.clear();
        info!("CodeLlama response cache cleared");
    }

    /// Analyze code and provide suggestions
    pub async fn analyze_code(&self, code: &str, language: &str) -> Result<String> {
        let prompt = format!(
            "Analyze the following {} code and provide suggestions for improvements, \
             potential bugs, and optimization opportunities:\n\n```{}\n{}\n```",
            language, language, code
        );

        self.generate_code(&prompt).await
    }

    /// Generate unit tests for given code
    pub async fn generate_tests(&self, code: &str, language: &str) -> Result<String> {
        let prompt = format!(
            "Generate comprehensive unit tests for the following {} code. \
             Include edge cases and ensure good test coverage:\n\n```{}\n{}\n```",
            language, language, code
        );

        self.generate_code(&prompt).await
    }

    /// Fix code based on error message
    pub async fn fix_code(&self, code: &str, error: &str, language: &str) -> Result<String> {
        let prompt = format!(
            "Fix the following {} code that produces this error:\n\nError: {}\n\nCode:\n```{}\n{}\n```",
            language, error, language, code
        );

        self.generate_code(&prompt).await
    }

    /// Complete code snippet
    pub async fn complete_code(&self, partial_code: &str, language: &str) -> Result<String> {
        let prompt = format!(
            "Complete the following {} code snippet:\n\n```{}\n{}\n```",
            language, language, partial_code
        );

        self.generate_code(&prompt).await
    }
}

/// Trait for integrating with Think AI's response system
#[async_trait]
pub trait CodeAssistant: Send + Sync {
    async fn assist_with_code(&self, query: &str) -> Result<String>;
    async fn is_code_related(&self, query: &str) -> bool;
}

#[async_trait]
impl CodeAssistant for CodeLlamaClient {
    async fn assist_with_code(&self, query: &str) -> Result<String> {
        // Determine the type of code assistance needed
        let query_lower = query.to_lowercase();

        if query_lower.contains("analyze") || query_lower.contains("review") {
            // Extract code from query for analysis
            if let Some(code_block) = extract_code_block(query) {
                return self
                    .analyze_code(&code_block.code, &code_block.language)
                    .await;
            }
        } else if query_lower.contains("test") || query_lower.contains("unit test") {
            if let Some(code_block) = extract_code_block(query) {
                return self
                    .generate_tests(&code_block.code, &code_block.language)
                    .await;
            }
        } else if query_lower.contains("fix") || query_lower.contains("error") {
            if let Some(code_block) = extract_code_block(query) {
                let error = extract_error_message(query).unwrap_or("Unknown error");
                return self
                    .fix_code(&code_block.code, error, &code_block.language)
                    .await;
            }
        } else if query_lower.contains("complete") || query_lower.contains("finish") {
            if let Some(code_block) = extract_code_block(query) {
                return self
                    .complete_code(&code_block.code, &code_block.language)
                    .await;
            }
        }

        // Default: treat as general code generation request
        self.generate_code(query).await
    }

    async fn is_code_related(&self, query: &str) -> bool {
        let code_keywords = [
            "code",
            "program",
            "function",
            "class",
            "method",
            "algorithm",
            "implement",
            "write",
            "create",
            "debug",
            "fix",
            "error",
            "bug",
            "python",
            "rust",
            "javascript",
            "java",
            "c++",
            "golang",
            "typescript",
            "react",
            "vue",
            "angular",
            "database",
            "sql",
            "api",
            "test",
            "optimize",
            "refactor",
            "analyze",
            "review",
            "complete",
            "snippet",
        ];

        let query_lower = query.to_lowercase();
        code_keywords
            .iter()
            .any(|&keyword| query_lower.contains(keyword))
    }
}

// Helper structures and functions
struct CodeBlock {
    code: String,
    language: String,
}

fn extract_code_block(text: &str) -> Option<CodeBlock> {
    // Simple extraction without regex dependency
    if let Some(start) = text.find("```") {
        let after_start = &text[start + 3..];
        if let Some(end) = after_start.find("```") {
            let block = &after_start[..end];
            let lines: Vec<&str> = block.lines().collect();
            if !lines.is_empty() {
                let first_line = lines[0].trim();
                let (language, code_start) = if first_line.chars().all(|c| c.is_alphanumeric()) {
                    (first_line.to_string(), 1)
                } else {
                    ("python".to_string(), 0)
                };

                let code = lines[code_start..].join("\n");
                return Some(CodeBlock { code, language });
            }
        }
    }
    None
}

fn extract_error_message(text: &str) -> Option<&str> {
    // Look for error patterns
    if let Some(idx) = text.find("error:") {
        Some(&text[idx..])
    } else if let Some(idx) = text.find("Error:") {
        Some(&text[idx..])
    } else {
        None
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hash_function() {
        let config = CodeLlamaConfig::default();
        let client = CodeLlamaClient::with_config(config).unwrap();

        let hash1 = client.hash_prompt("test prompt");
        let hash2 = client.hash_prompt("test prompt");
        let hash3 = client.hash_prompt("different prompt");

        assert_eq!(hash1, hash2, "Same prompts should produce same hash");
        assert_ne!(
            hash1, hash3,
            "Different prompts should produce different hashes"
        );
    }

    #[test]
    fn test_code_detection() {
        let test_cases = vec![
            ("How do I write a function in Python?", true),
            ("Can you help me debug this code?", true),
            ("What's the weather today?", false),
            ("Implement a binary search algorithm", true),
            ("Tell me a joke", false),
        ];

        for (query, expected) in test_cases {
            let client = CodeLlamaClient::new().unwrap();
            let runtime = tokio::runtime::Runtime::new().unwrap();
            let is_code = runtime.block_on(client.is_code_related(query));
            assert_eq!(is_code, expected, "Failed for query: {}", query);
        }
    }

    #[test]
    fn test_code_block_extraction() {
        let text = "Here's my code:\n```python\ndef hello():\n    print('Hello')\n```";
        let block = extract_code_block(text).unwrap();

        assert_eq!(block.language, "python");
        assert!(block.code.contains("def hello()"));
    }
}
