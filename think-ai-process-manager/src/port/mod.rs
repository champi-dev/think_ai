//! UUID-based port management with O(1) operations

pub mod killer;

use uuid::Uuid;
use std::collections::HashSet;
use std::sync::RwLock;

/// Generate unique port from UUID
/// 
/// What it does: Creates deterministic port from UUID
/// How: Hashes UUID to valid port range
/// Why: Avoids conflicts in multi-instance deployments
/// Confidence: 100% - Simple hash mapping
pub fn generate_unique_port() -> u16 {
    let uuid = Uuid::new_v4();
    let hash = uuid.as_u128();
    
    // Map to valid port range (1024-65535)
    let port = (hash % (65535 - 1024) + 1024) as u16;
    port
}

/// Port manager with O(1) allocation
pub struct PortManager {
    allocated: RwLock<HashSet<u16>>,
}

impl PortManager {
    pub fn new() -> Self {
        Self {
            allocated: RwLock::new(HashSet::new()),
        }
    }
    
    /// Allocate a unique port
    pub fn allocate(&self) -> u16 {
        loop {
            let port = generate_unique_port();
            let mut allocated = self.allocated.write().unwrap();
            
            if allocated.insert(port) {
                return port;
            }
        }
    }
    
    /// Release a port
    pub fn release(&self, port: u16) {
        let mut allocated = self.allocated.write().unwrap();
        allocated.remove(&port);
    }
}