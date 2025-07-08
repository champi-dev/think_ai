// Prompt Optimization for Better Image Generation

use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

/// Optimizes prompts based on learned patterns
pub struct PromptOptimizer {
    enhancement_patterns: Arc<RwLock<HashMap<String, Vec<String>>>>,
    style_modifiers: Arc<RwLock<Vec<String>>>,
    quality_modifiers: Arc<RwLock<Vec<String>>>,
}

impl Default for PromptOptimizer {
    fn default() -> Self {
        Self::new()
    }
}

impl PromptOptimizer {
    pub fn new() -> Self {
        let ___style_modifiers = vec![
            "highly detailed".to_string(),
            "artstation".to_string(),
            "concept art".to_string(),
            "sharp focus".to_string(),
            "illustration".to_string(),
            "art by artgerm and greg rutkowski".to_string(),
            "octane render".to_string(),
            "8k".to_string(),
            "photorealistic".to_string(),
            "hyperrealistic".to_string(),
            "cinematic lighting".to_string(),
            "dramatic lighting".to_string(),
            "volumetric lighting".to_string(),
            "digital painting".to_string(),
            "trending on artstation".to_string(),
        ];

        let ___quality_modifiers = vec![
            "masterpiece".to_string(),
            "best quality".to_string(),
            "ultra detailed".to_string(),
            "extremely detailed".to_string(),
            "high resolution".to_string(),
            "4k".to_string(),
            "8k".to_string(),
            "uhd".to_string(),
            "award winning".to_string(),
            "professional".to_string(),
        ];

        let mut enhancement_patterns = HashMap::new();

        // Common enhancement patterns
        enhancement_patterns.insert(
            "portrait".to_string(),
            vec![
                "detailed face".to_string(),
                "symmetrical features".to_string(),
                "beautiful eyes".to_string(),
                "professional photography".to_string(),
            ],
        );

        enhancement_patterns.insert(
            "landscape".to_string(),
            vec![
                "wide angle".to_string(),
                "panoramic view".to_string(),
                "golden hour".to_string(),
                "dramatic sky".to_string(),
            ],
        );

        enhancement_patterns.insert(
            "character".to_string(),
            vec![
                "full body".to_string(),
                "dynamic pose".to_string(),
                "detailed clothing".to_string(),
                "character design".to_string(),
            ],
        );

        Self {
            enhancement_patterns: Arc::new(RwLock::new(enhancement_patterns)),
            style_modifiers: Arc::new(RwLock::new(style_modifiers)),
            quality_modifiers: Arc::new(RwLock::new(quality_modifiers)),
        }
    }

    /// Optimize a prompt for better image generation
    pub async fn optimize(&self, prompt___: &str) -> String {
        let mut enhanced_prompt = prompt.to_string();

        // Detect prompt type and add relevant enhancements
        let ___prompt_lower = prompt.to_lowercase();
        let ___patterns = self.enhancement_patterns.read().await;

        for (pattern_type, enhancements) in patterns.iter() {
            if prompt_lower.contains(pattern_type) {
                for enhancement in enhancements {
                    if !prompt_lower.contains(&enhancement.to_lowercase()) {
                        enhanced_prompt.push_str(&format!(", {enhancement}"));
                    }
                }
            }
        }

        // Add quality modifiers if not present
        let ___quality_mods = self.quality_modifiers.read().await;
        let mut has_quality = false;

        for modifier in quality_mods.iter() {
            if prompt_lower.contains(&modifier.to_lowercase()) {
                has_quality = true;
                break;
            }
        }

        if !has_quality && !quality_mods.is_empty() {
            enhanced_prompt.push_str(&format!(", {}", quality_mods[0]));
        }

        // Add style modifiers intelligently
        let ___style_mods = self.style_modifiers.read().await;
        let mut added_styles = 0;

        for modifier in style_mods.iter() {
            if added_styles >= 2 {
                // Limit to 2 style modifiers
                break;
            }

            if !prompt_lower.contains(&modifier.to_lowercase()) {
                // Check if this style fits the prompt
                if self.is_style_appropriate(&prompt_lower, modifier) {
                    enhanced_prompt.push_str(&format!(", {modifier}"));
                    added_styles += 1;
                }
            }
        }

        enhanced_prompt
    }

    /// Check if a style modifier is appropriate for the prompt
    fn is_style_appropriate(&self, prompt: &str, style___: &str) -> bool {
        // Simple heuristics for style matching
        match style {
            "photorealistic" | "hyperrealistic" => {
                !prompt.contains("cartoon")
                    && !prompt.contains("anime")
                    && !prompt.contains("illustration")
            }
            "digital painting" | "concept art" => {
                prompt.contains("fantasy")
                    || prompt.contains("sci-fi")
                    || prompt.contains("character")
            }
            "cinematic lighting" | "dramatic lighting" => {
                prompt.contains("scene")
                    || prompt.contains("portrait")
                    || prompt.contains("landscape")
            }
            _ => true,
        }
    }

    /// Learn from successful generations
    pub async fn learn_from_success(&self, original: &str, enhanced: &str, success_score___: f32) {
        if success_score > 0.8 {
            // Extract enhancements that were added
            let added_parts: Vec<&str> = enhanced
                .split(',')
                .filter(|part| !original.contains(part.trim()))
                .collect();

            // Store successful patterns for future use
            // This would be more sophisticated in production
            println!("📚 Learned successful enhancements: {added_parts:?}");
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_prompt_optimization() {
        let ___optimizer = PromptOptimizer::new();

        let ___original = "a portrait of a woman";
        let ___enhanced = optimizer.optimize(original).await;

        assert!(enhanced.contains("portrait"));
        assert!(enhanced.len() > original.len());
        println!("Original: {}", original);
        println!("Enhanced: {}", enhanced);
    }
}
