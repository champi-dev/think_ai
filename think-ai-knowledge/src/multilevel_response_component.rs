//! Multi-Level Cached Response Component
//! 
//! This component uses the multi-level cache system to provide O(1) responses
//! by pre-computing and caching responses at word, phrase, paragraph, and full message levels.

use crate::response_generator::{ResponseComponent, ResponseContext};
use crate::multilevel_cache::{MultiLevelCache, CachedResponse, ResponseType, CacheLevel};
use std::sync::{Arc, RwLock};
use std::collections::HashMap;

/// Response component that uses multi-level caching for O(1) responses
pub struct MultiLevelResponseComponent {
    cache: Arc<RwLock<MultiLevelCache>>,
    learning_enabled: bool,
}

impl MultiLevelResponseComponent {
    pub fn new() -> Self {
        println!("🚀 INITIALIZING MultiLevelResponseComponent");
        Self {
            cache: Arc::new(RwLock::new(MultiLevelCache::new())),
            learning_enabled: true,
        }
    }
    
    /// Create with custom cache
    pub fn with_cache(cache: Arc<RwLock<MultiLevelCache>>) -> Self {
        Self {
            cache,
            learning_enabled: true,
        }
    }
    
    /// Enable or disable learning from interactions
    pub fn set_learning_enabled(&mut self, enabled: bool) {
        self.learning_enabled = enabled;
    }
    
    /// Add a new response pattern to the cache
    pub fn add_pattern(&self, level: CacheLevel, pattern: String, response: CachedResponse) {
        // Check if the response has the template bug
        if response.content.contains("the!") || response.content.contains("about !") {
            println!("⚠️ Rejecting broken template response: {}", response.content);
            return;
        }
        
        if let Ok(mut cache) = self.cache.write() {
            cache.add_response(level, pattern, response);
        }
    }
    
    /// Get cache statistics
    pub fn get_cache_stats(&self) -> Option<crate::multilevel_cache::CacheStats> {
        if let Ok(cache) = self.cache.read() {
            Some(cache.get_stats())
        } else {
            None
        }
    }
    
    /// Learn from user interaction and response quality
    pub fn learn_from_interaction(&self, query: &str, response: &str, user_satisfaction: f32) {
        if !self.learning_enabled {
            return;
        }
        
        // Extract patterns that worked well and cache them for future use
        if user_satisfaction > 0.7 {
            self.cache_successful_pattern(query, response, user_satisfaction);
        }
    }
    
    /// Cache a successful response pattern for future use
    fn cache_successful_pattern(&self, query: &str, response: &str, satisfaction: f32) {
        let query_normalized = query.to_lowercase().trim().to_string();
        
        // Create cached response with high scores since it was successful
        let cached_response = CachedResponse {
            content: response.to_string(),
            confidence: satisfaction,
            context_relevance: satisfaction,
            engagement_score: satisfaction,
            response_type: self.classify_response_type(response),
            source_level: CacheLevel::FullMessage,
        };
        
        if let Ok(mut cache) = self.cache.write() {
            cache.add_response(CacheLevel::FullMessage, query_normalized, cached_response);
        }
    }
    
    /// Classify the type of response for categorization
    fn classify_response_type(&self, response: &str) -> ResponseType {
        let response_lower = response.to_lowercase();
        
        if response_lower.contains("hello") || response_lower.contains("hi") || response_lower.contains("greetings") {
            ResponseType::Greeting
        } else if response_lower.contains("?") && response_lower.contains("what") {
            ResponseType::Question
        } else if response_lower.contains("code") || response_lower.contains("programming") || response_lower.contains("function") {
            ResponseType::Technical
        } else if response_lower.contains("love") || response_lower.contains("meaning") || response_lower.contains("consciousness") {
            ResponseType::Philosophical
        } else if response_lower.contains("i feel") || response_lower.contains("personal") || response_lower.contains("experience") {
            ResponseType::Personal
        } else if response_lower.contains("explain") || response_lower.contains("because") || response_lower.contains("definition") {
            ResponseType::Explanation
        } else {
            ResponseType::Conversational
        }
    }
    
