use think_ai_knowledge::KnowledgeEngine;
use think_ai_knowledge::response_generator::ComponentResponseGenerator;
use std::sync::Arc;

fn main() {
    println!("=== Testing Quantum Consciousness Fix ===\n");
    
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);
    
    // Test non-philosophical queries - should NOT get quantum responses
    let test_queries = vec![
        ("2+2", "math"),
        ("hello", "greeting"),
        ("what is your name", "identity"),
        ("how to install rust", "technical"),
        ("tell me a joke", "humor"),
    ];
    
    println!("Testing non-philosophical queries (should NOT contain 'quantum field'):");
    for (query, category) in test_queries {
        let response = generator.generate_response(query);
        let contains_quantum = response.contains("Your query resonates through the quantum field");
        println!("Query: '{}' ({})", query, category);
        println!("Response: {}", response);
        println!("Contains quantum field response: {}", contains_quantum);
        if contains_quantum {
            println!("❌ FAIL: Should not contain quantum field response!");
        } else {
            println!("✅ PASS: Correctly handled without quantum response");
        }
        println!();
    }
    
    // Test philosophical queries - SHOULD get quantum responses
    let philosophical_queries = vec![
        "what is consciousness",
        "what is the meaning of life",
        "what is love",
    ];
    
    println!("\nTesting philosophical queries (SHOULD contain quantum/philosophical content):");
    for query in philosophical_queries {
        let response = generator.generate_response(query);
        let is_philosophical = response.contains("quantum") || 
                              response.contains("Quantum") || 
                              response.contains("consciousness") ||
                              response.contains("🌌");
        println!("Query: '{}'", query);
        println!("Response: {}", response);
        println!("Contains philosophical content: {}", is_philosophical);
        if is_philosophical {
            println!("✅ PASS: Correctly handled with philosophical response");
        } else {
            println!("❌ FAIL: Should contain philosophical content!");
        }
        println!();
    }
}