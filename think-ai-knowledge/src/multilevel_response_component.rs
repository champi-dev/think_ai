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
        match phrase {
            phrase if phrase.starts_with("what is") => Some(CachedResponse {
                content: format!("That's an interesting question about {}! Let me help you understand that concept.", phrase.strip_prefix("what is ").unwrap_or("")),
                confidence: 0.7,
                context_relevance: 0.8,
                engagement_score: 0.75,
                response_type: ResponseType::Question,
                source_level: CacheLevel::Phrase,
            }),
            phrase if phrase.starts_with("how do") => Some(CachedResponse {
                content: "Great question about process! I'd love to walk through that step by step with you.".to_string(),
                confidence: 0.75,
                context_relevance: 0.8,
                engagement_score: 0.8,
                response_type: ResponseType::Question,
                source_level: CacheLevel::Phrase,
            }),
            _ => None,
        }
    }
    
    /// Generate a contextual response for a word pattern
    fn generate_word_response(&self, word: &str) -> Option<CachedResponse> {
        // Only create word responses for significant terms
        if ["programming", "coding", "python", "javascript", "algorithm", "science", "philosophy", "consciousness", "quantum"].contains(&word) {
            Some(CachedResponse {
                content: format!("I'd be happy to discuss {} with you! What specific aspect interests you most?", word),
                confidence: 0.6,
                context_relevance: 0.7,
                engagement_score: 0.8,
                response_type: if ["programming", "coding", "python", "javascript", "algorithm"].contains(&word) {
                    ResponseType::Technical
                } else {
                    ResponseType::Conversational
                },
                source_level: CacheLevel::Word,
            })
        } else {
            None
        }
    }
    
    /// Generate response using word-by-word and phrase-by-phrase analysis
    fn generate_multilevel_response(&self, query: &str) -> Option<String> {
        println!("   🔬 Analyzing query components:");
        
        // 1. Word-level analysis
        let query_lower = query.to_lowercase();
        let words: Vec<&str> = query_lower.split_whitespace().collect();
        println!("   📝 Words: {:?}", words);
        
        let mut word_responses = Vec::new();
        for word in &words {
            if let Some(response) = self.generate_word_response(word) {
                println!("   🎯 Word '{}' -> {}", word, response.content.chars().take(50).collect::<String>());
                word_responses.push(response);
            }
        }
        
        // 2. Phrase-level analysis  
        let phrases = self.extract_key_phrases(query);
        println!("   🔗 Phrases: {:?}", phrases);
        
        let mut phrase_responses = Vec::new();
        for phrase in &phrases {
            if let Some(response) = self.generate_phrase_response(phrase) {
                println!("   🎯 Phrase '{}' -> {}", phrase, response.content.chars().take(50).collect::<String>());
                phrase_responses.push(response);
            }
        }
        
        // 3. Intelligent combination of responses
        if !phrase_responses.is_empty() {
            // Prefer phrase-level responses
            let best_phrase = phrase_responses.into_iter()
                .max_by(|a, b| a.confidence.partial_cmp(&b.confidence).unwrap_or(std::cmp::Ordering::Equal))?;
            println!("   ✅ Using best phrase response");
            Some(best_phrase.content)
        } else if !word_responses.is_empty() {
            // Fall back to word-level responses
            let best_word = word_responses.into_iter()
                .max_by(|a, b| a.confidence.partial_cmp(&b.confidence).unwrap_or(std::cmp::Ordering::Equal))?;
            println!("   ✅ Using best word response");
            Some(best_word.content)
        } else {
            // Generate a dynamic response based on query structure
            println!("   🤖 Generating dynamic response for novel query");
            self.generate_dynamic_response(query)
        }
    }
    
    /// Generate a dynamic response for completely novel queries
    fn generate_dynamic_response(&self, query: &str) -> Option<String> {
        let query_lower = query.to_lowercase();
        
        if query_lower.starts_with("what is") || query_lower.starts_with("what's") {
            let topic = query_lower.strip_prefix("what is").unwrap_or(
                query_lower.strip_prefix("what's").unwrap_or("")
            ).trim();
            
            Some(format!(
                "That's a fascinating question about {}! {} is a topic that involves many different perspectives and dimensions. I'd love to explore this concept with you. What specifically about {} interests you most? Are you looking for a definition, examples, or perhaps how it relates to other concepts?",
                topic, 
                topic.split_whitespace().next().unwrap_or(topic),
                topic
            ))
        } else if query_lower.starts_with("how") {
            Some("That's a great process-oriented question! I'd love to walk through that step by step with you. Could you tell me a bit more about what specific aspect you're most curious about? Understanding your context will help me give you the most useful explanation.".to_string())
        } else if query_lower.starts_with("why") {
            Some("That's such a thoughtful question about underlying reasons and causes! These 'why' questions often lead to the most interesting discussions because they get at the heart of how things work. What prompted you to think about this? I'd love to explore the reasoning together.".to_string())
        } else {
            Some("That's an interesting topic! I'd love to explore this with you. Could you tell me a bit more about what specific aspect you're most curious about? The more context you give me, the better I can tailor my response to what you're actually looking for.".to_string())
        }
    }
}

impl ResponseComponent for MultiLevelResponseComponent {
    fn name(&self) -> &'static str {
        "MultiLevelCache"
    }
    
    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        // This component should have HIGHEST priority to ensure multi-level caching works
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
    
    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        // First, try to enhance cache with patterns from this query
        self.enhance_cache_with_query(query);
        
        // Then get the best cached response
        if let Ok(cache) = self.cache.read() {
            if let Some(response) = cache.get_best_response(query) {
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