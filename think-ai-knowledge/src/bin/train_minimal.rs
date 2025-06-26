use std::sync::Arc;
use think_ai_knowledge::{KnowledgeEngine, KnowledgeDomain, persistence::KnowledgePersistence};

fn main() {
    println!("🚀 Think AI Minimal Training");
    println!("=============================\n");

    let engine = Arc::new(KnowledgeEngine::new());
    
    // Add only essential routing knowledge for common queries
    // The LLM engine will handle actual response generation
    println!("📊 Adding minimal routing knowledge...");
    
    // Basic greetings
    engine.add_knowledge(
        KnowledgeDomain::Philosophy,
        "hello".to_string(),
        "greeting".to_string(),
        vec!["greeting".to_string()],
    );
    
    engine.add_knowledge(
        KnowledgeDomain::Philosophy,
        "hi".to_string(),
        "greeting".to_string(),
        vec!["greeting".to_string()],
    );
    
    // Common queries - just mark them for LLM handling
    engine.add_knowledge(
        KnowledgeDomain::Philosophy,
        "what can you do".to_string(),
        "capabilities".to_string(),
        vec!["capabilities".to_string()],
    );
    
    // Save the minimal knowledge
    let all_nodes = engine.get_all_nodes();
    println!("\n💾 Saving {} routing items...", all_nodes.len());
    
    match KnowledgePersistence::new("minimal_routing") {
        Ok(persistence) => {
            match persistence.save_checkpoint(&all_nodes, 1) {
                Ok(_) => println!("✅ Routing knowledge saved successfully!"),
                Err(e) => println!("❌ Failed to save: {}", e),
            }
        }
        Err(e) => println!("❌ Failed to create persistence: {}", e),
    }
    
    println!("\n✨ Training complete! The LLM engine will handle response generation.");
}