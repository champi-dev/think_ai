#!/bin/bash
# Script to integrate a real LLM into Think AI

echo "🤖 Integrating Real LLM into Think AI"
echo "===================================="
echo ""

# Check if Ollama is installed (easiest option)
if command -v ollama >/dev/null 2>&1; then
    echo "✅ Ollama detected! This is the easiest way."
    echo ""
    echo "1️⃣ Pull a small model:"
    echo "   ollama pull tinyllama"
    echo "   ollama pull phi"
    echo ""
    echo "2️⃣ Start Ollama:"
    echo "   ollama serve"
    echo ""
    echo "3️⃣ Think AI will use Ollama API"
else
    echo "❌ Ollama not found"
    echo ""
    echo "Install Ollama (recommended):"
    echo "   curl -fsSL https://ollama.ai/install.sh | sh"
    echo ""
    echo "Or use alternative:"
fi

# Alternative: Use llama.cpp
echo ""
echo "Alternative: Build with llama.cpp"
echo "================================="
echo ""
echo "1️⃣ Clone llama.cpp:"
echo "   git clone https://github.com/ggerganov/llama.cpp"
echo "   cd llama.cpp && make"
echo ""
echo "2️⃣ Download a model:"
echo "   # TinyLlama (1.1B - 600MB)"
echo "   wget https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
echo ""
echo "3️⃣ Run the model server:"
echo "   ./server -m tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf -c 2048"
echo ""

# Create the integration code
echo "Creating LLM integration module..."

cat > think-ai-llm-simple/Cargo.toml << 'EOF'
[package]
name = "think-ai-llm-simple"
version = "0.1.0"
edition = "2021"

[dependencies]
# For Ollama/llama.cpp API
reqwest = { version = "0.11", features = ["json"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tokio = { version = "1.35", features = ["full"] }
anyhow = "1.0"
tracing = "0.1"

# For caching O(1) responses
dashmap = "5.5"
ahash = "0.8"
EOF

mkdir -p think-ai-llm-simple/src

cat > think-ai-llm-simple/src/lib.rs << 'EOF'
//! Simple LLM Integration for Think AI
//! Uses Ollama or llama.cpp server for actual generation

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
    pub fn new(api_url: Option<String>) -> Self {
        let api_url = api_url.unwrap_or_else(|| "http://localhost:11434".to_string());
        
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
    pub async fn generate(&self, prompt: &str) -> anyhow::Result<String> {
        let start = Instant::now();
        
        // Step 1: O(1) cache check
        let hash = self.hash_prompt(prompt);
        if let Some(cached) = self.cache.get(&hash) {
            tracing::info!("Cache hit! O(1) response in {:?}", start.elapsed());
            return Ok(cached.text.clone());
        }
        
        // Step 2: Generate with LLM
        tracing::info!("Cache miss, generating with LLM...");
        let response = self.generate_with_llm(prompt).await?;
        
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
    async fn generate_with_llm(&self, prompt: &str) -> anyhow::Result<String> {
        // Try Ollama API format
        let request = GenerateRequest {
            model: "tinyllama".to_string(),
            prompt: prompt.to_string(),
            stream: false,
        };
        
        let response = self.client
            .post(&format!("{}/api/generate", self.api_url))
            .json(&request)
            .send()
            .await?;
        
        if response.status().is_success() {
            let gen_response: GenerateResponse = response.json().await?;
            Ok(gen_response.response)
        } else {
            // Fallback to llama.cpp format
            let llama_request = serde_json::json!({
                "prompt": prompt,
                "n_predict": 128,
                "temperature": 0.7,
            });
            
            let response = self.client
                .post(&format!("{}/completion", self.api_url))
                .json(&llama_request)
                .send()
                .await?;
            
            let text = response.text().await?;
            let json: serde_json::Value = serde_json::from_str(&text)?;
            
            Ok(json["content"].as_str().unwrap_or("Error generating").to_string())
        }
    }
    
    /// Hash prompt for O(1) lookup
    fn hash_prompt(&self, prompt: &str) -> u64 {
        use std::hash::{Hash, Hasher};
        let mut hasher = ahash::AHasher::default();
        prompt.hash(&mut hasher);
        hasher.finish()
    }
    
    /// Get cache statistics
    pub fn cache_stats(&self) -> (usize, f32) {
        let size = self.cache.len();
        // In real app, track hits/misses
        (size, 0.0)
    }
}

/// Integration point for Think AI
pub async fn create_llm_engine() -> anyhow::Result<SimpleLLM> {
    // Check if Ollama is running
    let ollama_url = "http://localhost:11434";
    let llama_cpp_url = "http://localhost:8080";
    
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
EOF

echo ""
echo "✅ LLM integration module created!"
echo ""
echo "📋 Next Steps:"
echo "============="
echo ""
echo "1. Start an LLM server:"
echo "   Option A: ollama serve (then: ollama pull tinyllama)"
echo "   Option B: ./llama.cpp/server -m model.gguf"
echo ""
echo "2. Update Think AI to use the LLM:"
echo "   - Add think-ai-llm-simple to workspace"
echo "   - Wire it into the chat endpoint"
echo ""
echo "3. Test it:"
echo "   curl -X POST http://localhost:8080/api/chat \\"
echo "     -d '{\"query\": \"Write a poem about O(1) algorithms\"}'"