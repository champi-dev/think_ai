//! HTTP server implementation with O(1) routing

pub mod port_manager;

use std::{net::SocketAddr, sync::Arc};
use crate::router::{AppState, create_router};
use tracing::info;

pub async fn run_server(
    addr: SocketAddr,
    engine: Arc<think_ai_core::O1Engine>,
    vector_index: Arc<think_ai_vector::O1VectorIndex>,
) -> crate::Result<()> {
    // Kill any process using the port
    let port = addr.port();
    if let Err(e) = port_manager::kill_port(port) {
        tracing::warn!("Failed to kill port {}: {}", port, e);
    } else {
        info!("Port {} cleared", port);
    }
    
    let state = Arc::new(AppState {
        engine,
        vector_index,
    });
    
    let app = create_router(state);
    
    let listener = tokio::net::TcpListener::bind(addr).await
        .map_err(|e| crate::HttpError::ServerError(e.to_string()))?;
    
    info!("Server listening on {}", addr);
    
    axum::serve(listener, app).await
        .map_err(|e| crate::HttpError::ServerError(e.to_string()))?;
    
    Ok(())
}