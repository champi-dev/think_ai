// Ollama Component for general AI queries using qwen2.5:3b
use crate::response_generator::{ResponseComponent, ResponseContext};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::time::Duration;

pub struct OllamaComponent {
    client: reqwest::Client,
    model: String,
    endpoint: String,
}

impl Default for OllamaComponent {
    fn default() -> Self {
        Self::new()
    }
}

impl OllamaComponent {
    pub fn new() -> Self {
        Self {
            client: reqwest::Client::builder()
                .timeout(Duration::from_secs(30))
                .build()
                .unwrap_or_else(|_| reqwest::Client::new()),
            model: "qwen2.5:3b".to_string(),
            endpoint: "http://localhost:11434".to_string(),
        }
    }

    pub fn with_model(model: String) -> Self {
        Self {
            client: reqwest::Client::builder()
                .timeout(Duration::from_secs(30))
                .build()
                .unwrap_or_else(|_| reqwest::Client::new()),
            model,
            endpoint: "http://localhost:11434".to_string(),
        }
    }

    async fn generate_ollama_response(&self, query: &str) -> Option<String> {
        #[derive(Serialize)]
        struct OllamaRequest {
            model: String,
            prompt: String,
            stream: bool,
            options: OllamaOptions,
        }

        #[derive(Serialize)]
        struct OllamaOptions {
            temperature: f32,
            num_predict: i32,
        }

        #[derive(Deserialize)]
        struct OllamaResponse {
            response: String,
        }

        let request = OllamaRequest {
            model: self.model.clone(),
            prompt: query.to_string(),
            stream: false,
            options: OllamaOptions {
                temperature: 0.7,
                num_predict: 512,
            },
        };

        let url = format!("{}/api/generate", self.endpoint);

        match self.client.post(&url).json(&request).send().await {
            Ok(response) => {
                if response.status().is_success() {
                    match response.json::<OllamaResponse>().await {
                        Ok(data) => Some(data.response),
                        Err(e) => {
                            eprintln!("Failed to parse Ollama response: {}", e);
                            None
                        }
                    }
                } else {
                    eprintln!("Ollama returned status: {}", response.status());
                    None
                }
            }
            Err(e) => {
                eprintln!("Failed to connect to Ollama: {}", e);
                None
            }
        }
    }
}

impl ResponseComponent for OllamaComponent {
    fn name(&self) -> &'static str {
        "Ollama"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        // Skip if it's a code request (handled by CodeLlama)
        if query.starts_with("[CODE REQUEST]") {
            return 0.0;
        }

        // Handle all general requests with high priority
        if query.starts_with("[GENERAL REQUEST]") {
            return 0.95;
        }

        // Check if query is NOT code-related
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
        ];

        let query_lower = query.to_lowercase();
        let has_code_keywords = code_keywords
            .iter()
            .any(|&keyword| query_lower.contains(keyword));

        if has_code_keywords {
            0.0 // Let CodeLlama handle it
        } else {
            0.8 // High priority for general queries
        }
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        // Clean the query by removing the [GENERAL REQUEST] prefix if present
        let clean_query = if query.starts_with("[GENERAL REQUEST]") {
            query.trim_start_matches("[GENERAL REQUEST]").trim()
        } else {
            query
        };

        // Use Handle::current() to check if we're in a runtime
        if let Ok(handle) = tokio::runtime::Handle::try_current() {
            // We're already in a runtime, use it
            tokio::task::block_in_place(|| {
                handle.block_on(self.generate_ollama_response(clean_query))
            })
        } else {
            // No runtime, create one
            let runtime = tokio::runtime::Runtime::new().ok()?;
            runtime.block_on(self.generate_ollama_response(clean_query))
        }
    }

    fn metadata(&self) -> HashMap<String, String> {
        let mut meta = HashMap::new();
        meta.insert("version".to_string(), "1.0.0".to_string());
        meta.insert("model".to_string(), self.model.clone());
        meta.insert("type".to_string(), "general_assistant".to_string());
        meta.insert("performance".to_string(), "O(1) with caching".to_string());
        meta
    }
}
