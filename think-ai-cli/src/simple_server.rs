use std::sync::Arc;

pub async fn run_simple_server(host: &str, port: u16) -> Result<(), Box<dyn std::error::Error>> {
    println!("🚀 Starting Think AI Server on {}:{}", host, port);

    // Initialize core engine
    let config = think_ai_core::EngineConfig::default();
    let engine = Arc::new(think_ai_core::O1Engine::new(config));
    engine.initialize().await?;

    // Initialize vector index
    let vector_config = think_ai_vector::LSHConfig::default();
    let vector_index = Arc::new(think_ai_vector::O1VectorIndex::new(vector_config)?);

    // Simple knowledge engine (without the broken knowledge module)
    let knowledge_engine = Arc::new(think_ai_knowledge::KnowledgeEngine::new());

    println!("✅ Engine initialized successfully");

    // Start HTTP server
    let addr: std::net::SocketAddr = format!("{}:{}", host, port).parse()?;
    println!("🌐 Server listening on http://{}", addr);

    // Use the HTTP server module
    think_ai_http::server::run_server(addr, engine, vector_index, knowledge_engine).await?;

    Ok(())
}