use std::sync::{Arc, atomic::{AtomicBool, Ordering}};
use std::time::Instant;
use think_ai_knowledge::{
    KnowledgeEngine, 
    dynamic_loader::DynamicKnowledgeLoader, 
    response_generator::ComponentResponseGenerator,
    comprehensive_knowledge::ComprehensiveKnowledgeGenerator,
};
use think_ai_qwen::client::QwenClient;
use std::io::Write;
use std::path::PathBuf;

pub struct KnowledgeChat {
    engine: Arc<KnowledgeEngine>,
    qwen_client: Arc<QwenClient>,
    response_generator: Arc<ComponentResponseGenerator>,
    conversation_history: Vec<(String, String)>, // (query, response) pairs
}

impl KnowledgeChat {
    pub fn new() -> Self {
        let engine = Arc::new(KnowledgeEngine::new());
        
        // First try to load from dynamic files
        let knowledge_dir = PathBuf::from("./knowledge_files");
        let dynamic_loader = DynamicKnowledgeLoader::new(&knowledge_dir);
        
        println!("📂 Loading knowledge from files...");
        match dynamic_loader.load_all(&engine) {
            Ok(count) => println!("✅ Loaded {} items from knowledge files", count),
            Err(e) => println!("⚠️  Could not load knowledge files: {}", e),
        }
        
        // Then load comprehensive knowledge (full set)
        println!("🧠 Loading comprehensive knowledge base...");
        ComprehensiveKnowledgeGenerator::populate_deep_knowledge(&engine);
        
        // Load from persistence if available
        let mut loaded = false;
        if let Ok(persistence) = think_ai_knowledge::persistence::KnowledgePersistence::new("./trained_knowledge") {
            if let Ok(Some(checkpoint)) = persistence.load_latest_checkpoint() {
                println!("🎓 Loading {} items from trained knowledge...", checkpoint.nodes.len());
                engine.load_nodes(checkpoint.nodes);
                loaded = true;
            }
        }
        
        if !loaded {
            if let Ok(persistence) = think_ai_knowledge::persistence::KnowledgePersistence::new("./knowledge_storage") {
                if let Ok(Some(checkpoint)) = persistence.load_latest_checkpoint() {
                    println!("📚 Loading {} items from checkpoint...", checkpoint.nodes.len());
                    engine.load_nodes(checkpoint.nodes);
                }
            }
        }
        
        let stats = engine.get_stats();
        println!("✅ Knowledge base ready with {} items across {} domains\n", 
            stats.total_nodes, 
            stats.domain_distribution.len()
        );
        
        let response_generator = Arc::new(ComponentResponseGenerator::new(engine.clone()));
        
        Self { 
            engine,
            qwen_client: Arc::new(QwenClient::new_with_defaults()),
            response_generator,
            conversation_history: Vec::new(),
        }
    }
    
    pub async fn process_query(&mut self, query: &str) -> (String, f64) {
        let start = Instant::now();
        
        // Handle special commands
        if query.trim().to_lowercase() == "help" {
            return (self.get_help_text(), start.elapsed().as_secs_f64() * 1000.0);
        }
        
        if query.trim().to_lowercase() == "stats" {
            return (self.get_stats_text(), start.elapsed().as_secs_f64() * 1000.0);
        }
        
        // Process knowledge query with context
        let contextualized_query = self.add_context_if_needed(query);
        let response = self.generate_response(&contextualized_query).await;
        let elapsed = start.elapsed().as_secs_f64() * 1000.0;
        
        // Store in conversation history
        self.conversation_history.push((query.to_string(), response.clone()));
        // Keep only last 10 exchanges
        if self.conversation_history.len() > 10 {
            self.conversation_history.remove(0);
        }
        
        (response, elapsed)
    }
    
    fn add_context_if_needed(&self, query: &str) -> String {
        let query_lower = query.to_lowercase();
        
        // Check if query contains context-dependent words
        let context_words = ["it", "its", "that", "this", "they", "their", "them", "those", "these"];
        let needs_context = context_words.iter().any(|word| {
            query_lower.split_whitespace().any(|w| w == *word)
        });
        
        if needs_context && !self.conversation_history.is_empty() {
            // Get the last topic discussed
            if let Some((prev_query, prev_response)) = self.conversation_history.last() {
                // Extract the main topic from previous response
                if let Some(topic) = self.extract_topic_from_response(prev_response) {
                    // Rewrite query with context
                    let contextualized = query.replace("it", &topic)
                        .replace("its", &format!("{}'s", topic))
                        .replace("that", &topic)
                        .replace("this", &topic);
                    
                    if contextualized != query {
                        return contextualized;
                    }
                }
            }
        }
        
        query.to_string()
    }
    