    /// Extract key phrases from a query for better pattern matching
    fn extract_key_phrases(&self, query: &str) -> Vec<String> {
        let mut phrases = Vec::new();
        let query_lower = query.to_lowercase();
        let words: Vec<&str> = query_lower.split_whitespace().collect();
        
        // Extract 2-word phrases
        for i in 0..words.len().saturating_sub(1) {
            phrases.push(format!("{} {}", words[i], words[i + 1]));
        }
        
        // Extract 3-word phrases
        for i in 0..words.len().saturating_sub(2) {
            phrases.push(format!("{} {} {}", words[i], words[i + 1], words[i + 2]));
        }
        
        // Extract question starters
        if words.len() >= 2 {
            let starter = format!("{} {}", words[0], words[1]);
            if ["what is", "what means", "how do", "can you", "can u", "do you"].contains(&starter.as_str()) {
                phrases.push(starter);
            }
        }
        
        phrases
    }
    
    /// Enhance cache with dynamic patterns based on query analysis
    pub fn enhance_cache_with_query(&self, query: &str) {
        let key_phrases = self.extract_key_phrases(query);
        
        // Add phrase-level patterns if not already cached
        for phrase in key_phrases {
            let response = self.generate_phrase_response(&phrase);
            if let Some(cached_response) = response {
                if let Ok(mut cache) = self.cache.write() {
                    cache.add_response(CacheLevel::Phrase, phrase, cached_response);
                }
            }
        }
        
        // Add word-level patterns
        let query_lower = query.to_lowercase();
        let words: Vec<&str> = query_lower.split_whitespace().collect();
        for word in words {
            if word.len() > 3 {
                let response = self.generate_word_response(word);
                if let Some(cached_response) = response {
                    if let Ok(mut cache) = self.cache.write() {
                        cache.add_response(CacheLevel::Word, word.to_string(), cached_response);
                    }
                }
            }
        }
    }
    
    /// Generate a contextual response for a phrase pattern
    fn generate_phrase_response(&self, phrase: &str) -> Option<CachedResponse> {
        // No template generation - purely knowledge-driven system
        None
    }
    
    /// Generate a contextual response for a word pattern
    fn generate_word_response(&self, word: &str) -> Option<CachedResponse> {
        // No template generation - purely knowledge-driven system
        None
    }
    
    /// Generate response using word-by-word and phrase-by-phrase analysis
    fn generate_multilevel_response(&self, query: &str) -> Option<String> {
        // Disabled verbose logging for production performance
        // println!("   🔬 Analyzing query components:");
        
        // 1. Word-level analysis
        let query_lower = query.to_lowercase();
        let words: Vec<&str> = query_lower.split_whitespace().collect();
        // println!("   📝 Words: {:?}", words);
        
        let mut word_responses = Vec::new();
        for word in &words {
            if let Some(response) = self.generate_word_response(word) {
                // println!("   🎯 Word '{}' -> {}", word, response.content.chars().take(50).collect::<String>());
                word_responses.push(response);
            }
        }
        
        // 2. Phrase-level analysis  
        let phrases = self.extract_key_phrases(query);
        // println!("   🔗 Phrases: {:?}", phrases);
        
        let mut phrase_responses = Vec::new();
        for phrase in &phrases {
            if let Some(response) = self.generate_phrase_response(phrase) {
                // println!("   🎯 Phrase '{}' -> {}", phrase, response.content.chars().take(50).collect::<String>());
                phrase_responses.push(response);
            }
        }
        
        // 3. Intelligent combination of responses
        if !phrase_responses.is_empty() {
            // Prefer phrase-level responses
            let best_phrase = phrase_responses.into_iter()
                .max_by(|a, b| a.confidence.partial_cmp(&b.confidence).unwrap_or(std::cmp::Ordering::Equal))?;
            // println!("   ✅ Using best phrase response");
            Some(best_phrase.content)
        } else if !word_responses.is_empty() {
            // Fall back to word-level responses
            let best_word = word_responses.into_iter()
                .max_by(|a, b| a.confidence.partial_cmp(&b.confidence).unwrap_or(std::cmp::Ordering::Equal))?;
            // println!("   ✅ Using best word response");
            Some(best_word.content)
        } else {
            // Generate a dynamic response based on query structure
            // println!("   🤖 Generating dynamic response for novel query");
            self.generate_dynamic_response(query)
        }
    }
    
