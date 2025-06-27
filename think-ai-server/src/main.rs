//! Think AI Server - Main server application

use std::{net::SocketAddr, sync::Arc};
use tracing::info;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize tracing
    think_ai_utils::logging::init_tracing();
    
    info!("Starting Think AI Server v0.1.0");
    
    // Initialize core engine
    let config = think_ai_core::EngineConfig::default();
    let engine = Arc::new(think_ai_core::O1Engine::new(config));
    engine.initialize().await?;
    
    info!("Core engine initialized");
    
    // Initialize vector index
    let vector_config = think_ai_vector::LSHConfig::default();
    let vector_index = Arc::new(think_ai_vector::O1VectorIndex::new(vector_config)?);
    
    info!("Vector index initialized");
    
    // Initialize knowledge engine
    let knowledge_engine = Arc::new(think_ai_knowledge::KnowledgeEngine::new());
    info!("Knowledge engine initialized");

    // Start HTTP server on port 8080
    let addr: SocketAddr = "127.0.0.1:8080".parse()?;
    info!("Starting HTTP server on port 8080");
    
    // Run server in background
    let server_handle = tokio::spawn(
        think_ai_http::server::run_server(addr, engine, vector_index, knowledge_engine)
    );
    
    // Wait for shutdown signal
    tokio::signal::ctrl_c().await?;
    info!("Shutting down...");
    
    server_handle.abort();
    
    Ok(())
}