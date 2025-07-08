//! Full Think AI HTTP Server with Image Generation
//! Run with: cargo run --bin full-server-with-images

use anyhow::Result;
use std::net::SocketAddr;
use std::sync::Arc;
use tracing_subscriber;

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logging
    tracing_subscriber::fmt::init();
    
    println!("🚀 Starting Think AI Full Server with Image Generation...");
    
    // Initialize engines
    let engine = Arc::new(think_ai_core::O1Engine::new(
        think_ai_core::EngineConfig::default()
    ));
    
    // Initialize vector index
    let vector_index = Arc::new(think_ai_vector::O1VectorIndex::new(
        think_ai_vector::LSHConfig {
            dimension: 512,
            num_hash_tables: 10,
            num_hash_functions: 8,
            seed: 42,
        }
    ).unwrap());
    
    // Initialize knowledge engine
    let knowledge_engine = Arc::new(think_ai_knowledge::KnowledgeEngine::new());
    
    println!("✅ Engines initialized successfully");
    
    // Set up server address
    let port = std::env::var("PORT")
        .ok()
        .and_then(|p| p.parse::<u16>().ok())
        .unwrap_or(8080);
    
    let addr: SocketAddr = format!("0.0.0.0:{}", port).parse()?;
    
    println!("🎨 Image generation enabled with AI learning");
    println!("📦 O(1) caching for instant image retrieval");
    println!("🌐 Starting server on {}", addr);
    
    // Run the server with image generation support
    think_ai_http::server::run_server(addr, engine, vector_index, knowledge_engine).await
        .map_err(|e| anyhow::anyhow!("Server error: {}", e))?;
    
    Ok(())
}