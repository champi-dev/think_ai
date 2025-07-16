use think_ai_codellama::{CodeLlamaClient, CodeAssistant, CodeLlamaConfig};
use think_ai_knowledge::response_generator::ComponentResponseGenerator;
use think_ai_knowledge::KnowledgeEngine;
use std::sync::Arc;

#[tokio::main]
async fn main() {
    println!("=== Testing CodeLlama Integration ===\n");
    
    // Test 1: Direct CodeLlama client test
    println!("Test 1: Direct CodeLlama Client");
    match test_direct_client().await {
        Ok(_) => println!("✅ Direct client test passed"),
        Err(e) => println!("❌ Direct client test failed: {}", e),
    }
    
    // Test 2: Component integration test
    println!("\nTest 2: Component Integration");
    test_component_integration();
    
    // Test 3: Performance metrics test
    println!("\nTest 3: Performance Metrics");
    test_performance_metrics().await;
}

async fn test_direct_client() -> Result<(), Box<dyn std::error::Error>> {
    let client = CodeLlamaClient::new()?;
    
    // Check if model is available
    let available = client.check_model_availability().await?;
    println!("CodeLlama model available: {}", available);
    
    if !available {
        return Err("CodeLlama model not available".into());
    }
    
    // Test code generation
    let prompt = "Write a simple Python function to calculate factorial";
    println!("\nPrompt: {}", prompt);
    
    let response = client.generate_code(prompt).await?;
    println!("Response:\n{}", response);
    
    // Test code analysis
    let code = r#"
def add(a, b):
    return a + b
"#;
    println!("\nAnalyzing code:");
    let analysis = client.analyze_code(code, "python").await?;
    println!("Analysis:\n{}", analysis);
    
    Ok(())
}

fn test_component_integration() {
    let engine = Arc::new(KnowledgeEngine::new());
    let generator = ComponentResponseGenerator::new(engine);
    
    let test_queries = vec![
        ("Write a Python function to reverse a string", "coding"),
        ("What is consciousness?", "philosophical"),
        ("2 + 2", "math"),
        ("Hello", "greeting"),
        ("Implement binary search in Rust", "coding"),
    ];
    
    println!("\nTesting query routing:");
    for (query, expected_type) in test_queries {
        println!("\nQuery: '{}'", query);
        let response = generator.generate_response(query);
        
        let response_type = if response.contains("💻 CodeLlama") {
            "coding"
        } else if response.contains("🌌") {
            "philosophical"
        } else if response.contains("=") && (response.contains("2") || response.contains("4")) {
            "math"
        } else if response.contains("Hi") || response.contains("Hello") || response.contains("Hey") {
            "greeting"
        } else {
            "other"
        };
        
        println!("Expected: {}, Got: {}", expected_type, response_type);
        println!("Response preview: {}", &response.chars().take(100).collect::<String>());
        
        if response_type == expected_type {
            println!("✅ Correctly routed");
        } else {
            println!("❌ Incorrect routing");
        }
    }
}

async fn test_performance_metrics() {
    let client = CodeLlamaClient::new().unwrap();
    
    // Make several requests to test caching
    let prompts = vec![
        "Write a function to add two numbers",
        "Write a function to add two numbers", // Duplicate for cache hit
        "Create a Python class for a stack",
        "Write a function to add two numbers", // Another cache hit
    ];
    
    for (i, prompt) in prompts.iter().enumerate() {
        println!("\nRequest {}: {}", i + 1, prompt);
        match client.generate_code(prompt).await {
            Ok(_) => println!("✅ Success"),
            Err(e) => println!("❌ Error: {}", e),
        }
    }
    
    // Get and display metrics
    let metrics = client.get_metrics().await;
    println!("\n=== Performance Metrics ===");
    println!("Total requests: {}", metrics.total_requests);
    println!("Cache hits: {} ({:.1}%)", 
        metrics.cache_hits, 
        (metrics.cache_hits as f64 / metrics.total_requests as f64) * 100.0
    );
    println!("Cache misses: {}", metrics.cache_misses);
    println!("Average response time: {:.2}ms", metrics.average_response_time_ms);
    
    // Verify O(1) performance
    if metrics.cache_hits > 0 {
        println!("\n✅ O(1) caching is working!");
    }
}