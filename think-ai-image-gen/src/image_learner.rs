//! Image Generation Learning System - Learn patterns for better generation

use anyhow::Result;
use serde::{Serialize, Deserialize};
use std::collections::HashMap;
use std::path::Path;
use tokio::fs;
use tokio::sync::RwLock;
use std::sync::Arc;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct LearningData {
    pub prompt_patterns: HashMap<String, PromptPattern>,
    pub style_effectiveness: HashMap<String, f32>,
    pub generation_metrics: GenerationMetrics,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PromptPattern {
    pub base_pattern: String,
    pub successful_variations: Vec<String>,
    pub average_generation_time: f32,
    pub usage_count: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GenerationMetrics {
    pub total_generations: u64,
    pub average_time_ms: f32,
    pub style_distribution: HashMap<String, u32>,
    pub dimension_distribution: HashMap<String, u32>,
}

/// Learns from image generation patterns to improve future generations
pub struct ImageLearner {
    data_path: std::path::PathBuf,
    learning_data: Arc<RwLock<LearningData>>,
}

impl ImageLearner {
    pub async fn new(cache_dir: &Path) -> Result<Self> {
        let data_path = cache_dir.join("learning_data.json");
        
        let learning_data = if data_path.exists() {
            let data = fs::read_to_string(&data_path).await?;
            serde_json::from_str(&data)?
        } else {
            LearningData {
                prompt_patterns: HashMap::new(),
                style_effectiveness: HashMap::new(),
                generation_metrics: GenerationMetrics {
                    total_generations: 0,
                    average_time_ms: 0.0,
                    style_distribution: HashMap::new(),
                    dimension_distribution: HashMap::new(),
                },
            }
        };
        
        Ok(Self {
            data_path,
            learning_data: Arc::new(RwLock::new(learning_data)),
        })
    }
    
    /// Learn from a generation
    pub async fn learn_from_generation(
        &self,
        original_prompt: &str,
        enhanced_prompt: &str,
        metadata: &crate::GenerationMetadata,
    ) -> Result<()> {
        let mut data = self.learning_data.write().await;
        
        // Update generation metrics
        data.generation_metrics.total_generations += 1;
        
        // Update average time (running average)
        let n = data.generation_metrics.total_generations as f32;
        data.generation_metrics.average_time_ms = 
            (data.generation_metrics.average_time_ms * (n - 1.0) + metadata.generation_time_ms as f32) / n;
        
        // Track dimension usage
        let dimension_key = format!("{}x{}", metadata.dimensions.0, metadata.dimensions.1);
        *data.generation_metrics.dimension_distribution.entry(dimension_key).or_insert(0) += 1;
        
        // Extract and learn patterns
        let base_pattern = self.extract_base_pattern(original_prompt);
        let pattern_entry = data.prompt_patterns
            .entry(base_pattern.clone())
            .or_insert_with(|| PromptPattern {
                base_pattern: base_pattern.clone(),
                successful_variations: Vec::new(),
                average_generation_time: 0.0,
                usage_count: 0,
            });
        
        pattern_entry.usage_count += 1;
        pattern_entry.average_generation_time = 
            (pattern_entry.average_generation_time * (pattern_entry.usage_count - 1) as f32 
             + metadata.generation_time_ms as f32) / pattern_entry.usage_count as f32;
        
        if !pattern_entry.successful_variations.contains(&enhanced_prompt.to_string()) {
            pattern_entry.successful_variations.push(enhanced_prompt.to_string());
        }
        
        // Learn style effectiveness
        let styles = self.extract_styles(enhanced_prompt);
        for style in styles {
            let effectiveness = data.style_effectiveness.entry(style.clone()).or_insert(0.5);
            // Simple effectiveness update based on generation speed
            let speed_score = 1.0 - (metadata.generation_time_ms as f32 / 10000.0).min(1.0);
            *effectiveness = (*effectiveness * 0.9) + (speed_score * 0.1); // Exponential moving average
            
            *data.generation_metrics.style_distribution.entry(style).or_insert(0) += 1;
        }
        
        drop(data);
        
        // Save learning data
        self.save_data().await?;
        
        Ok(())
    }
    
    /// Extract base pattern from prompt
    fn extract_base_pattern(&self, prompt: &str) -> String {
        // Simple pattern extraction - in production, use NLP
        let words: Vec<&str> = prompt.split_whitespace()
            .filter(|w| w.len() > 3)
            .take(3)
            .collect();
        words.join(" ")
    }
    
    /// Extract style modifiers from prompt
    fn extract_styles(&self, prompt: &str) -> Vec<String> {
        let known_styles = vec![
            "photorealistic", "hyperrealistic", "digital painting",
            "concept art", "illustration", "3d render", "octane render",
            "anime", "cartoon", "oil painting", "watercolor",
        ];
        
        let prompt_lower = prompt.to_lowercase();
        known_styles.into_iter()
            .filter(|style| prompt_lower.contains(style))
            .map(|s| s.to_string())
            .collect()
    }
    
    /// Get learned enhancements for a prompt
    pub async fn get_learned_enhancements(&self, prompt: &str) -> Vec<String> {
        let data = self.learning_data.read().await;
        let base_pattern = self.extract_base_pattern(prompt);
        
        if let Some(pattern) = data.prompt_patterns.get(&base_pattern) {
            // Return successful variations, sorted by relevance
            pattern.successful_variations.clone()
        } else {
            // Return general high-performing styles
            let mut effective_styles: Vec<(String, f32)> = data.style_effectiveness
                .iter()
                .map(|(style, score)| (style.clone(), *score))
                .collect();
            
            effective_styles.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
            
            effective_styles.into_iter()
                .take(3)
                .map(|(style, _)| style)
                .collect()
        }
    }
    
    /// Save learning data to disk
    async fn save_data(&self) -> Result<()> {
        let data = self.learning_data.read().await;
        let json_data = serde_json::to_string_pretty(&*data)?;
        fs::write(&self.data_path, json_data).await?;
        Ok(())
    }
    
    /// Get learning statistics
    pub async fn get_stats(&self) -> LearningData {
        self.learning_data.read().await.clone()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;
    
    #[tokio::test]
    async fn test_learning_system() {
        let temp_dir = TempDir::new().unwrap();
        let learner = ImageLearner::new(temp_dir.path()).await.unwrap();
        
        let metadata = crate::GenerationMetadata {
            prompt: "a beautiful sunset".to_string(),
            enhanced_prompt: "a beautiful sunset, photorealistic, 8k".to_string(),
            model_used: "test".to_string(),
            generation_time_ms: 5000,
            file_size_bytes: 1024,
            dimensions: (512, 512),
            timestamp: 0,
        };
        
        learner.learn_from_generation(
            "a beautiful sunset",
            "a beautiful sunset, photorealistic, 8k",
            &metadata
        ).await.unwrap();
        
        let stats = learner.get_stats().await;
        assert_eq!(stats.generation_metrics.total_generations, 1);
        assert!(stats.prompt_patterns.contains_key("a beautiful sunset"));
    }
}