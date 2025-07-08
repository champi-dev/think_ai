//! Minimal Response Generator - Pure AI responses without pre-loaded knowledge

use crate::qwen_cache::QwenCache;
use think_ai_qwen::client::{QwenClient, QwenRequest};
use std::sync::Arc;
use tokio::runtime::Runtime;

pub struct MinimalResponseGenerator {
    qwen_client: Arc<QwenClient>,
    cache: Arc<QwenCache>,
    runtime: Runtime,
}

impl MinimalResponseGenerator {
    pub fn new() -> Self {
        Self {
            qwen_client: Arc::new(QwenClient::new_with_defaults()),
            cache: Arc::new(QwenCache::new()),
            runtime: Runtime::new().expect("Failed to create runtime"),
        }
    }
    
    pub fn generate(&self, query: &str) -> String {
        // Check cache first for O(1) performance
        if let Some(cached_response) = self.cache.get(query) {
            return cached_response;
        }
        
        // Generate new response
        let request = QwenRequest {
            query: query.to_string(),
            context: None,
            system_prompt: Some("You are Think AI, a helpful AI assistant. Respond naturally and conversationally to the user's query.".to_string()),
        };
        
        let response = self.runtime.block_on(async {
            match self.qwen_client.generate(request).await {
                Ok(response) => response.content,
                Err(_) => {
                    // For now, return a simple contextual response
                    match query.to_lowercase().as_str() {
                        q if q.contains("hello") => "Hello! I'm Think AI. How can I help you today?".to_string(),
                        q if q.contains("what is") => {
                            let cleaned = q.replace("what is", "").trim().to_string();
                            format!("{} is something I'm learning about. Can you tell me more about what specific aspect interests you?", cleaned)
                        },
                        _ => format!("I'm processing your question about '{}'. Let me think about that.", query),
                    }
                }
            }
        });
        
        // Cache the response for future use
        self.cache.store(query, &response);
        
        response
    }
    
    pub fn get_stats(&self) -> String {
        let (total_cached, total_uses) = self.cache.get_stats();
        format!("📊 Cache stats: {} unique queries cached, {} total uses", total_cached, total_uses)
    }
}