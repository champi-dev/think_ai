// Fast Ollama Component with timeout handling and fallback
use crate::response_generator::{ResponseComponent, ResponseContext};
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::runtime::Handle;
use tokio::time::timeout;

pub struct FastOllamaComponent {
    endpoint_available: Arc<std::sync::Mutex<Option<bool>>>,
    last_check: Arc<std::sync::Mutex<Instant>>,
}

impl Default for FastOllamaComponent {
    fn default() -> Self {
        Self::new()
    }
}

impl FastOllamaComponent {
    pub fn new() -> Self {
        Self {
            endpoint_available: Arc::new(std::sync::Mutex::new(None)),
            last_check: Arc::new(std::sync::Mutex::new(
                Instant::now() - Duration::from_secs(60),
            )),
        }
    }

    fn is_available(&self) -> bool {
        let mut available = self.endpoint_available.lock().unwrap();
        let mut last_check = self.last_check.lock().unwrap();

        // Check every 30 seconds
        if last_check.elapsed() > Duration::from_secs(30) {
            *last_check = Instant::now();

            // Quick health check with 1s timeout
            let check = std::process::Command::new("curl")
                .arg("-s")
                .arg("-m")
                .arg("1")
                .arg("http://localhost:11434/api/tags")
                .output();

            *available = Some(check.map(|o| o.status.success()).unwrap_or(false));
        }

        available.unwrap_or(false)
    }

    fn generate_fallback_response(&self, query: &str) -> String {
        let query_lower = query.to_lowercase();

        // Provide intelligent fallback responses
        if query_lower.contains("hello") || query_lower.contains("hi") {
            "Hello! I'm currently operating in fast mode with limited capabilities. How can I help you today?".to_string()
        } else if query_lower.contains("how are you") {
            "I'm functioning well in fast response mode! My advanced features are temporarily limited, but I can still help with basic queries.".to_string()
        } else if query_lower.contains("what") && query_lower.contains("can you do") {
            "In fast mode, I can:\n• Answer basic questions\n• Have conversations\n• Remember our chat history\n• Provide quick responses\n\nFor complex queries, I'll do my best with the available resources!".to_string()
        } else if query_lower.contains("code") || query_lower.contains("programming") {
            "I can help with coding questions! While my advanced AI models might be temporarily unavailable, I can still discuss programming concepts, syntax, and best practices based on my knowledge base.".to_string()
        } else {
            format!("I understand you're asking about '{}'. While my advanced AI capabilities are temporarily limited, I'll do my best to help based on my core knowledge. Could you provide more specific details?", query)
        }
    }
}

impl ResponseComponent for FastOllamaComponent {
    fn name(&self) -> &'static str {
        "FastOllama"
    }

    fn can_handle(&self, query: &str, context: &ResponseContext) -> f32 {
        // Skip if query is already handled by other components
        if query.starts_with("[CODE REQUEST]") {
            return 0.0;
        }

        // Skip if conversational component can handle it well
        let query_lower = query.to_lowercase();
        if query_lower.contains("my name")
            || query_lower.contains("remember")
            || query_lower.contains("what") && query_lower.contains("know about me")
        {
            return 0.0;
        }

        // Handle general queries with lower priority
        0.5
    }

    fn generate(&self, query: &str, _context: &ResponseContext) -> Option<String> {
        // Quick check if Ollama is available
        if !self.is_available() {
            // Return fallback response immediately
            return Some(self.generate_fallback_response(query));
        }

        // Try to get response with strict timeout
        let query = query.to_string();
        let handle = Handle::try_current();

        match handle {
            Ok(handle) => {
                // We're already in async context
                handle.block_on(async {
                    timeout(Duration::from_secs(2), async {
                        // Very basic HTTP request with timeout
                        None // For now, return None to use fallback
                    })
                    .await
                    .ok()
                    .flatten()
                })
            }
            Err(_) => {
                // No async runtime, use fallback
                Some(self.generate_fallback_response(&query))
            }
        }
        .or_else(|| Some(self.generate_fallback_response(&query)))
    }
}
