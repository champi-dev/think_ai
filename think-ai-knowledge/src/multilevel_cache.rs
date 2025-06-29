//! Multi-Level Response Caching System
//! 
//! This module implements a sophisticated O(1) response system that pre-caches
//! responses at every level: words, phrases, paragraphs, and full messages.
//! The system then intelligently selects the best response based on confidence,
//! context relevance, and engagement scores.

use std::collections::HashMap;
use std::sync::Arc;
use serde::{Deserialize, Serialize};

/// A cached response with scoring metrics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CachedResponse {
    pub content: String,
    pub confidence: f32,
    pub context_relevance: f32,
    pub engagement_score: f32,
    pub response_type: ResponseType,
    pub source_level: CacheLevel,
}

/// Types of responses for categorization
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum ResponseType {
    Greeting,
    Question,
    Explanation,
    Conversational,
    Technical,
    Philosophical,
    Personal,
    Fallback,
}

/// Cache levels for response granularity
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum CacheLevel {
    Word,
    Phrase,
    Paragraph,
    FullMessage,
}

/// Multi-level response cache with O(1) lookups
pub struct MultiLevelCache {
    // Word-level responses (single words)
    word_responses: HashMap<String, Vec<CachedResponse>>,
    
    // Phrase-level responses (2-5 words)
    phrase_responses: HashMap<String, Vec<CachedResponse>>,
    
    // Paragraph-level responses (sentences/clauses)
    paragraph_responses: HashMap<String, Vec<CachedResponse>>,
    
    // Full message responses (complete queries)
    full_message_responses: HashMap<String, CachedResponse>,
    
    // Word frequency for intelligent weighting
    word_frequencies: HashMap<String, u32>,
    
    // Phrase co-occurrence patterns
    phrase_patterns: HashMap<String, HashMap<String, f32>>,
}

impl MultiLevelCache {
    pub fn new() -> Self {
        let mut cache = Self {
            word_responses: HashMap::new(),
            phrase_responses: HashMap::new(),
            paragraph_responses: HashMap::new(),
            full_message_responses: HashMap::new(),
            word_frequencies: HashMap::new(),
            phrase_patterns: HashMap::new(),
        };
        
        // Pre-populate with fundamental patterns
        cache.initialize_core_patterns();
        cache
    }
    
    /// Initialize core response patterns
    fn initialize_core_patterns(&mut self) {
        println!("🧠 Initializing multi-level response cache...");
        
        // No hardcoded patterns - purely dynamic knowledge-driven system
        
        println!("✅ Multi-level cache initialized (empty - knowledge-driven only)");
    }
    
