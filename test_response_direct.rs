use std::sync::Arc;
use think_ai_knowledge::KnowledgeEngine;
use think_ai_knowledge::response_generator::ComponentResponseGenerator;

fn main() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);
    
    // Test queries that previously caused issues
    let queries = vec![
        ("hello", "conversational"),
        ("what is consciousness", "philosophical"),  
        ("explain relativity", "scientific"),
        ("how do computers work", "technical"),
        ("what is the meaning of life", "philosophical"),
        ("tell me about evolution", "scientific"),
    ];
    
    let mut has_error = false;
    
    for (query, expected_type) in queries {
        println!("\n--- Testing '{}' (expecting {} response) ---", query, expected_type);
        let response = generator.generate_response(query);
        
        if response.contains("Knowledge engine LLM not initialized") {
            println!("ERROR: LLM initialization error found!");
            has_error = true;
        } else {
            println!("OK: Got valid response");
            println!("Response preview: {}...", &response[..response.len().min(100)]);
        }
    }
    
    if has_error {
        println!("\n❌ FAILED: LLM initialization errors detected");
        std::process::exit(1);
    } else {
        println!("\n✅ SUCCESS: All queries handled without LLM errors");
    }
}
