// Open Source Image Generation with Learning Capabilities

use anyhow::Result;
use reqwest::{header, Client};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

/// Hugging Face Inference API client for open source models
pub struct OpenSourceGenerator {
    client: Client,
    api_token: Option<String>,
    model_id: String,
    generation_history: Arc<RwLock<Vec<GenerationRecord>>>,
    quality_scores: Arc<RwLock<HashMap<String, f32>>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GenerationRecord {
    pub prompt: String,
    pub enhanced_prompt: String,
    pub model_used: String,
    pub generation_time_ms: u64,
    pub quality_score: f32,
    pub user_feedback: Option<UserFeedback>,
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum UserFeedback {
    Excellent,
    Good,
    Average,
    Poor,
}

impl UserFeedback {
    pub fn to_score(&self) -> f32 {
        match self {
            UserFeedback::Excellent => 1.0,
            UserFeedback::Good => 0.8,
            UserFeedback::Average => 0.5,
            UserFeedback::Poor => 0.2,
        }
    }
}

#[derive(Debug, Serialize)]
struct HuggingFaceRequest {
    inputs: String,
    parameters: Option<GenerationParameters>,
    options: Option<RequestOptions>,
}

#[derive(Debug, Serialize)]
struct GenerationParameters {
    negative_prompt: Option<String>,
    width: Option<u32>,
    height: Option<u32>,
    num_inference_steps: Option<u32>,
    guidance_scale: Option<f32>,
}

#[derive(Debug, Serialize)]
struct RequestOptions {
    wait_for_model: bool,
}

impl OpenSourceGenerator {
    /// Create a new open source generator
    pub fn new(api_token: Option<String>) -> Self {
        Self {
            client: Client::new(),
            api_token,
            // Default to Stable Diffusion 2.1
            model_id: "stabilityai/stable-diffusion-2-1".to_string(),
            generation_history: Arc::new(RwLock::new(Vec::new())),
            quality_scores: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    /// Set a different model (e.g., "runwayml/stable-diffusion-v1-5")
    pub fn with_model(mut self, model_id: &str) -> Self {
        self.model_id = model_id.to_string();
        self
    }

    /// Generate image using open source model
    pub async fn generate(
        &self,
        prompt: &str,
        negative_prompt: Option<&str>,
        width: Option<u32>,
        height: Option<u32>,
    ) -> Result<Vec<u8>> {
        let start_time = std::time::Instant::now();

        // For now, use a simple API endpoint
        // In production, we'd use Hugging Face Inference API or run locally
        let enhanced_prompt = self.enhance_prompt_with_learning(prompt).await;

        // If no API token, generate a placeholder
        if self.api_token.is_none() {
            println!("🎨 No API token provided, generating placeholder image");
            return self
                .generate_placeholder(
                    &enhanced_prompt,
                    width.unwrap_or(512),
                    height.unwrap_or(512),
                )
                .await;
        }

        let request = HuggingFaceRequest {
            inputs: enhanced_prompt.clone(),
            parameters: Some(GenerationParameters {
                negative_prompt: negative_prompt.map(|s| s.to_string()),
                width,
                height,
                num_inference_steps: Some(50),
                guidance_scale: Some(7.5),
            }),
            options: Some(RequestOptions {
                wait_for_model: true,
            }),
        };

        let response = self
            .client
            .post(format!(
                "https://api-inference.huggingface.co/models/{}",
                self.model_id
            ))
            .header(
                header::AUTHORIZATION,
                format!("Bearer {}", self.api_token.as_ref().unwrap()),
            )
            .json(&request)
            .send()
            .await?;

        if !response.status().is_success() {
            let error_text = response.text().await?;
            return Err(anyhow::anyhow!("API request failed: {}", error_text));
        }

        let image_data = response.bytes().await?.to_vec();
        let generation_time = start_time.elapsed().as_millis() as u64;

        // Record generation for learning
        self.record_generation(
            prompt,
            &enhanced_prompt,
            generation_time,
            0.7, // Default quality score
        )
        .await?;

        Ok(image_data)
    }

    /// Enhance prompt using learned patterns
    async fn enhance_prompt_with_learning(&self, prompt: &str) -> String {
        let history = self.generation_history.read().await;
        let quality_scores = self.quality_scores.read().await;

        // Find similar successful prompts
        let mut best_patterns: Vec<(String, f32)> = Vec::new();

        for record in history.iter() {
            if record.quality_score > 0.8 {
                let similarity = self.calculate_similarity(prompt, &record.prompt);
                if similarity > 0.6 {
                    // Extract enhancement patterns
                    let _patterns =
                        self.extract_enhancement_patterns(&record.prompt, &record.enhanced_prompt);
                    for pattern in patterns {
                        best_patterns.push((pattern, record.quality_score * similarity));
                    }
                }
            }
        }

        // Sort by score
        best_patterns.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());

        // Apply top patterns
        let mut enhanced = prompt.to_string();

        // Add learned quality modifiers
        let quality_modifiers = vec![
            "highly detailed",
            "professional",
            "8k resolution",
            "masterpiece",
            "best quality",
            "sharp focus",
            "intricate details",
        ];

        // Select modifiers based on learning
        for modifier in quality_modifiers {
            if let Some(score) = quality_scores.get(modifier) {
                if *score > 0.7 && !enhanced.contains(modifier) {
                    enhanced.push_str(&format!(", {modifier}"));
                }
            }
        }

        // Add style if not present
        if !enhanced.contains("style") && !enhanced.contains("art") {
            enhanced.push_str(", digital art");
        }

        enhanced
    }

    /// Calculate similarity between prompts
    fn calculate_similarity(&self, prompt1: &str, prompt2: &str) -> f32 {
        let words1: std::collections::HashSet<&str> = prompt1.split_whitespace().collect();
        let words2: std::collections::HashSet<&str> = prompt2.split_whitespace().collect();

        let intersection = words1.intersection(&words2).count() as f32;
        let union = words1.union(&words2).count() as f32;

        if union > 0.0 {
            intersection / union
        } else {
            0.0
        }
    }

    /// Extract enhancement patterns from prompt pairs
    fn extract_enhancement_patterns(&self, original: &str, enhanced: &str) -> Vec<String> {
        let original_words: std::collections::HashSet<&str> = original.split_whitespace().collect();
        let enhanced_words: std::collections::HashSet<&str> = enhanced.split_whitespace().collect();

        enhanced_words
            .difference(&original_words)
            .map(|&word| word.to_string())
            .collect()
    }

    /// Record generation for learning
    async fn record_generation(
        &self,
        original_prompt: &str,
        enhanced_prompt: &str,
        generation_time: u64,
        quality_score: f32,
    ) -> Result<()> {
        let record = GenerationRecord {
            prompt: original_prompt.to_string(),
            enhanced_prompt: enhanced_prompt.to_string(),
            model_used: self.model_id.clone(),
            generation_time_ms: generation_time,
            quality_score,
            user_feedback: None,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };

        self.generation_history.write().await.push(record);

        // Update quality scores for used modifiers
        let modifiers = self.extract_enhancement_patterns(original_prompt, enhanced_prompt);
        let mut scores = self.quality_scores.write().await;
        for modifier in modifiers {
            let score = scores.entry(modifier).or_insert(0.5);
            *score = (*score * 0.9) + (quality_score * 0.1); // Exponential moving average
        }

        Ok(())
    }

    /// Update feedback for a generation to improve learning
    pub async fn update_feedback(&self, prompt: &str, feedback: UserFeedback) -> Result<()> {
        let mut history = self.generation_history.write().await;

        // Find the most recent generation with this prompt
        if let Some(record) = history.iter_mut().rev().find(|r| r.prompt == prompt) {
            record.user_feedback = Some(feedback.clone());
            record.quality_score = feedback.to_score();

            // Update modifier scores based on feedback
            let _modifiers =
                self.extract_enhancement_patterns(&record.prompt, &record.enhanced_prompt);
            let mut scores = self.quality_scores.write().await;

            for modifier in modifiers {
                let score = scores.entry(modifier).or_insert(0.5);
                *score = (*score * 0.8) + (feedback.to_score() * 0.2);
            }
        }

        Ok(())
    }

    /// Generate a placeholder image when no API is available
    async fn generate_placeholder(
        &self,
        prompt: &str,
        width: u32,
        height_: u32,
    ) -> Result<Vec<u8>> {
        use sha2::{Digest, Sha256};

        // Generate colors from prompt
        let mut hasher = Sha256::new();
        hasher.update(prompt.as_bytes());
        let hash = hasher.finalize();

        // Create more vibrant colors
        let r_base = 100 + (hash[0] / 2);
        let g_base = 100 + (hash[1] / 2);
        let b_base = 100 + (hash[2] / 2);
        let pattern_type = hash[3] % 4;

        let mut image_data = Vec::with_capacity((width * height * 3) as usize);

        for y in 0..height {
            for x in 0..width {
                let (r, g, b) = match pattern_type {
                    0 => {
                        // Gradient
                        let fx = x as f32 / width as f32;
                        let fy = y as f32 / height as f32;
                        (
                            (r_base as f32 * (1.0 - fx) + 255.0 * fx) as u8,
                            (g_base as f32 * (1.0 - fy) + 255.0 * fy) as u8,
                            (b_base as f32 * (fx + fy) / 2.0) as u8,
                        )
                    }
                    1 => {
                        // Circular pattern
                        let cx = width as f32 / 2.0;
                        let cy = height as f32 / 2.0;
                        let dist = ((x as f32 - cx).powi(2) + (y as f32 - cy).powi(2)).sqrt();
                        let max_dist = (cx.powi(2) + cy.powi(2)).sqrt();
                        let factor = 1.0 - (dist / max_dist).min(1.0);
                        (
                            (r_base as f32 * factor + 50.0 * (1.0 - factor)) as u8,
                            (g_base as f32 * factor + 50.0 * (1.0 - factor)) as u8,
                            (b_base as f32 * factor + 50.0 * (1.0 - factor)) as u8,
                        )
                    }
                    2 => {
                        // Wave pattern
                        let wave = ((x as f32 * 0.1).sin() + (y as f32 * 0.1).cos()) / 2.0 + 0.5;
                        (
                            (r_base as f32 * wave + 128.0 * (1.0 - wave)) as u8,
                            (g_base as f32 * wave + 128.0 * (1.0 - wave)) as u8,
                            (b_base as f32 * wave + 128.0 * (1.0 - wave)) as u8,
                        )
                    }
                    _ => {
                        // Noise pattern
                        let noise = ((x * y) % 255) as f32 / 255.0;
                        (
                            (r_base as f32 * (1.0 - noise) + 255.0 * noise) as u8,
                            (g_base as f32 * (1.0 - noise) + 255.0 * noise) as u8,
                            (b_base as f32 * (1.0 - noise) + 255.0 * noise) as u8,
                        )
                    }
                };

                image_data.push(r);
                image_data.push(g);
                image_data.push(b);
            }
        }

        // Convert to PNG with better visual
        use image::{ImageBuffer, Rgb};

        // Create a cleaner image
        let mut clean_img = ImageBuffer::<Rgb<u8>, Vec<u8>>::new(width, height);

        // Fill with gradient
        for y in 0..height {
            for x in 0..width {
                let idx = ((y * width + x) * 3) as usize;
                if idx + 2 < image_data.len() {
                    clean_img.put_pixel(
                        x,
                        y,
                        Rgb([image_data[idx], image_data[idx + 1], image_data[idx + 2]]),
                    );
                }
            }
        }

        // Add border for visibility
        for x in 0..width {
            clean_img.put_pixel(x, 0, Rgb([255, 255, 255]));
            clean_img.put_pixel(x, height - 1, Rgb([255, 255, 255]));
        }
        for y in 0..height {
            clean_img.put_pixel(0, y, Rgb([255, 255, 255]));
            clean_img.put_pixel(width - 1, y, Rgb([255, 255, 255]));
        }

        // Add text area at bottom
        let text_height = 60;
        if height > text_height {
            for y in (height - text_height)..height {
                for x in 0..width {
                    let pixel = clean_img.get_pixel(x, y);
                    clean_img.put_pixel(
                        x,
                        y,
                        Rgb([
                            (pixel[0] as f32 * 0.3) as u8,
                            (pixel[1] as f32 * 0.3) as u8,
                            (pixel[2] as f32 * 0.3) as u8,
                        ]),
                    );
                }
            }
        }

        let mut png_data = Vec::new();
        clean_img.write_to(
            &mut std::io::Cursor::new(&mut png_data),
            image::ImageFormat::Png,
        )?;

        println!("🎨 Generated placeholder image for: {prompt}");
        Ok(png_data)
    }

    /// Get learning statistics
    pub async fn get_learning_stats(&self) -> LearningStats {
        let history = self.generation_history.read().await;
        let quality_scores = self.quality_scores.read().await;

        let total_generations = history.len();
        let avg_quality = if total_generations > 0 {
            history.iter().map(|r| r.quality_score).sum::<f32>() / total_generations as f32
        } else {
            0.0
        };

        let excellent_count = history
            .iter()
            .filter(|r| matches!(r.user_feedback, Some(UserFeedback::Excellent)))
            .count();

        let top_modifiers: Vec<(String, f32)> = quality_scores
            .iter()
            .map(|(k, v)| (k.clone(), *v))
            .filter(|(_, score)| *score > 0.7)
            .collect();

        LearningStats {
            total_generations,
            average_quality: avg_quality,
            excellent_generations: excellent_count,
            top_performing_modifiers: top_modifiers,
            model_used: self.model_id.clone(),
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct LearningStats {
    pub total_generations: usize,
    pub average_quality: f32,
    pub excellent_generations: usize,
    pub top_performing_modifiers: Vec<(String, f32)>,
    pub model_used: String,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_placeholder_generation() {
        let generator = OpenSourceGenerator::new(None);
        let data = generator
            .generate_placeholder("test prompt", 256, 256)
            .await
            .unwrap();
        assert!(!data.is_empty());
    }

    #[tokio::test]
    async fn test_prompt_enhancement() {
        let generator = OpenSourceGenerator::new(None);
        let enhanced = generator.enhance_prompt_with_learning("a cat").await;
        assert!(enhanced.contains("a cat"));
        assert!(enhanced.len() > 5); // Should add some modifiers
    }
}
