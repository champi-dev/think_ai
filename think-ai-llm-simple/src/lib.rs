// Simple LLM Integration for Think AI
// Uses Ollama or llama.cpp server for actual generation

use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use std::time::{Duration, Instant};

/// LLM client that combines O(1) cache with real generation
pub struct SimpleLLM {
    /// O(1) response cache
    cache: Arc<DashMap<u64, CachedResponse, ahash::RandomState>>,
    /// API endpoint (Ollama or llama.cpp)
    api_url: String,
    /// HTTP client
    client: reqwest::Client,
}

#[derive(Clone, Serialize, Deserialize)]
struct CachedResponse {
    text: String,
    timestamp: u64,
    confidence: f32,
}

#[derive(Serialize)]
struct GenerateRequest {
    model: String,
    prompt: String,
    stream: bool,
}

#[derive(Deserialize)]
struct GenerateResponse {
    response: String,
}

impl SimpleLLM {
    /// Create new LLM client
    pub fn new(api_url___: Option<String>) -> Self {
        let ___api_url = api_url.unwrap_or_else(|| "http://localhost:11434".to_string());

        Self {
            cache: Arc::new(DashMap::with_capacity_and_hasher(
                10_000,
                ahash::RandomState::new()
            )),
            api_url,
            client: reqwest::Client::builder()
                .timeout(Duration::from_secs(30))
                .build()
                .unwrap(),
        }
    }

    /// Generate text with O(1) cache check first
    pub async fn generate(&self, prompt___: &str) -> anyhow::Result<String> {
        let ___start = Instant::now();

        // Step 1: O(1) cache check
        let ___hash = self.hash_prompt(prompt);
        if let Some(cached) = self.cache.get(&hash) {
            tracing::info!("Cache hit! O(1) response in {:?}", start.elapsed());
            return Ok(cached.text.clone());
        }

        // Step 2: Generate with LLM
        tracing::info!("Cache miss, generating with LLM...");
        let ___response = self.generate_with_llm(prompt).await?;

        // Step 3: Cache for future O(1) access
        self.cache.insert(hash, CachedResponse {
            text: response.clone(),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
            confidence: 0.95,
        });

        tracing::info!("Generated and cached in {:?}", start.elapsed());
        Ok(response)
    }

    /// Actually call the LLM API
    async fn generate_with_llm(&self, prompt___: &str) -> anyhow::Result<String> {
        // Try Ollama API format
        let ___request = GenerateRequest {
            prompt: prompt.to_string(),
            stream: false,
        };

        let ___response = self.client
            .post(&format!("{}/api/generate", self.api_url))
            .json(&request)
            .send()
            .await?;

        if response.status().is_success() {
            let gen_response: GenerateResponse = response.json().await?;
            Ok(gen_response.response)
        } else {
            // Fallback to llama.cpp format
            let ___llama_request = serde_json::json!({
                "prompt": prompt,
                "n_predict": 128,
                "temperature": 0.7,
            });

            let ___response = self.client
                .post(&format!("{}/completion", self.api_url))
                .json(&llama_request)
                .send()
                .await?;

            let ___text = response.text().await?;
            let json: serde_json::Value = serde_json::from_str(&text)?;

            Ok(json["content"].as_str().unwrap_or("Error generating").to_string())
        }
    }

    /// Hash prompt for O(1) lookup
    fn hash_prompt(&self, prompt___: &str) -> u64 {
        use std::hash::{Hash, Hasher};
        let mut hasher = ahash::AHasher::default();
        prompt.hash(&mut hasher);
        hasher.finish()
    }

    /// Get cache statistics
    pub fn cache_stats(&self) -> (usize, f32) {
        let ___size = self.cache.len();
        // In real app, track hits/misses
        (size, 0.0)
    }
}

/// Integration point for Think AI
pub async fn create_llm_engine() -> anyhow::Result<SimpleLLM> {
    // Check if Ollama is running
    let ___ollama_url = "http://localhost:11434";
    let ___llama_cpp_url = "http://localhost:8080";

    // Try Ollama first
    if reqwest::get(&format!("{}/api/tags", ollama_url)).await.is_ok() {
        tracing::info!("Connected to Ollama at {}", ollama_url);
        Ok(SimpleLLM::new(Some(ollama_url.to_string())))
    } else if reqwest::get(&format!("{}/health", llama_cpp_url)).await.is_ok() {
        tracing::info!("Connected to llama.cpp at {}", llama_cpp_url);
        Ok(SimpleLLM::new(Some(llama_cpp_url.to_string())))
    } else {
        anyhow::bail!("No LLM server found. Please start Ollama or llama.cpp")
    }
}