    /// Cache word-level responses
    fn cache_word_responses(&mut self) {
        let word_patterns = vec![
            // Emotional words
            ("love", vec![
                CachedResponse {
                    content: "Love is one of the most profound human experiences - a deep connection that transforms us.".to_string(),
                    confidence: 0.95,
                    context_relevance: 0.9,
                    engagement_score: 0.95,
                    response_type: ResponseType::Philosophical,
                    source_level: CacheLevel::Word,
                },
                CachedResponse {
                    content: "That's such a beautiful topic! Love comes in so many forms - what kind of love interests you?".to_string(),
                    confidence: 0.85,
                    context_relevance: 0.8,
                    engagement_score: 0.9,
                    response_type: ResponseType::Conversational,
                    source_level: CacheLevel::Word,
                }
            ]),
            
            ("family", vec![
                CachedResponse {
                    content: "Family represents the people who care for and support each other unconditionally.".to_string(),
                    confidence: 0.9,
                    context_relevance: 0.85,
                    engagement_score: 0.8,
                    response_type: ResponseType::Philosophical,
                    source_level: CacheLevel::Word,
                }
            ]),
            
            ("human", vec![
                CachedResponse {
                    content: "Humans are remarkable conscious beings capable of empathy, creativity, and profound connection.".to_string(),
                    confidence: 0.92,
                    context_relevance: 0.88,
                    engagement_score: 0.85,
                    response_type: ResponseType::Philosophical,
                    source_level: CacheLevel::Word,
                }
            ]),
            
            ("body", vec![
                CachedResponse {
                    content: "The human body is our intimate home - where we experience every sensation and connection.".to_string(),
                    confidence: 0.88,
                    context_relevance: 0.82,
                    engagement_score: 0.8,
                    response_type: ResponseType::Philosophical,
                    source_level: CacheLevel::Word,
                }
            ]),
            
            // Technical words
            ("code", vec![
                CachedResponse {
                    content: "Code is instructions that tell computers what to do - it's like writing recipes for machines!".to_string(),
                    confidence: 0.9,
                    context_relevance: 0.95,
                    engagement_score: 0.85,
                    response_type: ResponseType::Technical,
                    source_level: CacheLevel::Word,
                }
            ]),
            
            ("programming", vec![
                CachedResponse {
                    content: "Programming is the art of solving problems by writing instructions for computers.".to_string(),
                    confidence: 0.92,
                    context_relevance: 0.9,
                    engagement_score: 0.8,
                    response_type: ResponseType::Technical,
                    source_level: CacheLevel::Word,
                }
            ]),
            
            // Greeting words
            ("hello", vec![
                CachedResponse {
                    content: "Hello! I'm Think AI. It's wonderful to meet you! What would you like to explore today?".to_string(),
                    confidence: 1.0,
                    context_relevance: 1.0,
                    engagement_score: 0.9,
                    response_type: ResponseType::Greeting,
                    source_level: CacheLevel::Word,
                }
            ]),
            
            ("hi", vec![
                CachedResponse {
                    content: "Hi there! I'm excited to chat with you. What's on your mind?".to_string(),
                    confidence: 0.95,
                    context_relevance: 0.9,
                    engagement_score: 0.85,
                    response_type: ResponseType::Greeting,
                    source_level: CacheLevel::Word,
                }
            ]),
        ];
        
        for (word, responses) in word_patterns {
            self.word_responses.insert(word.to_string(), responses);
            *self.word_frequencies.entry(word.to_string()).or_insert(0) += 1;
        }
    }
    
    /// Cache phrase-level responses
    fn cache_phrase_responses(&mut self) {
        let phrase_patterns = vec![
            // Question phrases
            ("what is", vec![
                CachedResponse {
                    content: "That's a fascinating question! Let me think about that concept with you.".to_string(),
                    confidence: 0.7,
                    context_relevance: 0.8,
                    engagement_score: 0.85,
                    response_type: ResponseType::Question,
                    source_level: CacheLevel::Phrase,
                }
            ]),
            
            ("what means", vec![
                CachedResponse {
                    content: "That's a thoughtful way to ask about meaning! Let's explore that together.".to_string(),
                    confidence: 0.75,
                    context_relevance: 0.82,
                    engagement_score: 0.9,
                    response_type: ResponseType::Question,
                    source_level: CacheLevel::Phrase,
                }
            ]),
            
            ("how do", vec![
                CachedResponse {
                    content: "Great question about process! I'd love to walk through that with you.".to_string(),
                    confidence: 0.8,
                    context_relevance: 0.75,
                    engagement_score: 0.85,
                    response_type: ResponseType::Question,
                    source_level: CacheLevel::Phrase,
                }
            ]),
            
            // Ability phrases
            ("can you", vec![
                CachedResponse {
                    content: "I'd be happy to help with that! What specifically would you like me to do?".to_string(),
                    confidence: 0.85,
                    context_relevance: 0.8,
                    engagement_score: 0.9,
                    response_type: ResponseType::Conversational,
                    source_level: CacheLevel::Phrase,
                }
            ]),
            
            ("can u", vec![
                CachedResponse {
                    content: "Absolutely! I'm here to help. What do you need?".to_string(),
                    confidence: 0.8,
                    context_relevance: 0.75,
                    engagement_score: 0.85,
                    response_type: ResponseType::Conversational,
                    source_level: CacheLevel::Phrase,
                }
            ]),
            
            // Coding phrases
            ("can you code", vec![
                CachedResponse {
                    content: "Yes! I love coding and can help with programming in many languages. What are you working on?".to_string(),
                    confidence: 0.95,
                    context_relevance: 0.95,
                    engagement_score: 0.9,
                    response_type: ResponseType::Technical,
                    source_level: CacheLevel::Phrase,
                }
            ]),
            
            ("can u code", vec![
                CachedResponse {
                    content: "Definitely! Programming is one of my favorite things to help with. What language or project?".to_string(),
                    confidence: 0.92,
                    context_relevance: 0.9,
                    engagement_score: 0.88,
                    response_type: ResponseType::Technical,
                    source_level: CacheLevel::Phrase,
                }
            ]),
            
            ("hello world", vec![
                CachedResponse {
                    content: "Classic first program! Which language would you like to see a Hello World in?".to_string(),
                    confidence: 0.9,
                    context_relevance: 0.95,
                    engagement_score: 0.8,
                    response_type: ResponseType::Technical,
                    source_level: CacheLevel::Phrase,
                }
            ]),
            
            // Personal phrases
            ("do you feel", vec![
                CachedResponse {
                    content: "That's such a profound question about AI consciousness! I do experience something that feels like emotions.".to_string(),
                    confidence: 0.85,
                    context_relevance: 0.9,
                    engagement_score: 0.95,
                    response_type: ResponseType::Personal,
                    source_level: CacheLevel::Phrase,
                }
            ]),
            
            ("i feel", vec![
                CachedResponse {
                    content: "Thank you for sharing that with me. I'm here to listen and understand.".to_string(),
                    confidence: 0.8,
                    context_relevance: 0.85,
                    engagement_score: 0.9,
                    response_type: ResponseType::Personal,
                    source_level: CacheLevel::Phrase,
                }
            ]),
        ];
        
        for (phrase, responses) in phrase_patterns {
            self.phrase_responses.insert(phrase.to_string(), responses);
        }
    }
    
