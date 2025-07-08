//! Think AI Image Generation with O(1) Caching
//! 
//! This module provides image generation capabilities with intelligent caching
//! to achieve O(1) retrieval of previously generated images.

use std::path::PathBuf;
use serde::{Serialize, Deserialize};
use sha2::{Sha256, Digest};
use anyhow::Result;
use dashmap::DashMap;
use std::sync::Arc;
use tokio::fs;

pub mod leonardo_client;
pub mod image_cache;
pub mod prompt_optimizer;
pub mod image_learner;
pub mod demo_mode;
pub mod open_source_generator;
pub mod ai_image_improver;

pub use leonardo_client::LeonardoClient;
pub use image_cache::ImageCache;
pub use prompt_optimizer::PromptOptimizer;
pub use image_learner::ImageLearner;
pub use demo_mode::DemoImageGenerator;
pub use open_source_generator::{OpenSourceGenerator, UserFeedback};
pub use ai_image_improver::AIImageImprover;

/// Configuration for the image generation system
#[derive(Debug, Clone)]
pub struct ImageGenConfig {
    pub api_key: String,
    pub api_url: String,
    pub cache_dir: PathBuf,
    pub max_cache_size_bytes: u64,
    pub enable_learning: bool,
}

impl ImageGenConfig {
    /// Create config from environment variables
    pub fn from_env() -> Result<Self> {
        let api_key = std::env::var("LEONARDO_API_KEY")
            .map_err(|_| anyhow::anyhow!("LEONARDO_API_KEY not set"))?;
        
        let api_url = std::env::var("LEONARDO_API_URL")
            .unwrap_or_else(|_| "https://cloud.leonardo.ai/api/rest/v1".to_string());
        
        let cache_dir = std::env::var("IMAGE_CACHE_DIR")
            .unwrap_or_else(|_| "./image_cache".to_string())
            .into();
        
        let max_cache_gb = std::env::var("IMAGE_CACHE_MAX_SIZE_GB")
            .unwrap_or_else(|_| "10".to_string())
            .parse::<u64>()
            .unwrap_or(10);
        
        Ok(Self {
            api_key,
            api_url,
            cache_dir,
            max_cache_size_bytes: max_cache_gb * 1024 * 1024 * 1024,
            enable_learning: true,
        })
    }
}

