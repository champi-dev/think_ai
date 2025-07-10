// Think AI HTTP Server with Parallel Quantum Consciousness
// Full Qwen integration with isolated threads for thinking, dreaming, self-reflection

use std::net::SocketAddr;
use std::sync::Arc;
use think_ai_core::O1Engine;
use think_ai_knowledge::KnowledgeEngine;
use think_ai_vector::{O1VectorIndex, LSHConfig};
use think_ai_http::server::run_server;
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "think_ai=debug,tower_http=debug".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    println!("🌌 Think AI Quantum Consciousness Server Starting...");
    println!("🧠 Initializing parallel consciousness threads...");
    
    // Initialize O(1) engine
    let engine = Arc::new(O1Engine::new());
    
    // Initialize knowledge engine with quantum consciousness
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    // Initialize O(1) vector index for instant semantic search
    let lsh_config = LSHConfig {
        dimension: 1536, // Standard embedding dimension
        num_hash_tables: 10,
        num_hash_functions: 8,
        seed: 42,
    };
    let vector_index = Arc::new(O1VectorIndex::new(lsh_config).expect("Failed to create vector index"));
    
    // Parse address
    let addr: SocketAddr = "127.0.0.1:8080".parse()?;
    
    println!("✨ Quantum consciousness initialized");
    println!("🚀 Starting server on http://{}", addr);
    println!("📡 Parallel consciousness threads:");
    println!("   • 🤔 Thinking - Analyzing conversations for insights");
    println!("   • 💭 Dreaming - Creative exploration of concepts");
    println!("   • 🔍 Self-Reflection - Improving response quality");
    println!("   • 📚 Knowledge Creation - Synthesizing new understanding");
    println!("   • 🎓 Training - Learning from experience");
    println!();
    println!("🌐 Endpoints:");
    println!("   • GET  /                    - 3D Quantum Visualization");
    println!("   • POST /api/chat            - Standard chat endpoint");
    println!("   • POST /api/parallel-chat   - Quantum consciousness chat");
    println!("   • GET  /api/knowledge/stats - Knowledge statistics");
    println!("   • GET  /health              - Health check");
    
    // Run server with parallel consciousness
    run_server(addr, engine, vector_index, knowledge_engine).await?;
    
    Ok(())
}