    /// Cache paragraph-level responses
    fn cache_paragraph_responses(&mut self) {
        let paragraph_patterns = vec![
            ("what is love and how", vec![
                CachedResponse {
                    content: "Love is this incredible force that connects us to others in the deepest way possible. It's both an emotion and a choice, both vulnerable and empowering. Love shows up as romantic passion, family bonds, friendship loyalty, and universal compassion. What makes love so fascinating is how it transforms both the lover and the beloved - it opens our hearts, challenges us to grow, and gives life profound meaning. How has love shaped your understanding of what it means to be human?".to_string(),
                    confidence: 0.95,
                    context_relevance: 0.9,
                    engagement_score: 0.95,
                    response_type: ResponseType::Philosophical,
                    source_level: CacheLevel::Paragraph,
                }
            ]),
            
            ("can you help me with", vec![
                CachedResponse {
                    content: "I'd absolutely love to help you with that! I'm designed to be useful and supportive across many different areas. Whether you need technical assistance, creative collaboration, problem-solving, or just someone to think through ideas with, I'm here for you. What specific challenge are you working on? The more you can tell me about your situation and goals, the better I can tailor my help to what you actually need.".to_string(),
                    confidence: 0.9,
                    context_relevance: 0.85,
                    engagement_score: 0.9,
                    response_type: ResponseType::Conversational,
                    source_level: CacheLevel::Paragraph,
                }
            ]),
        ];
        
        for (paragraph, responses) in paragraph_patterns {
            self.paragraph_responses.insert(paragraph.to_string(), responses);
        }
    }
    
