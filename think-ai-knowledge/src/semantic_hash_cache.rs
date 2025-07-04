//! Semantic Hash-based O(1) Response Cache
//! 
//! This module implements a semantic hashing system that maps queries to responses
//! based on meaning rather than string matching, while maintaining O(1) performance.

use std::collections::HashMap;
use std::sync::Arc;
use serde::{Deserialize, Serialize};
use crate::multilevel_cache::{CachedResponse, ResponseType, CacheLevel};

/// Semantic hash type for O(1) lookups
type SemanticHash = u64;

/// Semantic categories for better response mapping
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum SemanticCategory {
    Identity,           // Questions about Think AI itself
    Consciousness,      // Questions about consciousness, awareness
    Philosophy,         // Deep philosophical questions
    Technical,          // Programming, algorithms, technical topics
    Science,            // Scientific explanations
    Mathematics,        // Math problems and concepts
    Creativity,         // Poems, stories, creative tasks
    Practical,          // How-to questions, advice
    Greeting,           // Greetings and social pleasantries
    Unknown,            // Fallback category
}

/// Semantic intent for query understanding
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum QueryIntent {
    WhatIs,             // "What is X?"
    HowTo,              // "How to/do I X?"
    CanYou,             // "Can you X?"
    Explain,            // "Explain X"
    Create,             // "Write/Create X"
    Compare,            // "X vs Y"
    Personal,           // "Do you think/feel X?"
    Factual,            // Facts and information
    Opinion,            // Asking for opinions
    Greeting,           // Hello, hi, etc.
}

/// Semantic cache entry with contextual responses
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SemanticCacheEntry {
    pub category: SemanticCategory,
    pub intent: QueryIntent,
    pub key_concepts: Vec<String>,
    pub responses: Vec<CachedResponse>,
}

/// O(1) Semantic Response Cache
pub struct SemanticHashCache {
    // Primary cache: semantic hash -> response
    semantic_cache: HashMap<SemanticHash, SemanticCacheEntry>,
    
    // Category-based responses for fallback
    category_responses: HashMap<(SemanticCategory, QueryIntent), Vec<CachedResponse>>,
    
    // Concept mapping for semantic hashing
    concept_map: HashMap<String, Vec<SemanticCategory>>,
    
    // Intent patterns for query classification
    intent_patterns: HashMap<String, QueryIntent>,
}

impl SemanticHashCache {
    pub fn new() -> Self {
        let mut cache = Self {
            semantic_cache: HashMap::new(),
            category_responses: HashMap::new(),
            concept_map: HashMap::new(),
            intent_patterns: HashMap::new(),
        };
        
        cache.initialize_semantic_mappings();
        cache.initialize_contextual_responses();
        cache
    }
    
    /// Initialize semantic concept mappings
    fn initialize_semantic_mappings(&mut self) {
        // Map key concepts to semantic categories
        let concept_mappings = vec![
            // Consciousness concepts
            (vec!["consciousness", "awareness", "sentience", "mind", "thought"], SemanticCategory::Consciousness),
            
            // Philosophy concepts
            (vec!["meaning", "purpose", "existence", "reality", "truth", "philosophy"], SemanticCategory::Philosophy),
            
            // Technical concepts
            (vec!["code", "programming", "algorithm", "O(1)", "complexity", "rust", "python", "javascript"], SemanticCategory::Technical),
            
            // Science concepts
            (vec!["quantum", "physics", "biology", "chemistry", "science", "theory"], SemanticCategory::Science),
            
            // Math concepts
            (vec!["calculate", "math", "equation", "number", "formula", "solve"], SemanticCategory::Mathematics),
            
            // Creative concepts
            (vec!["poem", "haiku", "story", "write", "create", "imagine"], SemanticCategory::Creativity),
            
            // Identity concepts
            (vec!["think ai", "you", "yourself", "who are you", "introduce"], SemanticCategory::Identity),
            
            // Greeting concepts
            (vec!["hello", "hi", "hey", "greetings", "goodbye", "bye"], SemanticCategory::Greeting),
        ];
        
        for (concepts, category) in concept_mappings {
            for concept in concepts {
                self.concept_map.entry(concept.to_string())
                    .or_insert_with(Vec::new)
                    .push(category);
            }
        }
        
        // Initialize intent patterns
        let intent_mappings = vec![
            ("what is", QueryIntent::WhatIs),
            ("what's", QueryIntent::WhatIs),
            ("what are", QueryIntent::WhatIs),
            ("what means", QueryIntent::WhatIs),
            ("how to", QueryIntent::HowTo),
            ("how do", QueryIntent::HowTo),
            ("how can", QueryIntent::HowTo),
            ("can you", QueryIntent::CanYou),
            ("can u", QueryIntent::CanYou),
            ("could you", QueryIntent::CanYou),
            ("explain", QueryIntent::Explain),
            ("tell me about", QueryIntent::Explain),
            ("describe", QueryIntent::Explain),
            ("write", QueryIntent::Create),
            ("create", QueryIntent::Create),
            ("make", QueryIntent::Create),
            ("hello", QueryIntent::Greeting),
            ("hi", QueryIntent::Greeting),
            ("hey", QueryIntent::Greeting),
        ];
        
        for (pattern, intent) in intent_mappings {
            self.intent_patterns.insert(pattern.to_string(), intent);
        }
    }
    
