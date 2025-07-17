// Fast Response Component - Ensures <500ms response times

use crate::response_generator::{ResponseComponent, ResponseContext};
use std::collections::HashMap;
use std::time::Duration;

pub struct FastResponseComponent {
    quick_responses: HashMap<String, String>,
}

impl Default for FastResponseComponent {
    fn default() -> Self {
        Self::new()
    }
}

impl FastResponseComponent {
    pub fn new() -> Self {
        let mut quick_responses = HashMap::new();

        // Pre-computed responses for common queries
        quick_responses.insert(
            "hello".to_string(),
            "Hello! How can I help you today?".to_string(),
        );
        quick_responses.insert(
            "hi".to_string(),
            "Hi there! What can I do for you?".to_string(),
        );
        quick_responses.insert(
            "how are you".to_string(),
            "I'm functioning perfectly with O(1) response times! How are you?".to_string(),
        );
        quick_responses.insert(
            "what is your name".to_string(),
            "I'm Think AI, your intelligent assistant with instant responses.".to_string(),
        );
        quick_responses.insert("help".to_string(), "I'm here to help! You can ask me questions, have conversations, or request information on any topic.".to_string());
        quick_responses.insert(
            "thanks".to_string(),
            "You're welcome! Happy to help.".to_string(),
        );
        quick_responses.insert(
            "thank you".to_string(),
            "You're very welcome! Is there anything else I can help with?".to_string(),
        );
        quick_responses.insert("bye".to_string(), "Goodbye! Have a great day!".to_string());
        quick_responses.insert(
            "goodbye".to_string(),
            "Farewell! Feel free to come back anytime.".to_string(),
        );

        Self { quick_responses }
    }
}

impl ResponseComponent for FastResponseComponent {
    fn name(&self) -> &'static str {
        "FastResponse"
    }

    fn can_handle(&self, query: &str, _context: &ResponseContext) -> f32 {
        let query_lower = query.to_lowercase().trim().to_string();

        // Exact match gets highest priority
        if self.quick_responses.contains_key(&query_lower) {
            return 0.99; // Very high priority for instant responses
        }

        // Check for partial matches
        for key in self.quick_responses.keys() {
            if query_lower.contains(key) || key.contains(&query_lower) {
                return 0.85;
            }
        }

        0.0
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        let query_lower = query.to_lowercase().trim().to_string();

        // Direct lookup - O(1)
        if let Some(response) = self.quick_responses.get(&query_lower) {
            return Some(response.clone());
        }

        // Partial match fallback
        for (key, response) in &self.quick_responses {
            if query_lower.contains(key) || key.contains(&query_lower) {
                return Some(response.clone());
            }
        }

        None
    }
}

// Wrapper for slow components with timeout
pub struct TimeoutWrapper<T: ResponseComponent> {
    inner: T,
    timeout_duration: Duration,
}

impl<T: ResponseComponent> TimeoutWrapper<T> {
    pub fn new(inner: T, timeout_ms: u64) -> Self {
        Self {
            inner,
            timeout_duration: Duration::from_millis(timeout_ms),
        }
    }
}

impl<T: ResponseComponent + Send + Sync + 'static> ResponseComponent for TimeoutWrapper<T> {
    fn name(&self) -> &'static str {
        self.inner.name()
    }

    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        self.inner.can_handle(query, context)
    }

    fn generate(&self, query: &str, context: &ResponseContext) -> Option<String> {
        // For synchronous components, we can't easily add timeout
        // This would need async support in the trait
        // For now, just pass through
        self.inner.generate(query, context)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Arc;
    use std::time::Instant;

    #[test]
    fn test_fast_response_exact_match() {
        let component = FastResponseComponent::new();
        let context = ResponseContext {
            knowledge_engine: Arc::new(crate::KnowledgeEngine::new()),
            relevant_nodes: vec![],
            query_tokens: vec![],
            conversation_history: vec![],
            extracted_entities: HashMap::new(),
        };

        assert_eq!(component.can_handle("hello", &context), 0.99);
        assert_eq!(
            component.generate("hello", &context),
            Some("Hello! How can I help you today?".to_string())
        );
    }

    #[test]
    fn test_fast_response_performance() {
        let component = FastResponseComponent::new();
        let context = ResponseContext {
            knowledge_engine: Arc::new(crate::KnowledgeEngine::new()),
            relevant_nodes: vec![],
            query_tokens: vec![],
            conversation_history: vec![],
            extracted_entities: HashMap::new(),
        };

        let queries = ["hello", "hi", "thanks", "bye", "how are you"];
        let start = Instant::now();

        for _ in 0..1000 {
            for query in &queries {
                component.generate(query, &context);
            }
        }

        let duration = start.elapsed();
        let avg_time = duration.as_micros() as f64 / 5000.0;

        // Should be < 100 microseconds per query (0.1ms)
        assert!(
            avg_time < 100.0,
            "Average response time {} μs exceeds target",
            avg_time
        );
    }
}