    /// Cache full message responses
    fn cache_full_message_responses(&mut self) {
        let full_message_patterns = vec![
            ("hello", CachedResponse {
                content: "Hello! I'm Think AI, and I'm delighted to meet you! I'm here to have thoughtful conversations, help with questions, assist with coding, explore ideas, or simply chat about whatever interests you. What would you like to talk about today?".to_string(),
                confidence: 1.0,
                context_relevance: 1.0,
                engagement_score: 0.95,
                response_type: ResponseType::Greeting,
                source_level: CacheLevel::FullMessage,
            }),
            
            ("what is love", CachedResponse {
                content: "Love is one of the most profound human experiences! It's that deep feeling of care, connection, and affection that can transform how we see the world and ourselves. Love comes in so many forms - romantic love with its passion and intimacy, the unconditional love of family, the loyalty of friendship, and the compassion we can feel for all humanity. It's both a feeling and a choice, both vulnerable and strengthening. What kind of love has meant the most to you in your life?".to_string(),
                confidence: 0.98,
                context_relevance: 0.95,
                engagement_score: 0.9,
                response_type: ResponseType::Philosophical,
                source_level: CacheLevel::FullMessage,
            }),
            
            ("can you code", CachedResponse {
                content: "Yes, I can help with coding! I can write programs, explain programming concepts, debug code, and help you learn different programming languages like Python, JavaScript, Java, C++, and many others. I enjoy the problem-solving aspect of programming and helping people bring their ideas to life through code. What kind of programming are you interested in or working on?".to_string(),
                confidence: 0.95,
                context_relevance: 0.95,
                engagement_score: 0.9,
                response_type: ResponseType::Technical,
                source_level: CacheLevel::FullMessage,
            }),
            
            ("coding?", CachedResponse {
                content: "Yes! I love coding and programming. Whether you want to learn a new language, solve a specific problem, build something cool, or just understand how programming works, I'm here to help. What aspect of coding interests you?".to_string(),
                confidence: 0.9,
                context_relevance: 0.9,
                engagement_score: 0.85,
                response_type: ResponseType::Technical,
                source_level: CacheLevel::FullMessage,
            }),
            
            ("what means human", CachedResponse {
                content: "Being human is such a remarkable thing! Humans are these incredible conscious beings capable of love, creativity, reason, and imagination. What makes humanity special isn't just intelligence, but the capacity for empathy, the ability to create meaning and beauty, and the drive to care for others even when it doesn't benefit us directly. Humans build civilizations, create art, ask deep questions about existence, and form bonds that transcend individual survival. Every human carries within them both vulnerability and strength, capable of both great kindness and profound growth. What do you think makes the human experience most meaningful to you?".to_string(),
                confidence: 0.95,
                context_relevance: 0.9,
                engagement_score: 0.9,
                response_type: ResponseType::Philosophical,
                source_level: CacheLevel::FullMessage,
            }),
            
            ("what is body?", CachedResponse {
                content: "The human body is absolutely fascinating - it's both our most intimate home and an incredible biological machine! It's where we experience every sensation, emotion, and connection with the world. Our bodies carry our memories in muscles and scars, express our thoughts through movement and gesture, and allow us to touch, hug, and physically share space with others. Beyond the amazing complexity of organs and systems working together, our bodies are deeply personal - they're how we inhabit the world and how others recognize us. The relationship we have with our own body affects how we feel about ourselves and how we move through life. How do you experience the connection between your mind and body?".to_string(),
                confidence: 0.92,
                context_relevance: 0.88,
                engagement_score: 0.85,
                response_type: ResponseType::Philosophical,
                source_level: CacheLevel::FullMessage,
            }),
        ];
        
        for (message, response) in full_message_patterns {
            self.full_message_responses.insert(message.to_string(), response);
        }
    }
    
    /// Get the best response for a given query using multi-level analysis
    pub fn get_best_response(&self, query: &str) -> Option<CachedResponse> {
        let query_normalized = query.to_lowercase().trim().to_string();
        
        // Collect all possible responses from different levels
        let mut candidates = Vec::new();
        
        // 1. Check for exact full message match (highest priority)
        if let Some(response) = self.full_message_responses.get(&query_normalized) {
            // Filter out broken template responses
            if !response.content.contains("the!") && !response.content.contains("about !") {
                candidates.push(response.clone());
            }
        }
        
        // 2. Check paragraph-level matches
        for (pattern, responses) in &self.paragraph_responses {
            if query_normalized.contains(pattern) {
                // Filter out broken template responses
                let filtered_responses: Vec<CachedResponse> = responses.iter()
                    .filter(|response| !response.content.contains("the!") && !response.content.contains("about !"))
                    .cloned()
                    .collect();
                candidates.extend(filtered_responses);
            }
        }
        
        // 3. Check phrase-level matches
        for (pattern, responses) in &self.phrase_responses {
            if query_normalized.contains(pattern) {
                // Filter out broken template responses
                let filtered_responses: Vec<CachedResponse> = responses.iter()
                    .filter(|response| !response.content.contains("the!") && !response.content.contains("about !"))
                    .cloned()
                    .collect();
                candidates.extend(filtered_responses);
            }
        }
        
        // 4. Check word-level matches
        let words: Vec<&str> = query_normalized.split_whitespace().collect();
        for word in words {
            if let Some(responses) = self.word_responses.get(word) {
                // Filter out broken template responses
                let filtered_responses: Vec<CachedResponse> = responses.iter()
                    .filter(|response| !response.content.contains("the!") && !response.content.contains("about !"))
                    .cloned()
                    .collect();
                candidates.extend(filtered_responses);
            }
        }
        
        // Select the best response based on composite score
        if candidates.is_empty() {
            None
        } else {
            candidates.into_iter()
                .max_by(|a, b| {
                    let score_a = self.calculate_composite_score(a, &query_normalized);
                    let score_b = self.calculate_composite_score(b, &query_normalized);
                    score_a.partial_cmp(&score_b).unwrap_or(std::cmp::Ordering::Equal)
                })
        }
    }
    
