//! HTTP server implementation with O(1) routing

pub mod port_manager;
pub mod port_selector;

use std::{net::SocketAddr, sync::Arc};
use crate::router::{AppState, create_router};
use tracing::info;

pub async fn run_server(
    addr: SocketAddr,
    engine: Arc<think_ai_core::O1Engine>,
    vector_index: Arc<think_ai_vector::O1VectorIndex>,
    knowledge_engine: Arc<think_ai_knowledge::KnowledgeEngine>,
) -> crate::Result<()> {
    // Use UUID-based unique port if needed
    let final_port = if addr.port() == 0 {
        port_selector::find_available_port(None)
            .map_err(|e| crate::HttpError::ServerError(e))?
    } else {
        // Kill any process using the specified port
        let port = addr.port();
        if let Err(e) = port_manager::kill_port(port) {
            tracing::warn!("Failed to kill port {}: {}", port, e);
            // Try to find alternative port
            port_selector::find_available_port(Some(port))
                .map_err(|e| crate::HttpError::ServerError(e))?
        } else {
            info!("Port {} cleared", port);
            port
        }
    };
    
    let final_addr: SocketAddr = format!("{}:{}", addr.ip(), final_port)
        .parse()
        .map_err(|e: std::net::AddrParseError| 
            crate::HttpError::ServerError(e.to_string()))?;
    
    let state = Arc::new(AppState {
        engine,
        vector_index,
        knowledge_engine,
    });
    
    let app = create_router(state);
    
    let listener = tokio::net::TcpListener::bind(final_addr).await
        .map_err(|e| crate::HttpError::ServerError(e.to_string()))?;
    
    info!("Server listening on {}", final_addr);
    
    axum::serve(listener, app).await
        .map_err(|e| crate::HttpError::ServerError(e.to_string()))?;
    
    Ok(())
}