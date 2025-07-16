// Debug wrapper for ComponentResponseGenerator to log component selection
use crate::response_generator::{ComponentResponseGenerator, ResponseContext};
use crate::KnowledgeEngine;
use crate::enhanced_conversation_memory::EnhancedConversationMemory;
use std::sync::Arc;

pub struct DebugResponseGenerator {
    inner: ComponentResponseGenerator,
}

impl DebugResponseGenerator {
    pub fn new_with_memory(
        knowledge_engine: Arc<KnowledgeEngine>,
        memory: Arc<EnhancedConversationMemory>,
    ) -> Self {
        Self {
            inner: ComponentResponseGenerator::new_with_memory(knowledge_engine, memory),
        }
    }
    
    pub fn generate_response_with_model(&self, query: &str, model: Option<&str>) -> String {
        println!("\n=== DEBUG: Response Generation ===");
        println!("Query: {}", query);
        println!("Model hint: {:?}", model);
        
        // Check if query contains conversation context
        if query.contains("User:") || query.contains("Assistant:") {
            println!("Query contains conversation context");
            let lines: Vec<&str> = query.lines().collect();
            println!("Context lines: {}", lines.len());
            for (i, line) in lines.iter().enumerate() {
                if line.starts_with("User:") || line.starts_with("Assistant:") {
                    println!("  Line {}: {}", i, line);
                }
            }
        }
        
        let response = self.inner.generate_response_with_model(query, model);
        println!("Generated response: {}", response);
        println!("=================================\n");
        
        response
    }
}