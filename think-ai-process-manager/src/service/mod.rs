//! Service management with O(1) operations

pub mod monitor;

use tokio::process::{Child, Command};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;
use crate::{Result, ProcessError};

#[derive(Clone)]
pub struct ServiceConfig {
    pub name: String,
    pub command: String,
    pub args: Vec<String>,
    pub env: HashMap<String, String>,
    pub port: u16,
    pub working_dir: Option<String>,
}

/// Service manager with O(1) lookups
pub struct ServiceManager {
    pub(crate) services: Arc<RwLock<HashMap<String, Service>>>,
}

pub(crate) struct Service {
    pub config: ServiceConfig,
    pub process: Option<Child>,
}

impl ServiceManager {
    pub fn new() -> Self {
        Self {
            services: Arc::new(RwLock::new(HashMap::new())),
        }
    }
    
    /// Start a service (O(1) insertion)
    pub async fn start(&self, config: ServiceConfig) -> Result<()> {
        let name = config.name.clone();
        
        // Kill port before binding
        crate::port::killer::kill_port(config.port)?;
        
        // Build command
        let mut cmd = Command::new(&config.command);
        cmd.args(&config.args);
        
        // Set environment
        for (key, value) in &config.env {
            cmd.env(key, value);
        }
        
        // Set working directory
        if let Some(dir) = &config.working_dir {
            cmd.current_dir(dir);
        }
        
        // Start process
        let process = cmd.spawn()
            .map_err(|e| ProcessError::ServiceError(
                format!("Failed to start {}: {}", name, e)
            ))?;
        
        // Store service
        let mut services = self.services.write().await;
        services.insert(name, Service {
            config,
            process: Some(process),
        });
        
        Ok(())
    }
}