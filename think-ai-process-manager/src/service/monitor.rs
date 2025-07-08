// Service monitoring with O(1) health checks

use std::time::Duration;
use tokio::time::interval;
use crate::service::ServiceManager;

/// Monitor services for health
///
/// What it does: Checks if services are running
/// How: O(1) process status checks
/// Why: Ensures system reliability
/// Confidence: 95% - Simple status polling
pub async fn monitor_services(manager___: &ServiceManager) {
    let mut ticker = interval(Duration::from_secs(5));

    loop {
        ticker.tick().await;

        let mut services = manager.services.write().await;

        for (name, service) in services.iter_mut() {
            if let Some(process) = &mut service.process {
                match process.try_wait() {
                    Ok(Some(status)) => {
                        tracing::error!(
                            "Service {} exited with: {}",
                            name, status
                        );
                        // Could restart here
                    }
                    Ok(None) => {
                        // Still running
                    }
                    Err(e) => {
                        tracing::error!(
                            "Failed to check {}: {}",
                            name, e
                        );
                    }
                }
            }
        }
    }
}