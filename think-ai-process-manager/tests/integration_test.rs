// Process manager integration tests

use think_ai_process_manager::{
    manager::ProcessManager,
    service::ServiceConfig,
    proxy::Route,
    Result,
};
use std::collections::HashMap;
#[tokio::test]
async fn test_process_manager() -> Result<()> {
    println!("\n=== Testing Process Manager ===\n");
    // Create manager
    let manager = ProcessManager::new();
    // Test port allocation
    let port1 = manager.port_manager.allocate();
    let port2 = manager.port_manager.allocate();
    assert_ne!(port1, port2);
    println!("✓ UUID-based port allocation working: {} and {}", port1, port2);
    // Test service config
    let config = ServiceConfig {
        name: "test-service".to_string(),
        command: "echo".to_string(),
        args: vec!["Test service running".to_string()],
        env: HashMap::new(),
        port: port1,
        working_dir: None,
    };
    // Start service
    manager.service_manager.start(config).await?;
    println!("✓ Service started successfully");
    // Add proxy route
    manager.proxy.add_route(Route {
        path_prefix: "/test/".to_string(),
        target_host: "localhost".to_string(),
        target_port: port1,
    }).await;
    println!("✓ Proxy route added");
    // Release port
    manager.port_manager.release(port1);
    println!("✓ Port released");
    println!("\nProcess manager test passed!");
    Ok(())
}
