#!/bin/bash
set -e

echo "Direct test of response generation..."

# Create a simple Rust test
cat > test_response_direct.rs << 'EOF'
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
EOF

# Compile and run
echo "Compiling test..."
rustc --edition 2021 test_response_direct.rs \
    -L target/release/deps \
    --extern think_ai_knowledge=target/release/libthink_ai_knowledge.rlib \
    $(find target/release/deps -name "*.rlib" | sed 's/^/--extern /' | tr '\n' ' ') \
    -o test_response_direct 2>/dev/null || {
        echo "Direct compile failed, using cargo test instead..."
        cargo test --lib response_generator 2>&1 | grep -E "(test result:|ERROR:|passed)"
        exit $?
    }

echo "Running test..."
./test_response_direct