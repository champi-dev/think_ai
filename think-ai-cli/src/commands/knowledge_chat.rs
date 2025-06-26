use std::sync::{Arc, atomic::{AtomicBool, Ordering}};
use std::time::Instant;
use think_ai_knowledge::{KnowledgeEngine, real_knowledge::RealKnowledgeGenerator};
use think_ai_qwen::{QwenClient, KnowledgeContext};
use std::io::Write;

pub struct KnowledgeChat {
    engine: Arc<KnowledgeEngine>,
    qwen_client: Arc<QwenClient>,
    conversation_history: Vec<(String, String)>, // (query, response) pairs
}

impl KnowledgeChat {
    pub fn new() -> Self {
        let engine = Arc::new(KnowledgeEngine::new());
        
        // Load real knowledge
        println!("🧠 Loading knowledge base...");
        RealKnowledgeGenerator::populate_comprehensive_knowledge(&engine);
        
        // Load from persistence if available
        // First try trained knowledge, then fallback to regular storage
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
        
        Self { 
            engine,
            qwen_client: Arc::new(QwenClient::new()),
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
                        eprintln!("📝 Context added: {} → {}", query, contextualized);
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
        
        // O(1) fast path for system commands and greetings
        match query_lower.as_str() {
            "help" => return self.get_help_text(),
            "stats" => return self.get_stats_text(),
            "hi" | "hello" | "hey" => {
                return "Hello! I'm Think AI with a knowledge base of science, programming, and more. What would you like to know?".to_string();
            }
            _ => {}
        }
        
        // First, always try the knowledge base (this is O(1) with hash lookup)
        if let Some(results) = self.engine.query(query) {
            if !results.is_empty() {
                let node = &results[0];
                return node.content.clone();
            }
        }
        
        // Try case-insensitive search
        if let Some(results) = self.engine.query(&query_lower) {
            if !results.is_empty() {
                let node = &results[0];
                return node.content.clone();
            }
        }
        
        // Try intelligent query for partial matches
        let results = self.engine.intelligent_query(query);
        if !results.is_empty() {
            let node = &results[0];
            return node.content.clone();
        }
        
        // CACHE MISS - Use Qwen for intelligent response with knowledge context
        print!("🔄 Thinking");
        std::io::Write::flush(&mut std::io::stdout()).unwrap();
        
        // Show progress dots with a stop flag
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
        
        // Get top relevant knowledge pieces even if not exact matches
        let knowledge_nodes = self.engine.get_top_relevant(query, 5);
        
        // Convert to KnowledgeContext for Qwen
        let knowledge_contexts: Vec<KnowledgeContext> = knowledge_nodes
            .iter()
            .map(|node| KnowledgeContext {
                domain: format!("{:?}", node.domain),
                title: node.topic.clone(),
                content: node.content.clone(),
            })
            .collect();
        
        // Now we can properly await the async call
        
        let result = match tokio::time::timeout(
            tokio::time::Duration::from_secs(5),
            self.qwen_client.generate_response_with_context(query, &knowledge_contexts)
        ).await {
            Ok(Ok(response)) => {
                response
            },
            Ok(Err(e)) => {
                eprintln!("\n⚠️  API Error: {}. Using offline response.", e);
                self.generate_fallback_response(query)
            }
            Err(_) => {
                eprintln!("\n⚠️  Request timed out. Using offline response.");
                self.generate_fallback_response(query)
            }
        };
        
        // Stop progress indicator
        stop_progress.store(true, Ordering::Relaxed);
        let _ = progress_handle.join();
        println!(); // New line after dots
        
        result
    }
    
    // Removed hardcoded direct answers - everything comes from knowledge base
    
    // Removed has_exact_match - not needed for O(1) performance
    
    // Removed complex synthesis - not needed for O(1) performance
    
    fn generate_fallback_response(&self, query: &str) -> String {
        let query_lower = query.to_lowercase();
        
        // Handle greetings
        if query_lower == "hi" || query_lower == "hello" || query_lower == "hey" {
            return "Hello! I'm Think AI with a knowledge base of science, programming, and more. What would you like to know?".to_string();
        }
        
        // Handle personal introductions
        if query_lower.starts_with("i'm ") || query_lower.starts_with("i am ") {
            let words: Vec<&str> = query.split_whitespace().collect();
            let name = if words.len() > 1 { words[1] } else { "there" };
            return format!("Nice to meet you, {}! I'm Think AI. How can I help you today?", name);
        }
        
        // Try to extract the core concept and suggest related topics
        let stats = self.engine.get_stats();
        format!(
            "I don't have specific information about '{}' in my {} knowledge items. \n\n\
            I can help with topics like:\n\
            • Programming (JavaScript, Python, Rust)\n\
            • Science (physics, biology, chemistry)\n\
            • Mathematics and algorithms\n\
            • Philosophy and consciousness\n\
            • History and art\n\n\
            Try asking about one of these areas!",
            query, stats.total_nodes
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