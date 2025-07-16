use std::sync::Arc;
use think_ai_knowledge::KnowledgeEngine;
use think_ai_knowledge::response_generator::ComponentResponseGenerator;

fn main() {
    println!("Testing LLM initialization issue...");
    
    // Create knowledge engine
    let engine = Arc::new(KnowledgeEngine::new());
    
    // Create response generator
    let generator = ComponentResponseGenerator::new(engine.clone());
    
    // Test various queries that might trigger the error
    let test_queries = vec![
        "hello",
        "what is consciousness",
        "explain quantum mechanics",
        "how does AI work",
        "what is the meaning of life",
        "tell me about physics",
        "Previous conversation:\nuser: hello\nassistant: Hi!\n\nCurrent query: what is AI",
    ];
    
    for query in test_queries {
        println!("\n--- Testing query: '{}' ---", query);
        let response = generator.generate_response(query);
        println!("Response: {}", response);
        
        if response.contains("Knowledge engine LLM not initialized") {
            println!("ERROR: Found the LLM initialization error!");
        }
    }
}