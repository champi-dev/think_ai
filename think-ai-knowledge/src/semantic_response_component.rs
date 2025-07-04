//! Semantic Response Component - O(1) contextual responses using semantic hashing
//! 
//! This component replaces the MultiLevelResponseComponent with a more intelligent
//! system that understands query semantics while maintaining O(1) performance.

use crate::response_generator::{ResponseComponent, ResponseContext};
use crate::semantic_hash_cache::{SemanticHashCache, SemanticCategory, QueryIntent};
use crate::multilevel_cache::{CachedResponse, ResponseType, CacheLevel};
use std::sync::{Arc, RwLock};
use std::collections::HashMap;

/// Semantic response component with O(1) contextual understanding
pub struct SemanticResponseComponent {
    cache: Arc<RwLock<SemanticHashCache>>,
    fallback_to_knowledge: bool,
}

impl SemanticResponseComponent {
    pub fn new() -> Self {
        println!("🚀 Initializing SemanticResponseComponent with contextual O(1) responses");
        Self {
            cache: Arc::new(RwLock::new(SemanticHashCache::new())),
            fallback_to_knowledge: true,
        }
    }
    
    /// Check if we should use knowledge base instead
    fn should_use_knowledge(&self, context: &ResponseContext) -> bool {
        // If we have high-quality knowledge nodes, prefer them over generic responses
        context.relevant_nodes.iter().any(|node| node.confidence > 0.8)
    }
    
    /// Generate a response that acknowledges lack of specific knowledge
    fn generate_fallback_response(&self, query: &str) -> Option<String> {
        let query_lower = query.to_lowercase();
        
        if query_lower.contains("thank") && query_lower.contains("goodbye") {
            Some("You're welcome! It was great chatting with you. Have a wonderful day!".to_string())
        } else if query_lower.starts_with("thank") {
            Some("You're welcome! Is there anything else you'd like to explore?".to_string())
        } else {
            // For unknown queries, be honest about limitations
            Some("I need to access my knowledge base to give you a comprehensive answer about that. While I maintain O(1) response times, my cached knowledge doesn't include specific information on this topic.".to_string())
        }
    }
}

impl ResponseComponent for SemanticResponseComponent {
    fn name(&self) -> &'static str {
        "SemanticCache"
    }
    
    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        // Lower priority if knowledge base has relevant information
        if self.should_use_knowledge(context) && self.fallback_to_knowledge {
            return 0.5; // Let knowledge base take precedence
        }
        
        // Check if we have a semantic match
        if let Ok(cache) = self.cache.read() {
            if let Some(_) = cache.get_semantic_response(query) {
                0.9 // High score for semantic matches
            } else {
                0.3 // Low score to allow other components
            }
        } else {
            0.1
        }
    }
    
    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // First check if knowledge base should handle this
        if self.should_use_knowledge(context) && self.fallback_to_knowledge {
            return None; // Let knowledge base handle it
        }
        
        // Try semantic lookup
        if let Ok(cache) = self.cache.read() {
            if let Some(response) = cache.get_semantic_response(query) {
                return Some(response.content);
            }
        }
        
        // Generate appropriate fallback
        self.generate_fallback_response(query)
    }
    
    fn metadata(&self) -> HashMap<String, String> {
        let mut metadata = HashMap::new();
        metadata.insert("type".to_string(), "semantic_cache".to_string());
        metadata.insert("fallback_to_knowledge".to_string(), self.fallback_to_knowledge.to_string());
        metadata
    }
}

impl Default for SemanticResponseComponent {
    fn default() -> Self {
        Self::new()
    }
}