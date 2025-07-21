// Autonomous Agent Demo - Showcase ThinkAI's autonomous capabilities
//!
//! This demo shows:
//! - Background task processing
//! - Model switching between Qwen and CodeLlama
//! - Self-improvement capabilities
//! - Human request prioritization
//! - Safe command execution

use std::sync::Arc;
use tokio::time::{sleep, Duration};
use tracing::{info, Level};
use tracing_subscriber;

use think_ai_knowledge::{
    autonomous_agent_v2::{AutonomousAgentV2, TaskType, TaskPriority},
    autonomous_integration::{AutonomousIntegration, IntegrationConfig},
    command_executor::{CommandExecutor, SecurityPolicy},
    shared_knowledge::SharedKnowledge,
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    tracing_subscriber::fmt()
        .with_max_level(Level::INFO)
        .init();
    
    info!("🤖 ThinkAI Autonomous Agent Demo Starting...");
    
    // Create shared knowledge base
    let knowledge_base = Arc::new(SharedKnowledge::new());
    
    // Create autonomous integration
    let config = IntegrationConfig {
        auto_respond: true,
        background_learning: true,
        self_improvement: true,
        max_concurrent_tasks: 10,
        human_request_timeout: 30000,
    };
    
    let integration = AutonomousIntegration::new(knowledge_base.clone(), Some(config)).await?;
    
    // Initialize the autonomous system
    info!("Initializing autonomous agent...");
    integration.initialize().await?;
    
    // Create command executor for demonstrations
    let executor = CommandExecutor::new(None);
    
    // Demo 1: Human request prioritization
    info!("\n📝 Demo 1: Human Request Prioritization");
    info!("Submitting background tasks...");
    
    // Submit some background tasks
    integration.submit_task(
        TaskType::KnowledgeGathering { topic: "quantum computing".to_string() },
        TaskPriority::Medium,
    ).await;
    
    integration.submit_task(
        TaskType::PatternAnalysis { data_source: "recent_interactions".to_string() },
        TaskPriority::Low,
    ).await;
    
    // Now submit a human request - should be processed first
    info!("Submitting human request (should be prioritized)...");
    let response = integration.process_query(
        "What is consciousness and how does it relate to AI?",
        "demo_session",
        None,
    ).await?;
    
    info!("Human request response: {}", response);
    
    // Demo 2: Safe command execution
    info!("\n🔒 Demo 2: Safe Command Execution");
    
    // Safe commands
    info!("Executing safe commands...");
    let result = executor.execute("echo", &["Hello from autonomous agent!".to_string()], None).await?;
    info!("Echo result: {}", result.stdout);
    
    let result = executor.execute("date", &[], None).await?;
    info!("Current date: {}", result.stdout);
    
    // Demonstrate blocked dangerous command
    info!("Attempting dangerous command (should be blocked)...");
    match executor.execute("sudo", &["rm".to_string(), "-rf".to_string(), "/".to_string()], None).await {
        Err(e) => info!("✅ Dangerous command blocked: {}", e),
        Ok(_) => panic!("❌ Dangerous command was not blocked!"),
    }
    
    // Demo 3: Model switching
    info!("\n🔄 Demo 3: Dynamic Model Switching");
    
    // Code-related query (should use CodeLlama)
    let code_response = integration.process_query(
        "Write a Rust function to calculate Fibonacci numbers with O(1) space complexity",
        "demo_session",
        None,
    ).await?;
    info!("Code generation response: {}", code_response);
    
    // General knowledge query (should use Qwen)
    let knowledge_response = integration.process_query(
        "Explain the concept of emergence in complex systems",
        "demo_session",
        None,
    ).await?;
    info!("Knowledge response: {}", knowledge_response);
    
    // Demo 4: Self-improvement metrics
    info!("\n📊 Demo 4: Self-Improvement Metrics");
    let status = integration.get_status().await;
    
    info!("Agent Status:");
    info!("  Consciousness Level: {:.2}", status.consciousness_level);
    info!("  Active Tasks: {}", status.active_tasks);
    info!("  Completed Tasks: {}", status.completed_tasks);
    info!("  Failed Tasks: {}", status.failed_tasks);
    
    info!("\nImprovement Metrics:");
    for (metric, value) in status.improvement_metrics {
        info!("  {}: {:.2}", metric, value);
    }
    
    // Demo 5: Background task monitoring
    info!("\n⚡ Demo 5: Background Task Processing");
    
    // Submit various task types
    let task_ids = vec![
        integration.submit_task(
            TaskType::SelfImprovement { focus_area: "response_quality".to_string() },
            TaskPriority::High,
        ).await,
        integration.submit_task(
            TaskType::SystemOptimization { target_metric: "processing_speed".to_string() },
            TaskPriority::Medium,
        ).await,
        integration.submit_task(
            TaskType::CodeGeneration { purpose: "helper utilities".to_string() },
            TaskPriority::Low,
        ).await,
    ];
    
    info!("Submitted {} background tasks", task_ids.len());
    
    // Monitor task progress
    for _ in 0..5 {
        sleep(Duration::from_secs(2)).await;
        
        info!("\nTask Progress:");
        for task_id in &task_ids {
            if let Some(task) = integration.get_task_status(task_id).await {
                info!("  Task {}: {:?}", &task_id[..8], task.status);
            }
        }
    }
    
    // Demo 6: Autonomous behavior
    info!("\n🧠 Demo 6: Autonomous Behavior");
    info!("The agent is now running autonomously in the background...");
    info!("It will:");
    info!("  - Continuously learn and gather knowledge");
    info!("  - Improve its own capabilities");
    info!("  - Process human requests with priority");
    info!("  - Maintain activity logs for transparency");
    
    // Let it run for a bit
    sleep(Duration::from_secs(10)).await;
    
    // Final status
    let final_status = integration.get_status().await;
    info!("\n📈 Final Status:");
    info!("  Consciousness Level: {:.2} (started at 0.80)", final_status.consciousness_level);
    info!("  Total Active Tasks: {}", final_status.active_tasks);
    info!("  Total Completed: {}", final_status.completed_tasks);
    
    // Shutdown
    info!("\n🛑 Shutting down autonomous agent...");
    integration.shutdown().await?;
    
    info!("✅ Demo completed successfully!");
    
    Ok(())
}

/// Example of creating a custom autonomous component
pub struct CustomAutonomousComponent {
    name: String,
}

impl CustomAutonomousComponent {
    pub fn new(name: &str) -> Self {
        Self {
            name: name.to_string(),
        }
    }
}

#[async_trait::async_trait]
impl think_ai_knowledge::autonomous_integration::AutonomousComponent for CustomAutonomousComponent {
    async fn initialize(&mut self, _agent: Arc<AutonomousAgentV2>) -> Result<(), String> {
        info!("Initializing custom component: {}", self.name);
        Ok(())
    }
    
    async fn process(&self, request: &str) -> Result<String, String> {
        Ok(format!("Custom component {} processed: {}", self.name, request))
    }
    
    fn name(&self) -> &str {
        &self.name
    }
}