    fn extract_topic_from_response(&self, response: &str) -> Option<String> {
        // Simple heuristic: look for "The X is" or "X is" pattern
        if let Some(start) = response.find("The ") {
            if let Some(is_pos) = response[start..].find(" is") {
                let topic = &response[start+4..start+is_pos];
                if topic.len() < 50 { // Reasonable topic length
                    return Some(topic.to_string());
                }
            }
        }
        
        // Try without "The"
        if response.starts_with(|c: char| c.is_uppercase()) {
            if let Some(is_pos) = response.find(" is") {
                let topic = &response[..is_pos];
                if topic.len() < 50 && !topic.contains(' ') {
                    return Some(topic.to_string());
                }
            }
        }
        
        None
    }
    
    async fn generate_response(&self, query: &str) -> String {
        let query_lower = query.to_lowercase();
        
        // O(1) fast path for system commands
        match query_lower.as_str() {
            "help" => return self.get_help_text(),
            "stats" => return self.get_stats_text(),
            _ => {}
        }
        
        // Handle common abbreviations
        let expanded_query = match query_lower.as_str() {
            "js" | "what is js" => "javascript",
            "ts" | "what is ts" => "typescript", 
            "py" | "what is py" => "python",
            "cs" | "what is cs" => "computer science",
            "ml" | "what is ml" => "machine learning",
            "ai" | "what is ai" => "artificial intelligence",
            "ds" | "what is ds" => "data structures",
            _ => query
        };
        
        // Use component-based response generator first
        let component_response = self.response_generator.generate_response(expanded_query);
        
        // If component generator produced a good response, use it
        if !component_response.contains("I need more context") && component_response.len() > 50 {
            return component_response;
        }
        
        // Otherwise, try direct knowledge lookup
        if let Some(results) = self.engine.query(expanded_query) {
            if !results.is_empty() {
                return results[0].content.clone();
            }
        }
        
        // Try case-insensitive search
        let expanded_lower = expanded_query.to_lowercase();
        if let Some(results) = self.engine.query(&expanded_lower) {
            if !results.is_empty() {
                return results[0].content.clone();
            }
        }
        
        // CACHE MISS - Use enhanced TinyLlama with context
        print!("🔄 Generating");
        std::io::Write::flush(&mut std::io::stdout()).unwrap();
        
        // Show progress dots
        let stop_progress = Arc::new(AtomicBool::new(false));
        let stop_flag = stop_progress.clone();
        
        let progress_handle = std::thread::spawn(move || {
            while !stop_flag.load(Ordering::Relaxed) {
                std::thread::sleep(std::time::Duration::from_millis(500));
                if !stop_flag.load(Ordering::Relaxed) {
                    print!(".");
                    std::io::Write::flush(&mut std::io::stdout()).unwrap();
                }
            }
        });
        
        // Get knowledge context
        let knowledge_nodes = self.engine.get_top_relevant(expanded_query, 5);
        let context = if !knowledge_nodes.is_empty() {
            knowledge_nodes.iter()
                .take(3)
                .map(|node| format!("{}: {}", node.topic, &node.content[..100.min(node.content.len())]))
                .collect::<Vec<_>>()
                .join(" ")
        } else {
            String::new()
        };
        
        let result = match tokio::time::timeout(
            tokio::time::Duration::from_secs(5),
            async {
                if context.is_empty() {
                    self.tinyllama_client.generate(expanded_query).await
                } else {
                    self.tinyllama_client.generate_with_context(expanded_query, &context).await
                }
            }
        ).await {
            Ok(Ok(response)) => response,
            Ok(Err(e)) => {
                eprintln!("\n⚠️  Generation error: {}", e);
                component_response // Fall back to component response
            }
            Err(_) => {
                eprintln!("\n⚠️  Generation timeout");
                component_response // Fall back to component response
            }
        };
        
        // Stop progress indicator
        stop_progress.store(true, Ordering::Relaxed);
        let _ = progress_handle.join();
        println!(); // New line after dots
        
        result
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