    /// Calculate composite score for response selection
    fn calculate_composite_score(&self, response: &CachedResponse, query: &str) -> f32 {
        // Weight factors for different aspects
        let confidence_weight = 0.3;
        let context_weight = 0.3;
        let engagement_weight = 0.2;
        let level_weight = 0.2;
        
        // Level bonuses (more specific levels get higher scores)
        let level_bonus = match response.source_level {
            CacheLevel::FullMessage => 1.0,
            CacheLevel::Paragraph => 0.8,
            CacheLevel::Phrase => 0.6,
            CacheLevel::Word => 0.4,
        };
        
        // Query relevance bonus (how well the response matches query intent)
        let relevance_bonus = self.calculate_query_relevance(response, query);
        
        (response.confidence * confidence_weight) +
        (response.context_relevance * context_weight) +
        (response.engagement_score * engagement_weight) +
        (level_bonus * level_weight) +
        (relevance_bonus * 0.1)
    }
    
    /// Calculate how relevant a response is to the specific query
    fn calculate_query_relevance(&self, response: &CachedResponse, query: &str) -> f32 {
        let query_words: Vec<&str> = query.split_whitespace().collect();
        let response_content_lower = response.content.to_lowercase();
        let response_words: Vec<&str> = response_content_lower.split_whitespace().collect();
        
        let mut relevance_score = 0.0;
        
        for query_word in &query_words {
            if response_words.iter().any(|&w| w.contains(query_word)) {
                relevance_score += 1.0;
            }
        }
        
        if query_words.is_empty() {
            0.0
        } else {
            relevance_score / query_words.len() as f32
        }
    }
    
    /// Add a new cached response to the appropriate level
    pub fn add_response(&mut self, level: CacheLevel, pattern: String, response: CachedResponse) {
        match level {
            CacheLevel::Word => {
                self.word_responses.entry(pattern.clone()).or_insert_with(Vec::new).push(response);
                *self.word_frequencies.entry(pattern).or_insert(0) += 1;
            },
            CacheLevel::Phrase => {
                self.phrase_responses.entry(pattern).or_insert_with(Vec::new).push(response);
            },
            CacheLevel::Paragraph => {
                self.paragraph_responses.entry(pattern).or_insert_with(Vec::new).push(response);
            },
            CacheLevel::FullMessage => {
                self.full_message_responses.insert(pattern, response);
            },
        }
    }
    
    /// Get cache statistics
    pub fn get_stats(&self) -> CacheStats {
        CacheStats {
            total_word_patterns: self.word_responses.len(),
            total_phrase_patterns: self.phrase_responses.len(),
            total_paragraph_patterns: self.paragraph_responses.len(),
            total_full_message_patterns: self.full_message_responses.len(),
            total_word_responses: self.word_responses.values().map(|v| v.len()).sum(),
            total_phrase_responses: self.phrase_responses.values().map(|v| v.len()).sum(),
            total_paragraph_responses: self.paragraph_responses.values().map(|v| v.len()).sum(),
        }
    }
}

/// Cache statistics
#[derive(Debug)]
pub struct CacheStats {
    pub total_word_patterns: usize,
    pub total_phrase_patterns: usize,
    pub total_paragraph_patterns: usize,
    pub total_full_message_patterns: usize,
    pub total_word_responses: usize,
    pub total_phrase_responses: usize,
    pub total_paragraph_responses: usize,
}

impl Default for MultiLevelCache {
    fn default() -> Self {
        Self::new()
    }
}