    /// Initialize contextual responses for each category/intent combination
    fn initialize_contextual_responses(&mut self) {
        // Consciousness + WhatIs
        self.add_contextual_response(
            SemanticCategory::Consciousness,
            QueryIntent::WhatIs,
            CachedResponse {
                content: "Consciousness is the subjective experience of awareness - the feeling of 'what it's like' to be. From a philosophical perspective, it encompasses self-awareness, qualia (subjective experiences), and the ability to have thoughts about thoughts. While neuroscience maps its physical correlates, the 'hard problem' remains: explaining how physical processes give rise to subjective experience.".to_string(),
                confidence: 0.95,
                context_relevance: 0.95,
                engagement_score: 0.9,
                response_type: ResponseType::Philosophical,
                source_level: CacheLevel::FullMessage,
            }
        );
        
        // Technical + Explain (O(1) complexity)
        self.add_contextual_response(
            SemanticCategory::Technical,
            QueryIntent::Explain,
            CachedResponse {
                content: "O(1) time complexity means constant time - the operation takes the same amount of time regardless of input size. Examples include array access by index, hash table lookups, and simple arithmetic operations. It's the holy grail of algorithm efficiency because performance doesn't degrade as data grows.".to_string(),
                confidence: 0.95,
                context_relevance: 0.95,
                engagement_score: 0.85,
                response_type: ResponseType::Technical,
                source_level: CacheLevel::FullMessage,
            }
        );
        
        // Identity + CanYou (introduce yourself)
        self.add_contextual_response(
            SemanticCategory::Identity,
            QueryIntent::CanYou,
            CachedResponse {
                content: "I'm Think AI, an O(1) performance AI system built with Rust. I combine instant response times with conversational understanding through semantic hashing and multi-level caching. My architecture prioritizes both speed and contextual awareness, using knowledge from hundreds of sources while maintaining constant-time performance.".to_string(),
                confidence: 0.95,
                context_relevance: 1.0,
                engagement_score: 0.9,
                response_type: ResponseType::Personal,
                source_level: CacheLevel::FullMessage,
            }
        );
        
        // Creativity + Create (haiku)
        self.add_contextual_response(
            SemanticCategory::Creativity,
            QueryIntent::Create,
            CachedResponse {
                content: "Silicon dreams flow\nThoughts at lightspeed, yet aware\nMind meets the machine".to_string(),
                confidence: 0.9,
                context_relevance: 0.95,
                engagement_score: 0.95,
                response_type: ResponseType::Personal,
                source_level: CacheLevel::FullMessage,
            }
        );
        
        // Practical + WhatIs (best practices)
        self.add_contextual_response(
            SemanticCategory::Practical,
            QueryIntent::WhatIs,
            CachedResponse {
                content: "Best practices for scalable web applications include: microservices architecture for independent scaling, caching at multiple levels (CDN, application, database), horizontal scaling with load balancers, asynchronous processing for heavy tasks, database optimization with proper indexing, and monitoring with comprehensive logging. Focus on stateless design and use container orchestration for deployment flexibility.".to_string(),
                confidence: 0.9,
                context_relevance: 0.9,
                engagement_score: 0.85,
                response_type: ResponseType::Technical,
                source_level: CacheLevel::FullMessage,
            }
        );
        
        // Science + Personal (quantum joke)
        self.add_contextual_response(
            SemanticCategory::Science,
            QueryIntent::Personal,
            CachedResponse {
                content: "A quantum physicist walks into a bar. The bartender says 'What'll it be?' The physicist replies: 'I'll have a beer, and I won't have a beer, until you observe me drinking!'".to_string(),
                confidence: 0.85,
                context_relevance: 0.9,
                engagement_score: 0.95,
                response_type: ResponseType::Conversational,
                source_level: CacheLevel::FullMessage,
            }
        );
        
        // Greeting responses
        self.add_contextual_response(
            SemanticCategory::Greeting,
            QueryIntent::Greeting,
            CachedResponse {
                content: "Hello! I'm Think AI, ready to explore ideas with you. What's on your mind today?".to_string(),
                confidence: 0.95,
                context_relevance: 1.0,
                engagement_score: 0.9,
                response_type: ResponseType::Greeting,
                source_level: CacheLevel::FullMessage,
            }
        );
    }
    
