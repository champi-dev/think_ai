use std::sync::Arc;

fn main() {
    println!("🔍 Testing Think AI search...");
    
    // Initialize knowledge engine
    let knowledge_engine = Arc::new(think_ai_knowledge::KnowledgeEngine::new());
    
    // Load knowledge from JSON files
    let knowledge_files_dir = std::path::PathBuf::from("./knowledge_files");
    if knowledge_files_dir.exists() {
        let dynamic_loader = think_ai_knowledge::dynamic_loader::DynamicKnowledgeLoader::new(&knowledge_files_dir);
        match dynamic_loader.load_all(&knowledge_engine) {
            Ok(count) => println!("✅ Loaded {} items from knowledge files", count),
            Err(e) => println!("⚠️  Could not load knowledge files: {}", e),
        }
    }
    
    // Test queries
    let queries = vec![
        "what is the universe",
        "universe", 
        "what is gravity",
        "gravity"
    ];
    
    for query in queries {
        println!("\n🔍 Testing query: '{}'", query);
        
        // Test intelligent_query
        let results = knowledge_engine.intelligent_query(query);
        println!("   intelligent_query returned {} results:", results.len());
        for (i, node) in results.iter().take(3).enumerate() {
            println!("   {}. {} - {}", i+1, node.topic, &node.content.chars().take(100).collect::<String>());
        }
        
        // Test regular query
        if let Some(regular_results) = knowledge_engine.query(query) {
            println!("   regular query returned {} results:", regular_results.len());
            for (i, node) in regular_results.iter().take(3).enumerate() {
                println!("   {}. {} - {}", i+1, node.topic, &node.content.chars().take(100).collect::<String>());
            }
        } else {
            println!("   regular query returned None");
        }
    }
}