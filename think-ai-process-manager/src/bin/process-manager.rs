// Think AI Process Manager CLI

use think_ai_process_manager::{
    manager::ProcessManager,
    Result,
    service::monitor::monitor_services,
};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};
#[tokio::main]
async fn main() -> Result<()> {
    // Initialize tracing
    tracing_subscriber::registry()
        .with(tracing_subscriber::EnvFilter::new(
            std::env::var("RUST_LOG")
                .unwrap_or_else(|_| "info".to_string())
        ))
        .with(tracing_subscriber::fmt::layer())
        .init();
    tracing::info!("Starting Think AI Process Manager");
    // Create manager
    let manager = ProcessManager::new();
    // Start all services
    manager.start_all().await?;
    // Monitor services
    let service_manager = manager.service_manager.clone();
    let monitor_handle = tokio::spawn(async move {
        monitor_services(&service_manager).await;
    });
    // Wait for shutdown signal
    tokio::signal::ctrl_c().await?;
    tracing::info!("Shutting down...");
    // Cleanup would go here
    Ok(())
}