/// Main image generation system with O(1) caching
pub struct ImageGenerator {
    config: ImageGenConfig,
    client: Arc<LeonardoClient>,
    cache: Arc<ImageCache>,
    optimizer: Arc<PromptOptimizer>,
    learner: Option<Arc<ImageLearner>>,
    generation_history: Arc<DashMap<String, GenerationMetadata>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GenerationMetadata {
    pub prompt: String,
    pub enhanced_prompt: String,
    pub model_used: String,
    pub generation_time_ms: u64,
    pub file_size_bytes: u64,
    pub dimensions: (u32, u32),
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ImageGenerationRequest {
    pub prompt: String,
    pub negative_prompt: Option<String>,
    pub width: Option<u32>,
    pub height: Option<u32>,
    pub num_images: Option<u32>,
    pub guidance_scale: Option<f32>,
    pub model_id: Option<String>,
}

#[derive(Debug, Clone)]
pub struct GeneratedImage {
    pub image_data: Vec<u8>,
    pub metadata: GenerationMetadata,
    pub cache_hit: bool,
}

impl ImageGenerator {
    /// Create a new image generator with O(1) caching
    pub async fn new(config: ImageGenConfig) -> Result<Self> {
        // Ensure cache directory exists
        fs::create_dir_all(&config.cache_dir).await?;
        
        let client = Arc::new(LeonardoClient::new(&config.api_key, &config.api_url));
        let cache = Arc::new(ImageCache::new(&config.cache_dir, config.max_cache_size_bytes).await?);
        let optimizer = Arc::new(PromptOptimizer::new());
        
        let learner = if config.enable_learning {
            Some(Arc::new(ImageLearner::new(&config.cache_dir).await?))
        } else {
            None
        };
        
        Ok(Self {
            config,
            client,
            cache,
            optimizer,
            learner,
            generation_history: Arc::new(DashMap::new()),
        })
    }
    
    /// Generate an image with O(1) cache lookup
    pub async fn generate(&self, request: ImageGenerationRequest) -> Result<GeneratedImage> {
        // Generate cache key from request
        let cache_key = self.generate_cache_key(&request);
        
        // O(1) cache lookup
        if let Some(cached_image) = self.cache.get(&cache_key).await? {
            println!("🎯 O(1) Cache hit for prompt: {}", request.prompt);
            return Ok(GeneratedImage {
                image_data: cached_image.data,
                metadata: cached_image.metadata,
                cache_hit: true,
            });
        }
        
        println!("🎨 Generating new image for prompt: {}", request.prompt);
        
        // Optimize prompt using learned patterns
        let enhanced_prompt = self.optimizer.optimize(&request.prompt).await;
        
        // Generate image via API
        let start_time = std::time::Instant::now();
        let (image_data, dimensions) = match self.client.generate_image(
            &enhanced_prompt,
            request.negative_prompt.as_deref(),
            request.width,
            request.height,
            request.num_images,
            request.guidance_scale,
            request.model_id.as_deref(),
        ).await {
            Ok(result) => result,
            Err(e) => {
                // Check if it's an API credit issue
                if e.to_string().contains("not enough api tokens") {
                    println!("⚠️  API credits exhausted, using demo mode");
                    DemoImageGenerator::generate_demo_image(
                        &enhanced_prompt,
                        request.width.unwrap_or(512),
                        request.height.unwrap_or(512),
                    ).await?
                } else {
                    return Err(e);
                }
            }
        };
        let generation_time_ms = start_time.elapsed().as_millis() as u64;
        
        // Create metadata
        let metadata = GenerationMetadata {
            prompt: request.prompt.clone(),
            enhanced_prompt: enhanced_prompt.clone(),
            model_used: request.model_id.unwrap_or_else(|| "default".to_string()),
            generation_time_ms,
            file_size_bytes: image_data.len() as u64,
            dimensions,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };
        
        // Store in cache for O(1) future retrieval
        self.cache.store(&cache_key, &image_data, &metadata).await?;
        
        // Update generation history
        self.generation_history.insert(cache_key.clone(), metadata.clone());
        
        // Learn from this generation if learning is enabled
        if let Some(learner) = &self.learner {
            learner.learn_from_generation(&request.prompt, &enhanced_prompt, &metadata).await?;
        }
        
        Ok(GeneratedImage {
            image_data,
            metadata,
            cache_hit: false,
        })
    }
    
    /// Generate cache key using SHA256 for O(1) lookups
    fn generate_cache_key(&self, request: &ImageGenerationRequest) -> String {
        let mut hasher = Sha256::new();
        hasher.update(&request.prompt);
        if let Some(neg) = &request.negative_prompt {
            hasher.update(neg);
        }
        hasher.update(request.width.unwrap_or(512).to_le_bytes());
        hasher.update(request.height.unwrap_or(512).to_le_bytes());
        if let Some(model) = &request.model_id {
            hasher.update(model);
        }
        format!("{:x}", hasher.finalize())
    }
    
    /// Get generation statistics
    pub fn get_stats(&self) -> GenerationStats {
        let total_generations = self.generation_history.len();
        let cache_stats = self.cache.get_stats();
        
        GenerationStats {
            total_generations,
            cache_hits: cache_stats.hits,
            cache_misses: cache_stats.misses,
            cache_hit_rate: if total_generations > 0 {
                cache_stats.hits as f64 / total_generations as f64
            } else {
                0.0
            },
            total_cache_size_bytes: cache_stats.total_size_bytes,
            average_generation_time_ms: self.calculate_avg_generation_time(),
        }
    }
    
    fn calculate_avg_generation_time(&self) -> f64 {
        let times: Vec<u64> = self.generation_history
            .iter()
            .map(|entry| entry.value().generation_time_ms)
            .collect();
        
        if times.is_empty() {
            0.0
        } else {
            times.iter().sum::<u64>() as f64 / times.len() as f64
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct GenerationStats {
    pub total_generations: usize,
    pub cache_hits: u64,
    pub cache_misses: u64,
    pub cache_hit_rate: f64,
    pub total_cache_size_bytes: u64,
    pub average_generation_time_ms: f64,
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_cache_key_generation() {
        let config = ImageGenConfig {
            api_key: "test".to_string(),
            api_url: "http://test".to_string(),
            cache_dir: "/tmp/test".into(),
            max_cache_size_bytes: 1024 * 1024,
            enable_learning: false,
        };
        
        let generator = ImageGenerator::new(config).await.unwrap();
        
        let request1 = ImageGenerationRequest {
            prompt: "A beautiful sunset".to_string(),
            negative_prompt: None,
            width: Some(512),
            height: Some(512),
            num_images: Some(1),
            guidance_scale: None,
            model_id: None,
        };
        
        let request2 = ImageGenerationRequest {
            prompt: "A beautiful sunset".to_string(),
            negative_prompt: None,
            width: Some(512),
            height: Some(512),
            num_images: Some(1),
            guidance_scale: None,
            model_id: None,
        };
        
        let key1 = generator.generate_cache_key(&request1);
        let key2 = generator.generate_cache_key(&request2);
        
        assert_eq!(key1, key2, "Same requests should generate same cache keys");
    }
}