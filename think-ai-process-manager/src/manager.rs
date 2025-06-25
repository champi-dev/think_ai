//! High-level process management orchestration

use std::sync::Arc;
use std::collections::HashMap;
use indicatif::{ProgressBar, ProgressStyle};
use crate::{
    service::{ServiceManager, ServiceConfig},
    proxy::{ReverseProxy, Route},
    port::PortManager,
    Result,
};

/// Complete process manager
pub struct ProcessManager {
    pub service_manager: Arc<ServiceManager>,
    pub proxy: Arc<ReverseProxy>,
    pub port_manager: Arc<PortManager>,
}

impl ProcessManager {
    pub fn new() -> Self {
        Self {
            service_manager: Arc::new(ServiceManager::new()),
            proxy: Arc::new(ReverseProxy::new()),
            port_manager: Arc::new(PortManager::new()),
        }
    }
    
    /// Start all Think AI services
    pub async fn start_all(&self) -> Result<()> {
        let pb = ProgressBar::new(3);
        pb.set_style(ProgressStyle::default_bar()
            .template("{msg} [{bar:40}] {pos}/{len}")
            .unwrap());
        
        // Get main port from env or generate
        let main_port = std::env::var("PORT")
            .ok()
            .and_then(|p| p.parse().ok())
            .unwrap_or_else(|| self.port_manager.allocate());
        
        pb.set_message("Starting API server...");
        
        // Start API server
        let api_port = self.port_manager.allocate();
        let api_config = ServiceConfig {
            name: "api".to_string(),
            command: "cargo".to_string(),
            args: vec!["run".to_string(), "--bin".to_string(), 
                      "think-ai-server".to_string()],
            env: {
                let mut env = HashMap::new();
                env.insert("PORT".to_string(), api_port.to_string());
                env
            },
            port: api_port,
            working_dir: None,
        };
        
        self.service_manager.start(api_config).await?;
        pb.inc(1);
        
        // Add API route
        self.proxy.add_route(Route {
            path_prefix: "/api/".to_string(),
            target_host: "localhost".to_string(),
            target_port: api_port,
        }).await;
        
        pb.set_message("Starting CLI server...");
        
        // Start CLI server
        let cli_port = self.port_manager.allocate();
        let cli_config = ServiceConfig {
            name: "cli".to_string(),
            command: "cargo".to_string(),
            args: vec!["run".to_string(), "--bin".to_string(),
                      "think-ai".to_string(), "--".to_string(),
                      "server".to_string()],
            env: {
                let mut env = HashMap::new();
                env.insert("PORT".to_string(), cli_port.to_string());
                env
            },
            port: cli_port,
            working_dir: None,
        };
        
        self.service_manager.start(cli_config).await?;
        pb.inc(1);
        
        // Add CLI route
        self.proxy.add_route(Route {
            path_prefix: "/".to_string(),
            target_host: "localhost".to_string(),
            target_port: cli_port,
        }).await;
        
        pb.set_message("Starting reverse proxy...");
        
        // Start proxy
        let proxy = self.proxy.clone();
        tokio::spawn(async move {
            crate::proxy::server::start_proxy(proxy, main_port).await
        });
        
        pb.inc(1);
        pb.finish_with_message("All services started!");
        
        tracing::info!("System running on port {}", main_port);
        
        Ok(())
    }
}