// AI-Powered Image Improvement System
//!
// This module enables Think AI to learn from generated images and continuously
// improve its image generation capabilities through reinforcement learning.

use anyhow::Result;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

use crate::image_cache::ImageCache;
use crate::image_learner::ImageLearner;
use crate::open_source_generator::{OpenSourceGenerator, UserFeedback};

/// AI Image Improver - Learns from feedback and improves over time
pub struct AIImageImprover {
    generator: Arc<OpenSourceGenerator>,
    cache: Arc<ImageCache>,
    learner: Arc<ImageLearner>,
    improvement_model: Arc<RwLock<ImprovementModel>>,
    feedback_history: Arc<RwLock<Vec<FeedbackRecord>>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ImprovementModel {
    /// Prompt enhancement strategies that work well
    enhancement_strategies: HashMap<String, EnhancementStrategy>,
    /// Style combinations that produce high-quality results
    style_combinations: HashMap<String, f32>,
    /// Negative prompt patterns to avoid common issues
    negative_patterns: Vec<String>,
    /// Model performance metrics
    model_metrics: ModelMetrics,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct EnhancementStrategy {
    pattern: String,
    success_rate: f32,
    usage_count: u32,
    examples: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ModelMetrics {
    total_generations: u64,
    successful_generations: u64,
    average_quality_score: f32,
    improvement_rate: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct FeedbackRecord {
    prompt: String,
    enhanced_prompt: String,
    feedback: UserFeedback,
    improvements_applied: Vec<String>,
    timestamp: u64,
}

impl AIImageImprover {
    /// Create a new AI Image Improver
    pub async fn new(cache_dir: &std::path::Path, api_token: Option<String>) -> Result<Self> {
        let generator = Arc::new(OpenSourceGenerator::new(api_token));
        let cache = Arc::new(ImageCache::new(cache_dir, 10 * 1024 * 1024 * 1024).await?); // 10GB
        let learner = Arc::new(ImageLearner::new(cache_dir).await?);

        let improvement_model = Arc::new(RwLock::new(ImprovementModel {
            enhancement_strategies: Self::initialize_strategies(),
            style_combinations: Self::initialize_styles(),
            negative_patterns: Self::initialize_negative_patterns(),
            model_metrics: ModelMetrics {
                total_generations: 0,
                successful_generations: 0,
                average_quality_score: 0.5,
                improvement_rate: 0.0,
            },
        }));

        Ok(Self {
            generator,
            cache,
            learner,
            improvement_model,
            feedback_history: Arc::new(RwLock::new(Vec::new())),
        })
    }

    /// Generate an improved image using AI learning
    pub async fn generate_improved(
        &self,
        prompt: &str,
        width: Option<u32>,
        height: Option<u32>,
    ) -> Result<(Vec<u8>, String)> {
        // Get cache key
        let cache_key = self.generate_cache_key(prompt, width, height);

        // Check O(1) cache
        if let Some(cached) = self.cache.get(&cache_key).await? {
            println!("🎯 O(1) Cache hit with AI improvements!");
            return Ok((cached.data, cached.metadata.enhanced_prompt));
        }

        // Apply AI improvements to prompt
        let improved_prompt = self.apply_ai_improvements(prompt).await?;
        let negative_prompt = self.generate_negative_prompt(prompt).await;

        println!("🤖 AI Enhanced prompt: {improved_prompt}");
        if let Some(neg) = &negative_prompt {
            println!("🚫 AI Negative prompt: {neg}");
        }

        // Generate image
        let image_data = self
            .generator
            .generate(&improved_prompt, negative_prompt.as_deref(), width, height)
            .await?;

        // Store in cache
        let metadata = crate::GenerationMetadata {
            prompt: prompt.to_string(),
            enhanced_prompt: improved_prompt.clone(),
            model_used: "open-source".to_string(),
            generation_time_ms: 1000, // Placeholder
            file_size_bytes: image_data.len() as u64,
            dimensions: (width.unwrap_or(512), height.unwrap_or(512)),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };

        self.cache.store(&cache_key, &image_data, &metadata).await?;

        // Learn from this generation
        self.learner
            .learn_from_generation(prompt, &improved_prompt, &metadata)
            .await?;

        // Update model metrics
        self.update_metrics(true).await;

        Ok((image_data, improved_prompt))
    }

    /// Apply AI improvements to the prompt
    async fn apply_ai_improvements(&self, prompt: &str) -> Result<String> {
        let model = self.improvement_model.read().await;
        let mut improved = prompt.to_string();

        // Analyze prompt for improvement opportunities
        let prompt_analysis = self.analyze_prompt(prompt);

        // Apply enhancement strategies based on success rates
        let mut applied_strategies = Vec::new();

        for (key, strategy) in &model.enhancement_strategies {
            if strategy.success_rate > 0.7 && self.should_apply_strategy(prompt, strategy) {
                improved = self.apply_strategy(&improved, strategy);
                applied_strategies.push(key.clone());
            }
        }

        // Add high-performing style combinations
        for (style, score) in &model.style_combinations {
            if *score > 0.8 && !improved.contains(style) {
                improved.push_str(&format!(", {style}"));
            }
        }

        // Ensure quality modifiers based on learning
        if prompt_analysis.needs_detail && !improved.contains("detailed") {
            improved.push_str(", highly detailed, intricate");
        }

        if prompt_analysis.needs_quality && !improved.contains("quality") {
            improved.push_str(", best quality, masterpiece");
        }

        if prompt_analysis.is_artistic && !improved.contains("artistic") {
            improved.push_str(", artistic, professional");
        }

        Ok(improved)
    }

    /// Generate negative prompt to avoid common issues
    async fn generate_negative_prompt(&self, prompt: &str) -> Option<String> {
        let model = self.improvement_model.read().await;

        let mut negative_terms = vec![
            "low quality",
            "blurry",
            "pixelated",
            "distorted",
            "deformed",
        ];

        // Add learned negative patterns
        for pattern in &model.negative_patterns {
            if !negative_terms.contains(&pattern.as_str()) {
                negative_terms.push(pattern);
            }
        }

        // Context-specific negatives
        if prompt.contains("person") || prompt.contains("portrait") {
            negative_terms.extend(&["bad anatomy", "extra limbs", "malformed"]);
        }

        if prompt.contains("landscape") || prompt.contains("nature") {
            negative_terms.extend(&["unrealistic", "oversaturated"]);
        }

        Some(negative_terms.join(", "))
    }

    /// Provide feedback to improve the AI
    pub async fn provide_feedback(
        &self,
        prompt: &str,
        feedback: UserFeedback,
        suggestions: Option<Vec<String>>,
    ) -> Result<()> {
        // Update generator's learning
        self.generator
            .update_feedback(prompt, feedback.clone())
            .await?;

        // Record feedback
        let record = FeedbackRecord {
            prompt: prompt.to_string(),
            enhanced_prompt: String::new(), // TODO: Track this
            feedback: feedback.clone(),
            improvements_applied: suggestions.clone().unwrap_or_default(),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };

        self.feedback_history.write().await.push(record);

        // Update improvement model based on feedback
        self.update_improvement_model(&feedback, &suggestions)
            .await?;

        // Update metrics
        let is_success = matches!(feedback, UserFeedback::Excellent | UserFeedback::Good);
        self.update_metrics(is_success).await;

        Ok(())
    }

    /// Analyze prompt to determine improvement needs
    fn analyze_prompt(&self, prompt: &str) -> PromptAnalysis {
        let words: Vec<&str> = prompt.split_whitespace().collect();
        let word_count = words.len();

        PromptAnalysis {
            needs_detail: word_count < 5,
            needs_quality: !prompt.contains("quality") && !prompt.contains("detailed"),
            is_artistic: prompt.contains("art")
                || prompt.contains("painting")
                || prompt.contains("drawing"),
            is_photographic: prompt.contains("photo") || prompt.contains("realistic"),
            has_style: prompt.contains("style") || prompt.contains("inspired"),
        }
    }

    /// Determine if a strategy should be applied
    fn should_apply_strategy(&self, prompt: &str, strategy: &EnhancementStrategy) -> bool {
        // Check if the strategy pattern matches the prompt context
        let prompt_lower = prompt.to_lowercase();
        let pattern_lower = strategy.pattern.to_lowercase();

        // Simple pattern matching - in production, use NLP
        prompt_lower.contains(&pattern_lower)
            || (strategy.usage_count > 10 && strategy.success_rate > 0.8)
    }

    /// Apply a specific enhancement strategy
    fn apply_strategy(&self, prompt: &str, strategy: &EnhancementStrategy) -> String {
        // Apply the strategy based on its examples
        if let Some(example) = strategy.examples.first() {
            format!("{prompt}, {example}")
        } else {
            prompt.to_string()
        }
    }

    /// Update improvement model based on feedback
    async fn update_improvement_model(
        &self,
        feedback: &UserFeedback,
        suggestions: &Option<Vec<String>>,
    ) -> Result<()> {
        let mut model = self.improvement_model.write().await;

        // Update style combinations based on feedback
        let score_delta = match feedback {
            UserFeedback::Excellent => 0.1,
            UserFeedback::Good => 0.05,
            UserFeedback::Average => -0.02,
            UserFeedback::Poor => -0.1,
        };

        // If we have suggestions, they might be styles to improve
        if let Some(suggestions) = suggestions {
            for suggestion in suggestions {
                let score = model
                    .style_combinations
                    .entry(suggestion.clone())
                    .or_insert(0.5);
                *score = (*score + score_delta).clamp(0.0, 1.0);
            }
        }

        Ok(())
    }

    /// Update model metrics
    async fn update_metrics(&self, is_success: bool) {
        let mut model = self.improvement_model.write().await;
        let metrics = &mut model.model_metrics;

        metrics.total_generations += 1;
        if is_success {
            metrics.successful_generations += 1;
        }

        // Update average quality score
        let _success_rate =
            metrics.successful_generations as f32 / metrics.total_generations as f32;
        metrics.average_quality_score = success_rate;

        // Calculate improvement rate (comparing recent vs overall performance)
        if metrics.total_generations > 10 {
            let recent_rate = if metrics.total_generations > 100 {
                // Last 10% of generations
                let recent_window = metrics.total_generations / 10;
                metrics.successful_generations as f32 / recent_window as f32
            } else {
                success_rate
            };

            metrics.improvement_rate = recent_rate - 0.5; // Baseline of 0.5
        }
    }

    /// Generate cache key
    fn generate_cache_key(
        &self,
        prompt: &str,
        width: Option<u32>,
        height__: Option<u32>,
    ) -> String {
        use sha2::{Digest, Sha256};
        let mut hasher = Sha256::new();
        hasher.update(prompt);
        hasher.update(width.unwrap_or(512).to_le_bytes());
        hasher.update(height.unwrap_or(512).to_le_bytes());
        hasher.update(b"ai-improved");
        format!("{:x}", hasher.finalize())
    }

    /// Get AI learning statistics
    pub async fn get_ai_stats(&self) -> AILearningStats {
        let model = self.improvement_model.read().await;
        let generator_stats = self.generator.get_learning_stats().await;
        let feedback_history = self.feedback_history.read().await;

        let excellent_feedback = feedback_history
            .iter()
            .filter(|r| matches!(r.feedback, UserFeedback::Excellent))
            .count();

        let top_strategies: Vec<(String, f32)> = model
            .enhancement_strategies
            .iter()
            .map(|(k, v)| (k.clone(), v.success_rate))
            .filter(|(_, rate)| *rate > 0.7)
            .collect();

        AILearningStats {
            total_generations: model.model_metrics.total_generations,
            success_rate: model.model_metrics.average_quality_score,
            improvement_rate: model.model_metrics.improvement_rate,
            excellent_generations: excellent_feedback,
            top_strategies,
            active_styles: model.style_combinations.len(),
            learned_patterns: model.enhancement_strategies.len(),
            feedback_count: feedback_history.len(),
        }
    }

    /// Initialize default enhancement strategies
    fn initialize_strategies() -> HashMap<String, EnhancementStrategy> {
        let mut strategies = HashMap::new();

        strategies.insert(
            "portrait".to_string(),
            EnhancementStrategy {
                pattern: "portrait".to_string(),
                success_rate: 0.75,
                usage_count: 0,
                examples: vec![
                    "professional lighting".to_string(),
                    "sharp focus on face".to_string(),
                ],
            },
        );

        strategies.insert(
            "landscape".to_string(),
            EnhancementStrategy {
                pattern: "landscape".to_string(),
                success_rate: 0.8,
                usage_count: 0,
                examples: vec![
                    "dramatic sky".to_string(),
                    "golden hour lighting".to_string(),
                ],
            },
        );

        strategies.insert(
            "abstract".to_string(),
            EnhancementStrategy {
                pattern: "abstract".to_string(),
                success_rate: 0.7,
                usage_count: 0,
                examples: vec![
                    "vibrant colors".to_string(),
                    "dynamic composition".to_string(),
                ],
            },
        );

        strategies
    }

    /// Initialize default style combinations
    fn initialize_styles() -> HashMap<String, f32> {
        let mut styles = HashMap::new();

        styles.insert("digital art".to_string(), 0.8);
        styles.insert("concept art".to_string(), 0.75);
        styles.insert("trending on artstation".to_string(), 0.85);
        styles.insert("octane render".to_string(), 0.7);
        styles.insert("unreal engine".to_string(), 0.7);

        styles
    }

    /// Initialize negative patterns to avoid
    fn initialize_negative_patterns() -> Vec<String> {
        vec![
            "bad composition".to_string(),
            "amateur".to_string(),
            "poorly drawn".to_string(),
            "bad lighting".to_string(),
            "oversaturated".to_string(),
        ]
    }
}

#[derive(Debug)]
struct PromptAnalysis {
    needs_detail: bool,
    needs_quality: bool,
    is_artistic: bool,
    is_photographic: bool,
    has_style: bool,
}

#[derive(Debug, Clone, Serialize)]
pub struct AILearningStats {
    pub total_generations: u64,
    pub success_rate: f32,
    pub improvement_rate: f32,
    pub excellent_generations: usize,
    pub top_strategies: Vec<(String, f32)>,
    pub active_styles: usize,
    pub learned_patterns: usize,
    pub feedback_count: usize,
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[tokio::test]
    async fn test_ai_improvement() {
        let temp_dir = TempDir::new().unwrap();
        let improver = AIImageImprover::new(temp_dir.path(), None).await.unwrap();

        let (data, enhanced) = improver
            .generate_improved("a simple cat", Some(256), Some(256))
            .await
            .unwrap();

        assert!(!data.is_empty());
        assert!(enhanced.contains("cat"));
        assert!(enhanced.len() > 12); // Should be enhanced
    }
}