    /// Generate a dynamic response for completely novel queries
    fn generate_dynamic_response(&self, query: &str) -> Option<String> {
        // No template generation - purely knowledge-driven system
        // If no knowledge is available, return None to let other components handle
        None
    }
    
    /// Check if a response actually answers the question usefully
    fn is_response_useful(&self, query: &str, response: &str) -> bool {
        let response_lower = response.to_lowercase();
        
        // Detect generic unhelpful template responses
        if response_lower.contains("that's a fascinating question") ||
           response_lower.contains("that's an interesting topic") ||
           response_lower.contains("i'd love to explore this with you") ||
           response_lower.contains("could you tell me a bit more") ||
           response_lower.contains("let me think about that concept") ||
           response_lower.contains("what specific aspect interests you") {
            return false;
        }
        
        // For "what is" questions, check if response is substantial and informative
        let query_lower = query.to_lowercase();
        if query_lower.starts_with("what is") || query_lower.starts_with("what's") {
            // Response should be substantial (more than a template) and not just questions back
            return response_lower.len() > 50 && 
                   !response_lower.contains("?") && 
                   !response_lower.contains("what would you like to know");
        }
        
        true // Default to useful for other types of queries
    }
}

impl ResponseComponent for MultiLevelResponseComponent {
    fn name(&self) -> &'static str {
        "MultiLevelCache"
    }
    
    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase();
        
        // If we have relevant knowledge available for ANY query, defer to knowledge base
        if !context.relevant_nodes.is_empty() {
            return 0.85; // Lower priority to let knowledge base handle any question with relevant knowledge
        }
        
        // This component should have HIGHEST priority to ensure multi-level caching works for other queries
        if let Ok(cache) = self.cache.read() {
            if let Some(_response) = cache.get_best_response(query) {
                // Return MAXIMUM score for cached responses - cache hits should ALWAYS win
                0.995 // MAXIMUM score to beat all other components when we have a cache hit
            } else {
                // Even for uncached queries, score HIGHEST so we can generate patterns
                0.99 // HIGHEST priority to beat SimpleCache
            }
        } else {
            0.9 // Still high priority even if lock fails
        }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // First, try to enhance cache with patterns from this query
        self.enhance_cache_with_query(query);
        
        // Then get the best cached response
        if let Ok(cache) = self.cache.read() {
            if let Some(response) = cache.get_best_response(query) {
                // Check if the cached response has the broken template bug
                if response.content.contains("the!") || response.content.contains("about !") {
                    // Regenerate the response if it has the template bug
                    return self.generate_multilevel_response(query);
                }
                
                // Check if cached response is useful when we have relevant knowledge available
                if !context.relevant_nodes.is_empty() && !self.is_response_useful(query, &response.content) {
                    println!("🚫 Cache response not useful, falling back to knowledge base");
                    return None; // Let knowledge base handle it
                }
                
                Some(response.content)
            } else {
                // Do the actual multi-level analysis
                self.generate_multilevel_response(query)
            }
        } else {
            None
        }
    }
    
    
    fn metadata(&self) -> HashMap<String, String> {
        let mut metadata = HashMap::new();
        metadata.insert("type".to_string(), "multilevel_cache".to_string());
        metadata.insert("learning_enabled".to_string(), self.learning_enabled.to_string());
        
        if let Some(stats) = self.get_cache_stats() {
            metadata.insert("word_patterns".to_string(), stats.total_word_patterns.to_string());
            metadata.insert("phrase_patterns".to_string(), stats.total_phrase_patterns.to_string());
            metadata.insert("paragraph_patterns".to_string(), stats.total_paragraph_patterns.to_string());
            metadata.insert("full_message_patterns".to_string(), stats.total_full_message_patterns.to_string());
            metadata.insert("total_responses".to_string(), 
                (stats.total_word_responses + stats.total_phrase_responses + stats.total_paragraph_responses).to_string());
        }
        
        metadata
    }
}

impl Default for MultiLevelResponseComponent {
    fn default() -> Self {
        Self::new()
    }
}