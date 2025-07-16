// Simple Cache Component - Minimal test version
//!
// This is a minimal version to test component registration and basic functionality

use crate::response_generator::{ResponseComponent, ResponseContext};
use std::collections::HashMap;

/// Minimal cache component for testing
pub struct SimpleCacheComponent {
    test_responses: HashMap<String, String>,
}

impl SimpleCacheComponent {
    pub fn new() -> Self {
        println!("🚀 SimpleCacheComponent: INITIALIZING");
        let mut test_responses = HashMap::new();

        test_responses.insert(
            "hello".to_string(),
            "Hello from SimpleCacheComponent! This proves the cache is working.".to_string(),
        );

        test_responses.insert(
            "test".to_string(),
            "Test response from SimpleCacheComponent.".to_string(),
        );

        println!(
            "📦 SimpleCacheComponent: Added {} test responses",
            test_responses.len()
        );

        Self { test_responses }
    }
}

impl ResponseComponent for SimpleCacheComponent {
    fn name(&self) -> &'static str {
        "SimpleCache"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_normalized = query.to_lowercase().trim().to_string();
        println!("🔍 SimpleCache: Checking if I can handle '{query}'");

        if self.test_responses.contains_key(&query_normalized) {
            println!("🎯 SimpleCache: EXACT MATCH found for '{query}'");
            1.0 // Maximum score for exact matches
        } else {
            println!("🔍 SimpleCache: No exact match for '{query}'");
            0.95 // Still high score to test if component gets called
        }
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        println!("🧠 SimpleCache: GENERATE called for '{query}'");
        let query_normalized = query.to_lowercase().trim().to_string();

        if let Some(cached_response) = self.test_responses.get(&query_normalized) {
            println!("✅ SimpleCache: Returning cached response");
            Some(cached_response.clone())
        } else {
            println!("🤖 SimpleCache: Generating dynamic response");
            Some(format!(
                "SimpleCache dynamic response for: '{query}'. This proves the component is working!"
            ))
        }
    }

    fn metadata(&self) -> HashMap<String, String> {
        let mut metadata = HashMap::new();
        metadata.insert("type".to_string(), "simple_cache_test".to_string());
        metadata.insert(
            "cached_responses".to_string(),
            self.test_responses.len().to_string(),
        );
        metadata
    }
}

impl Default for SimpleCacheComponent {
    fn default() -> Self {
        Self::new()
    }
}
