use std::sync::Arc;
use std::time::Instant;
use think_ai_knowledge::{KnowledgeEngine, real_knowledge::RealKnowledgeGenerator};

pub struct KnowledgeChat {
    engine: Arc<KnowledgeEngine>,
}

impl KnowledgeChat {
    pub fn new() -> Self {
        let engine = Arc::new(KnowledgeEngine::new());
        
        // Load real knowledge
        println!("🧠 Loading knowledge base...");
        RealKnowledgeGenerator::populate_comprehensive_knowledge(&engine);
        
        // Load from persistence if available
        if let Ok(persistence) = think_ai_knowledge::persistence::KnowledgePersistence::new("./knowledge_storage") {
            if let Ok(Some(checkpoint)) = persistence.load_latest_checkpoint() {
                println!("📚 Loading {} items from checkpoint...", checkpoint.nodes.len());
                engine.load_nodes(checkpoint.nodes);
            }
        }
        
        let stats = engine.get_stats();
        println!("✅ Knowledge base ready with {} items across {} domains\n", 
            stats.total_nodes, 
            stats.domain_distribution.len()
        );
        
        Self { engine }
    }
    
    pub fn process_query(&self, query: &str) -> (String, f64) {
        let start = Instant::now();
        
        // Handle special commands
        if query.trim().to_lowercase() == "help" {
            return (self.get_help_text(), start.elapsed().as_secs_f64() * 1000.0);
        }
        
        if query.trim().to_lowercase() == "stats" {
            return (self.get_stats_text(), start.elapsed().as_secs_f64() * 1000.0);
        }
        
        // Process knowledge query
        let response = self.generate_response(query);
        let elapsed = start.elapsed().as_secs_f64() * 1000.0;
        
        (response, elapsed)
    }
    
    fn generate_response(&self, query: &str) -> String {
        // Try intelligent query first
        let results = self.engine.intelligent_query(query);
        
        if results.is_empty() {
            // If no results, provide a thoughtful response
            return self.generate_fallback_response(query);
        }
        
        // Generate comprehensive response from knowledge
        let mut response = String::new();
        
        if results.len() == 1 {
            let node = &results[0];
            response.push_str(&node.content);
            
            if !node.related_concepts.is_empty() {
                response.push_str(&format!("\n\n📌 Related concepts: {}", node.related_concepts.join(", ")));
            }
        } else {
            // Multiple relevant results - synthesize
            response.push_str(&format!("I found {} relevant pieces of knowledge:\n\n", results.len()));
            
            for (i, node) in results.iter().take(3).enumerate() {
                response.push_str(&format!("{}. **{}**\n", i + 1, node.topic));
                
                // Truncate content if too long
                if node.content.len() > 200 {
                    response.push_str(&format!("{}...\n\n", &node.content[..200]));
                } else {
                    response.push_str(&format!("{}\n\n", node.content));
                }
            }
            
            if results.len() > 3 {
                response.push_str(&format!("... and {} more related topics.", results.len() - 3));
            }
        }
        
        response
    }
    
    fn generate_fallback_response(&self, query: &str) -> String {
        let query_lower = query.to_lowercase();
        
        // Check for greeting
        if query_lower.contains("hello") || query_lower.contains("hi") || query_lower.contains("hey") {
            return "Hello! I'm Think AI with a comprehensive knowledge base. I can discuss topics in programming, mathematics, physics, philosophy, history, biology, and more. What would you like to know about?".to_string();
        }
        
        // Check for capability questions
        if query_lower.contains("can you") || query_lower.contains("what can") {
            return format!("I have knowledge about programming languages (JavaScript, Python, Rust), computer science concepts, mathematics, physics, philosophy, history, biology, and art. I can explain concepts, provide detailed information, and help you understand complex topics. Try asking me about any of these areas!");
        }
        
        // Generic thoughtful response
        format!(
            "I don't have specific information about '{}' in my knowledge base yet. However, I can discuss:\n\
            • Programming and computer science\n\
            • Mathematics and algorithms\n\
            • Physics and quantum mechanics\n\
            • Philosophy and consciousness\n\
            • Biology and evolution\n\
            • History and art\n\
            \nTry asking about any of these topics!",
            query
        )
    }
    
    fn get_help_text(&self) -> String {
        "🧠 Think AI Knowledge System Commands:\n\n\
        • Type any question to query the knowledge base\n\
        • 'help' - Show this help message\n\
        • 'stats' - Show knowledge base statistics\n\
        • 'exit' or 'quit' - Exit the chat\n\
        \n\
        Example queries:\n\
        • What is JavaScript?\n\
        • Explain quantum mechanics\n\
        • Tell me about consciousness\n\
        • How do hash tables work?\n\
        • What is the Industrial Revolution?".to_string()
    }
    
    fn get_stats_text(&self) -> String {
        let stats = self.engine.get_stats();
        let mut domain_info = String::new();
        
        let domain_count = stats.domain_distribution.len();
        for (domain, count) in &stats.domain_distribution {
            domain_info.push_str(&format!("  • {:?}: {} items\n", domain, count));
        }
        
        format!(
            "📊 Knowledge Base Statistics:\n\n\
            Total Knowledge Items: {}\n\
            Domains Covered: {}\n\
            Average Confidence: {:.2}\n\
            \n\
            Domain Distribution:\n{}",
            stats.total_nodes,
            domain_count,
            stats.average_confidence,
            domain_info
        )
    }
}