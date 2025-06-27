//! Build knowledge from scratch using TinyLlama evaluation

use think_ai_knowledge::{KnowledgeEngine, tinyllama_knowledge_builder::TinyLlamaKnowledgeBuilder};
use std::sync::Arc;

#[tokio::main]
async fn main() {
    println!("🚀 Think AI Knowledge Builder with TinyLlama");
    println!("============================================\n");
    
    // Create knowledge engine
    let engine = Arc::new(KnowledgeEngine::new());
    
    // Create TinyLlama knowledge builder
    let builder = TinyLlamaKnowledgeBuilder::new(engine.clone());
    
    // Build knowledge from scratch
    println!("🏗️  Building knowledge from scratch...");
    builder.build_from_scratch().await;
    
    // Show stats
    let stats = engine.get_stats();
    println!("\n📊 Knowledge Building Complete!");
    println!("Total nodes: {}", stats.total_nodes);
    println!("Total items: {}", stats.total_knowledge_items);
    println!("\nDomain distribution:");
    for (domain, count) in stats.domain_distribution {
        println!("  {:?}: {}", domain, count);
    }
    
    // Test some queries with O(1) cache
    println!("\n🧪 Testing O(1) cached responses:");
    
    let test_queries = vec![
        "what is love",
        "what is consciousness",
        "tell me about mars",
        "explain programming",
        "hello",
    ];
    
    for query in test_queries {
        println!("\n💬 Query: '{}'", query);
        let start = std::time::Instant::now();
        
        // Try O(1) cache first
        if let Some(cached) = builder.get_cached_response(query).await {
            let elapsed = start.elapsed().as_micros();
            println!("⚡ Response ({}μs): {}", elapsed, cached);
        } else {
            // Generate and cache
            let response = builder.generate_evaluated_response(query).await;
            let elapsed = start.elapsed().as_millis();
            println!("🔄 Generated ({}ms): {}", elapsed, response);
        }
    }
    
    println!("\n✅ Knowledge building and caching complete!");
}