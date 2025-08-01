use std::sync::Arc;
use std::time::{Duration, Instant};
use dashmap::DashMap;
use parking_lot::RwLock;
use serde::{Deserialize, Serialize};
use tokio::sync::mpsc;
use tracing;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OptimizationConfig {
    // Cache settings
    pub enable_response_cache: bool,
    pub cache_ttl_seconds: u64,
    pub max_cache_size: usize,
    
    // Model settings
    pub model_timeout_ms: u64,
    pub max_tokens: usize,
    pub temperature: f32,
    pub num_gpu_layers: Option<i32>,
    
    // Concurrency settings
    pub max_concurrent_requests: usize,
    pub request_queue_size: usize,
    
    // Prefetch settings
    pub enable_prefetch: bool,
    pub common_queries: Vec<String>,
}

impl Default for OptimizationConfig {
    fn default() -> Self {
        Self {
            enable_response_cache: true,
            cache_ttl_seconds: 86400, // 24 hours - trade disk for speed
            max_cache_size: 1000000, // 1M entries - aggressive caching
            
            model_timeout_ms: 10000, // 10 seconds base timeout, will scale with token count
            max_tokens: 2000, // Default 2k tokens, will adjust based on query complexity
            temperature: 0.7, // Balanced temperature for better responses
            num_gpu_layers: None, // Auto-detect
            
            max_concurrent_requests: 10,
            request_queue_size: 100,
            
            enable_prefetch: true,
            common_queries: vec![
                "hello".to_string(),
                "help".to_string(),
                "what can you do".to_string(),
            ],
        }
    }
}

pub struct ResponseCache {
    cache: Arc<DashMap<u64, CachedResponse>>,
    config: OptimizationConfig,
}

#[derive(Clone)]
struct CachedResponse {
    content: String,
    timestamp: Instant,
}

impl ResponseCache {
    pub fn new(config: OptimizationConfig) -> Self {
        let cache = Arc::new(DashMap::with_capacity(config.max_cache_size));
        
        // Prefetch common responses if enabled
        if config.enable_prefetch {
            let cache_clone = cache.clone();
            tokio::spawn(async move {
                // This would prefetch common queries
                // Implementation depends on your generate_response function
            });
        }
        
        Self { cache, config }
    }
    
    pub fn get(&self, query: &str) -> Option<String> {
        if !self.config.enable_response_cache {
            return None;
        }
        
        let hash = self.hash_query(query);
        
        if let Some(cached) = self.cache.get(&hash) {
            let age = cached.timestamp.elapsed();
            if age.as_secs() < self.config.cache_ttl_seconds {
                return Some(cached.content.clone());
            } else {
                // Remove expired entry
                self.cache.remove(&hash);
            }
        }
        
        None
    }
    
    pub fn set(&self, query: &str, response: String) {
        if !self.config.enable_response_cache {
            return;
        }
        
        let hash = self.hash_query(query);
        
        // Implement LRU if cache is full
        if self.cache.len() >= self.config.max_cache_size {
            // Remove oldest entry (simple implementation)
            if let Some(oldest_key) = self.cache.iter()
                .min_by_key(|entry| entry.timestamp.elapsed())
                .map(|entry| *entry.key()) {
                self.cache.remove(&oldest_key);
            }
        }
        
        self.cache.insert(hash, CachedResponse {
            content: response,
            timestamp: Instant::now(),
        });
    }
    
    fn hash_query(&self, query: &str) -> u64 {
        use std::collections::hash_map::DefaultHasher;
        use std::hash::{Hash, Hasher};
        
        let mut hasher = DefaultHasher::new();
        query.to_lowercase().hash(&mut hasher);
        hasher.finish()
    }
}

pub struct RequestOptimizer {
    cache: ResponseCache,
    config: OptimizationConfig,
    metrics: Arc<RwLock<OptimizationMetrics>>,
    request_semaphore: Arc<tokio::sync::Semaphore>,
}

#[derive(Default)]
struct OptimizationMetrics {
    cache_hits: u64,
    cache_misses: u64,
    avg_response_time_ms: f64,
    total_requests: u64,
}

impl RequestOptimizer {
    pub fn new(config: OptimizationConfig) -> Self {
        let semaphore = Arc::new(tokio::sync::Semaphore::new(config.max_concurrent_requests));
        
        Self {
            cache: ResponseCache::new(config.clone()),
            config,
            metrics: Arc::new(RwLock::new(OptimizationMetrics::default())),
            request_semaphore: semaphore,
        }
    }
    