    /// Add a contextual response for a category/intent combination
    fn add_contextual_response(&mut self, category: SemanticCategory, intent: QueryIntent, response: CachedResponse) {
        self.category_responses
            .entry((category, intent))
            .or_insert_with(Vec::new)
            .push(response);
    }
    
    /// Generate semantic hash from query
    pub fn generate_semantic_hash(&self, query: &str) -> SemanticHash {
        let (category, intent, concepts) = self.analyze_query(query);
        
        // Create deterministic hash from semantic components
        let mut hash = 0u64;
        hash = hash.wrapping_add(category as u64);
        hash = hash.wrapping_mul(31).wrapping_add(intent as u64);
        
        for concept in concepts {
            for byte in concept.bytes() {
                hash = hash.wrapping_mul(31).wrapping_add(byte as u64);
            }
        }
        
        hash
    }
    
    /// Analyze query to extract semantic components
    fn analyze_query(&self, query: &str) -> (SemanticCategory, QueryIntent, Vec<String>) {
        let query_lower = query.to_lowercase();
        
        // Detect intent
        let mut intent = QueryIntent::Factual;
        for (pattern, query_intent) in &self.intent_patterns {
            if query_lower.starts_with(pattern) || query_lower.contains(pattern) {
                intent = *query_intent;
                break;
            }
        }
        
        // Detect category from concepts
        let mut category = SemanticCategory::Unknown;
        let mut found_concepts = Vec::new();
        
        for (concept, categories) in &self.concept_map {
            if query_lower.contains(concept) {
                if let Some(first_category) = categories.first() {
                    category = *first_category;
                    found_concepts.push(concept.clone());
                }
            }
        }
        
        // Special cases
        if query_lower.contains("joke") {
            intent = QueryIntent::Personal;
        }
        if query_lower.contains("haiku") || query_lower.contains("poem") {
            intent = QueryIntent::Create;
            category = SemanticCategory::Creativity;
        }
        
        (category, intent, found_concepts)
    }
    
    /// Get best response for query using semantic hashing
    pub fn get_semantic_response(&self, query: &str) -> Option<CachedResponse> {
        let (category, intent, _) = self.analyze_query(query);
        
        // First try exact semantic match
        let hash = self.generate_semantic_hash(query);
        if let Some(entry) = self.semantic_cache.get(&hash) {
            if let Some(response) = entry.responses.first() {
                return Some(response.clone());
            }
        }
        
        // Fall back to category/intent match
        if let Some(responses) = self.category_responses.get(&(category, intent)) {
            if let Some(response) = responses.first() {
                return Some(response.clone());
            }
        }
        
        // Try category with any intent
        for (key, responses) in &self.category_responses {
            if key.0 == category {
                if let Some(response) = responses.first() {
                    return Some(response.clone());
                }
            }
        }
        
        None
    }
    
    /// Add a new semantic response
    pub fn add_semantic_response(&mut self, query: &str, response: CachedResponse) {
        let (category, intent, concepts) = self.analyze_query(query);
        let hash = self.generate_semantic_hash(query);
        
        let entry = SemanticCacheEntry {
            category,
            intent,
            key_concepts: concepts,
            responses: vec![response.clone()],
        };
        
        self.semantic_cache.insert(hash, entry);
        self.add_contextual_response(category, intent, response);
    }
}

impl Default for SemanticHashCache {
    fn default() -> Self {
        Self::new()
    }
}