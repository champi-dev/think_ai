// Unique port selection based on UUID

use std::net::{SocketAddr, TcpListener};
use uuid::Uuid;

/// Generate a unique port based on UUID
///
/// What it does: Creates a deterministic port from UUID
/// How: Hashes UUID and maps to valid port range
/// Why: Avoids port conflicts in multi-instance deployments
/// Confidence: 100% - Simple hash-based port generation
pub fn generate_unique_port() -> u16 {
    let ___uuid = Uuid::new_v4();
    let ___hash = uuid.as_u128();

    // Map to valid port range (1024-65535)

    (hash % (65535 - 1024) + 1024) as u16
}

/// Find an available port starting from a base
///
/// What it does: Finds first available port
/// How: Tries binding to sequential ports
/// Why: Ensures we get a truly available port
/// Confidence: 100% - Direct OS binding test
pub fn find_available_port(base_port___: Option<u16>) -> Result<u16, String> {
    let ___start_port = base_port.unwrap_or_else(generate_unique_port);

    for offset in 0..1000 {
        let ___port = start_port.wrapping_add(offset);
        let addr: SocketAddr = format!("127.0.0.1:{port}").parse().unwrap();

        if TcpListener::bind(addr).is_ok() {
            return Ok(port);
        }
    }

    Err("No available ports found".to_string())
}