    pub async fn optimize_request<Fut, FutFactory>(&self, query: &str, mut generate_fn: FutFactory) -> Result<String, anyhow::Error>
    where
        FutFactory: FnMut(String, OptimizationConfig) -> Fut,
        Fut: std::future::Future<Output = Result<String, anyhow::Error>>,
    {
        let start = Instant::now();
        
        // Check cache first
        if let Some(cached) = self.cache.get(query) {
            self.update_metrics(start.elapsed(), true);
            return Ok(cached);
        }
        
        // Acquire semaphore to limit concurrent requests
        let _permit = self.request_semaphore.acquire().await?;
        
        // Implement exponential backoff with retries
        const MAX_RETRIES: u32 = 3;
        let mut retry_count = 0;
        let mut last_error = None;
        
        while retry_count < MAX_RETRIES {
            // Calculate timeout with exponential backoff
            // Base timeout scales with expected token generation
            // More realistic: 1s per 100 tokens for qwen2.5:7b
            let token_limit = determine_token_limit(query);
            let base_timeout = ((token_limit as u64 / 100) * 1000).max(15000); // Min 15s to match qwen client
            let timeout_ms = base_timeout + (retry_count as u64 * base_timeout);
            let timeout_duration = Duration::from_millis(timeout_ms);
            
            match tokio::time::timeout(
                timeout_duration,
                generate_fn(query.to_string(), self.config.clone())
            ).await {
                Ok(Ok(response)) => {
                    // Success! Cache and return
                    self.cache.set(query, response.clone());
                    self.update_metrics(start.elapsed(), false);
                    return Ok(response);
                }
                Ok(Err(e)) => {
                    // Generation failed, but not a timeout
                    last_error = Some(format!("Generation error: {}", e));
                    retry_count += 1;
                }
                Err(_) => {
                    // Timeout occurred
                    last_error = Some(format!("Timeout after {}ms", timeout_ms));
                    retry_count += 1;
                }
            }
            
            // If we're going to retry, wait with exponential backoff
            if retry_count < MAX_RETRIES {
                let backoff_ms = 1000 * (2_u64.pow(retry_count - 1));
                tokio::time::sleep(Duration::from_millis(backoff_ms)).await;
                tracing::warn!("Retrying request (attempt {}/{}): {}", retry_count + 1, MAX_RETRIES, last_error.as_ref().unwrap_or(&"Unknown error".to_string()));
            }
        }
        
        // All retries exhausted
        self.update_metrics(start.elapsed(), false);
        Err(anyhow::anyhow!("Request failed after {} retries: {}", MAX_RETRIES, last_error.unwrap_or_else(|| "Unknown error".to_string())))
    }
    
    fn update_metrics(&self, duration: Duration, cache_hit: bool) {
        let mut metrics = self.metrics.write();
        
        if cache_hit {
            metrics.cache_hits += 1;
        } else {
            metrics.cache_misses += 1;
        }
        
        metrics.total_requests += 1;
        
        // Update rolling average
        let new_time = duration.as_millis() as f64;
        metrics.avg_response_time_ms = 
            (metrics.avg_response_time_ms * (metrics.total_requests - 1) as f64 + new_time) 
            / metrics.total_requests as f64;
    }
    
    pub fn get_metrics(&self) -> serde_json::Value {
        let metrics = self.metrics.read();
        let cache_hit_rate = if metrics.total_requests > 0 {
            metrics.cache_hits as f64 / metrics.total_requests as f64
        } else {
            0.0
        };
        
        serde_json::json!({
            "cache_hit_rate": cache_hit_rate,
            "avg_response_time_ms": metrics.avg_response_time_ms,
            "total_requests": metrics.total_requests,
            "cache_hits": metrics.cache_hits,
            "cache_misses": metrics.cache_misses
        })
    }
}

// GPU detection and optimization
pub fn detect_and_configure_gpu() -> Option<i32> {
    use std::process::Command;
    
    // Check if GPU is available
    if let Ok(output) = Command::new("nvidia-smi").output() {
        if output.status.success() {
            // GPU detected, determine optimal layer count based on VRAM
            let output_str = String::from_utf8_lossy(&output.stdout);
            
            // Parse available memory (simplified)
            if output_str.contains("2048MiB") || output_str.contains("2GB") {
                // 2GB GPU - use fewer layers
                return Some(24);
            } else if output_str.contains("4096MiB") || output_str.contains("4GB") {
                // 4GB GPU
                return Some(32);
            } else {
                // 8GB+ GPU
                return Some(50);
            }
        }
    }
    
    None
}

// Function to determine appropriate token limit based on query complexity
pub fn determine_token_limit(query: &str) -> usize {
    let char_count = query.len();
    let word_count = query.split_whitespace().count();
    let query_lower = query.to_lowercase();
    
    // Base calculation: proportional to input length
    // Roughly 2-3x the input tokens for simple queries, up to 10x for complex ones
    let base_tokens = (char_count / 4).max(50); // Approximate chars to tokens conversion
    
    // Multiplier based on query type
    let multiplier = if query_lower.contains("explain") || 
                        query_lower.contains("how does") ||
                        query_lower.contains("what is") ||
                        query_lower.contains("describe") ||
                        query_lower.contains("in detail") ||
                        query_lower.contains("comprehensive") {
        10.0 // Detailed explanations need more tokens
    } else if query_lower.contains("code") ||
              query_lower.contains("write") ||
              query_lower.contains("function") ||
              query_lower.contains("implement") {
        8.0 // Code generation needs substantial tokens
    } else if word_count > 20 || (query.contains("?") && query.contains(",")) {
        5.0 // Multi-part questions
    } else if query_lower.contains("hello") || 
              query_lower.contains("hi") ||
              query_lower.contains("thanks") ||
              word_count < 5 {
        2.0 // Simple greetings get simple responses
    } else {
        3.0 // Default multiplier
    };
    
    // Calculate final token limit
    let calculated_tokens = (base_tokens as f64 * multiplier) as usize;
    
    // Apply reasonable bounds
    // Min: 100 tokens (even "hi" should get a decent response)
    // Max: 2000 tokens (to prevent excessive generation time)
    calculated_tokens.clamp(100, 2000)
}