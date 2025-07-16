// Test script to verify CodeLlama component functionality

use think_ai_knowledge::response_generator::ComponentResponseGenerator;
use think_ai_knowledge::KnowledgeEngine;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    // Initialize
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(knowledge_engine);
    
    println!("Testing CodeLlama Component:");
    println!("============================\n");
    
    // Test 1: Direct code request with model
    println!("Test 1: Direct code request with 'codellama' model");
    let response1 = generator.generate_response_with_model(
        "write a simple python server",
        Some("codellama")
    );
    println!("Response: {}\n", response1);
    
    // Test 2: Code request with [CODE REQUEST] prefix
    println!("Test 2: Code request with [CODE REQUEST] prefix");
    let response2 = generator.generate_response(
        "[CODE REQUEST] write a simple python server"
    );
    println!("Response: {}\n", response2);
    
    // Test 3: Regular code request without prefix
    println!("Test 3: Regular code request (should auto-detect)");
    let response3 = generator.generate_response(
        "write a simple python server"
    );
    println!("Response: {}\n", response3);
    
    // Test 4: JavaScript code request
    println!("Test 4: JavaScript async function");
    let response4 = generator.generate_response_with_model(
        "create a javascript async function to fetch data",
        Some("codellama")
    );
    println!("Response: {}\n", response4);
}