use std::sync::{Arc, atomic::{AtomicBool, Ordering}};
use std::time::Instant;
use think_ai_knowledge::{
    KnowledgeEngine, 
    real_knowledge::RealKnowledgeGenerator, 
    dynamic_loader::DynamicKnowledgeLoader, 
    response_generator::ComponentResponseGenerator,
    intelligent_response_selector::{IntelligentResponseSelector, ResponseSource},
    tinyllama_knowledge_builder::TinyLlamaKnowledgeBuilder,
    self_evaluator::SelfEvaluator,
    conversation_memory::ConversationMemory
};
use think_ai_tinyllama::TinyLlamaClient;
use std::io::Write;
use std::path::PathBuf;

pub struct KnowledgeChat {
    engine: Arc<KnowledgeEngine>,
    tinyllama_client: Arc<TinyLlamaClient>,
    response_generator: Arc<ComponentResponseGenerator>,
    intelligent_selector: Arc<IntelligentResponseSelector>,
    tinyllama_builder: Arc<TinyLlamaKnowledgeBuilder>,
    self_evaluator: Arc<SelfEvaluator>,
    conversation_memory: Arc<ConversationMemory>,
    conversation_history: Vec<(String, String)>, // (query, response) pairs
}

impl KnowledgeChat {
    pub fn new() -> Self {
        let engine = Arc::new(KnowledgeEngine::new());
        let tinyllama_builder = Arc::new(TinyLlamaKnowledgeBuilder::new(engine.clone()));
        
        // Check if we have cached knowledge from TinyLlama
        let cache_dir = PathBuf::from("./cache");
        let knowledge_files_dir = PathBuf::from("./knowledge_files");
        
        if cache_dir.exists() && cache_dir.join("response_cache.json").exists() {
            // Load cached knowledge
            println!("📂 Loading TinyLlama-built knowledge from cache...");
            let dynamic_loader = DynamicKnowledgeLoader::new(&knowledge_files_dir);
            match dynamic_loader.load_all(&engine) {
                Ok(count) => println!("✅ Loaded {} items from TinyLlama knowledge", count),
                Err(e) => println!("⚠️  Could not load knowledge files: {}", e),
            }
        } else {
            // Build knowledge from scratch with TinyLlama
            println!("🧠 Building knowledge from scratch with TinyLlama...");
            println!("⚡ This will take a moment but will provide O(1) cached responses!");
            
            let builder_clone = tinyllama_builder.clone();
            // Run the knowledge building in a separate thread to avoid runtime conflict
            std::thread::spawn(move || {
                let rt = tokio::runtime::Runtime::new().unwrap();
                rt.block_on(async {
                    builder_clone.build_from_scratch().await;
                });
            }).join().unwrap();
            
            println!("✅ TinyLlama knowledge building complete!");
        }
        
        let stats = engine.get_stats();
        println!("✅ Knowledge base ready with {} items across {} domains\n", 
            stats.total_nodes, 
            stats.domain_distribution.len()
        );
        
        // Initialize conversation memory for long-term contextual dialogue
        let conversation_memory = Arc::new(ConversationMemory::new(1000));
        
        let response_generator = Arc::new(ComponentResponseGenerator::new_with_memory(
            engine.clone(),
            conversation_memory.clone()
        ));
        let intelligent_selector = Arc::new(IntelligentResponseSelector::new(
            engine.clone(),
            response_generator.clone()
        ));
        
        // Initialize self-evaluator for continuous improvement
        let self_evaluator = Arc::new(SelfEvaluator::new(
            engine.clone(),
            response_generator.clone()
        ));
        
        let chat = Self { 
            engine,
            tinyllama_client: Arc::new(TinyLlamaClient::new()),
            response_generator,
            intelligent_selector,
            tinyllama_builder,
            self_evaluator,
            conversation_memory,
            conversation_history: Vec::new(),
        };
        
        // Start self-evaluation system in background
        let evaluator = chat.self_evaluator.clone();
        tokio::spawn(async move {
            println!("🧠 Starting self-evaluation system...");
            evaluator.start_background_evaluation().await;
        });
        
        chat
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
        
        // Store in conversation memory for long-term context
        self.conversation_memory.add_turn(query, &response);
        
        // Also keep in local history for backward compatibility
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
        
        // Try O(1) cached response first
        if let Some(cached) = self.tinyllama_builder.get_cached_response(&query_lower).await {
            print!(" [⚡ O(1) Cache]");
            println!();
            return cached;
        }
        
        // O(1) fast path for system commands and greetings
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
        
        // Use intelligent selector to get best response
        print!("🔄 Thinking");
        std::io::Write::flush(&mut std::io::stdout()).unwrap();
        
        // Show progress indicator
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
        
        // Generate response using actual knowledge base first
        let knowledge_response = self.response_generator.generate_response(expanded_query);
        
        // Stop progress indicator
        stop_progress.store(true, Ordering::Relaxed);
        let _ = progress_handle.join();
        
        // Check if response contains fallback text and clean it if needed
        if knowledge_response.contains("Additionally, i don't have specific information") ||
           knowledge_response.contains("Furthermore, i can help with topics") {
            // Extract just the knowledge content, remove fallback text
            let clean_response = knowledge_response
                .split("Additionally, i don't have specific information").next()
                .unwrap_or(&knowledge_response)
                .split("Furthermore, i can help with topics").next()
                .unwrap_or(&knowledge_response)
                .trim_end_matches(". ")
                .trim()
                .to_string();
            
            if clean_response.len() > 50 {
                print!(" [📚 Enhanced Knowledge]");
                println!();
                return clean_response;
            }
        }
        
        // CRITICAL: Check for high-quality conversational responses first (Turing test)
        // Perfect responses from Conversational, Identity, Humor, Mathematical components
        if (knowledge_response.contains("Hello! I'm Think AI") ||
            knowledge_response.contains("My name is Think AI") ||
            knowledge_response.contains("I'm Think AI") ||
            knowledge_response.contains("Here's a joke for you") ||
            knowledge_response.contains("=") && knowledge_response.len() < 20) &&
           !knowledge_response.contains("I don't have specific information") {
            print!(" [🎯 Perfect Response]");
            println!();
            return knowledge_response;
        }
        
        // If we got a good knowledge response without fallback text, use it
        if !knowledge_response.contains("I don't have specific information") && 
           !knowledge_response.contains("Could you please elaborate") &&
           knowledge_response.len() > 50 {
            print!(" [📚 Knowledge Base]");
            println!();
            return knowledge_response;
        }
        
        // Otherwise fall back to TinyLlama evaluation
        let response = self.tinyllama_builder.generate_evaluated_response(expanded_query).await;
        
        // Show that it's TinyLlama evaluated
        print!(" [🤖 TinyLlama Evaluated]");
        println!(); // New line after indicator
        
        response
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
        let eval_stats = self.self_evaluator.get_evaluation_stats();
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
            🧠 Self-Evaluation Statistics:\n\
            Total Self-Evaluations: {}\n\
            Average Response Quality: {:.2}\n\
            Recent Quality Trend: {:.2}\n\
            Improvement Areas: {}\n\
            Auto-Evaluation Active: {}\n\
            \n\
            Domain Distribution:\n{}",
            stats.total_nodes,
            domain_count,
            stats.average_confidence,
            eval_stats.total_evaluations,
            eval_stats.average_quality,
            eval_stats.recent_quality,
            eval_stats.improvement_areas,
            if eval_stats.is_running { "✅ Yes" } else { "❌ No" },
            domain_info
        )
    }
}