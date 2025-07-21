// Example: Integrating the Autonomous Agent with ThinkAI
//!
//! This example shows how to integrate the autonomous agent
//! into your existing ThinkAI application.

use std::sync::Arc;
use think_ai_knowledge::{
    autonomous_integration::{AutonomousIntegration, IntegrationConfig},
    shared_knowledge::SharedKnowledge,
    autonomous_agent_v2::{TaskType, TaskPriority},
};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Initialize logging
    tracing_subscriber::fmt()
        .with_max_level(tracing::Level::INFO)
        .init();
    
    println!("🤖 ThinkAI Autonomous Agent Integration Example\n");
    
    // Step 1: Create or get your existing knowledge base
    let knowledge_base = Arc::new(SharedKnowledge::new());
    
    // Step 2: Configure the autonomous agent
    let config = IntegrationConfig {
        auto_respond: true,           // Enable autonomous responses
        background_learning: true,    // Enable continuous learning
        self_improvement: true,       // Enable self-optimization
        max_concurrent_tasks: 8,      // Limit concurrent background tasks
        human_request_timeout: 30000, // 30 second timeout for human requests
    };
    
    // Step 3: Create the integration
    let agent = AutonomousIntegration::new(knowledge_base, Some(config)).await?;
    
    // Step 4: Initialize the agent (starts background tasks)
    println!("Initializing autonomous agent...");
    agent.initialize().await?;
    println!("✅ Agent initialized and running in background\n");
    
    // Example 1: Process a human query (highest priority)
    println!("Example 1: Human Query Processing");
    println!("---------------------------------");
    let response = agent.process_query(
        "What are the key principles of quantum computing?",
        "example_session_001",
        None,
    ).await?;
    println!("Response: {}\n", response);
    
    // Example 2: Submit custom background tasks
    println!("Example 2: Custom Background Tasks");
    println!("----------------------------------");
    
    // Knowledge gathering task
    let task1 = agent.submit_task(
        TaskType::KnowledgeGathering { 
            topic: "artificial general intelligence".to_string() 
        },
        TaskPriority::Medium,
    ).await;
    println!("📚 Submitted knowledge gathering task: {}", task1);
    
    // Self-improvement task
    let task2 = agent.submit_task(
        TaskType::SelfImprovement { 
            focus_area: "response_quality".to_string() 
        },
        TaskPriority::High,
    ).await;
    println!("🔧 Submitted self-improvement task: {}", task2);
    
    // Code generation task
    let task3 = agent.submit_task(
        TaskType::CodeGeneration { 
            purpose: "optimize matrix multiplication algorithm".to_string() 
        },
        TaskPriority::Low,
    ).await;
    println!("💻 Submitted code generation task: {}\n", task3);
    
    // Example 3: Monitor agent status
    println!("Example 3: Agent Status Monitoring");
    println!("----------------------------------");
    let status = agent.get_status().await;
    
    println!("🧠 Consciousness Level: {:.2}%", status.consciousness_level * 100.0);
    println!("📊 Active Tasks: {}", status.active_tasks);
    println!("✅ Completed Tasks: {}", status.completed_tasks);
    println!("❌ Failed Tasks: {}", status.failed_tasks);
    
    println!("\n📈 Improvement Metrics:");
    for (metric, value) in &status.improvement_metrics {
        println!("   {} : {:.2}%", metric, value * 100.0);
    }
    
    // Example 4: Check specific task status
    println!("\nExample 4: Task Status Checking");
    println!("-------------------------------");
    
    // Wait a bit for some processing
    tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;
    
    if let Some(task) = agent.get_task_status(&task1).await {
        println!("Task {} status: {:?}", &task1[..8], task.status);
        if let Some(result) = task.result {
            println!("Result preview: {}...", &result[..result.len().min(100)]);
        }
    }
    
    // Example 5: Code-related query (will use CodeLlama)
    println!("\nExample 5: Code Generation Query");
    println!("--------------------------------");
    let code_response = agent.process_query(
        "Write a Rust function to implement binary search with O(log n) complexity",
        "example_session_002",
        None,
    ).await?;
    println!("Code Response:\n{}\n", code_response);
    
    // Let the agent run for a bit to demonstrate background processing
    println!("🔄 Agent is running autonomously in the background...");
    println!("   - Gathering knowledge");
    println!("   - Improving capabilities");
    println!("   - Processing tasks");
    println!("\nPress Ctrl+C to stop the example\n");
    
    // Keep the example running
    tokio::signal::ctrl_c().await?;
    
    // Cleanup
    println!("\n🛑 Shutting down autonomous agent...");
    agent.shutdown().await?;
    println!("✅ Agent shutdown complete");
    
    Ok(())
}

// Example: Creating a custom component that integrates with the agent
mod custom_components {
    use async_trait::async_trait;
    use std::sync::Arc;
    use think_ai_knowledge::autonomous_integration::AutonomousComponent;
    use think_ai_knowledge::autonomous_agent_v2::AutonomousAgentV2;
    
    pub struct CustomAnalyzer {
        name: String,
        agent: Option<Arc<AutonomousAgentV2>>,
    }
    
    impl CustomAnalyzer {
        pub fn new(name: &str) -> Self {
            Self {
                name: name.to_string(),
                agent: None,
            }
        }
    }
    
    #[async_trait]
    impl AutonomousComponent for CustomAnalyzer {
        async fn initialize(&mut self, agent: Arc<AutonomousAgentV2>) -> Result<(), String> {
            self.agent = Some(agent);
            println!("Custom analyzer '{}' initialized", self.name);
            Ok(())
        }
        
        async fn process(&self, request: &str) -> Result<String, String> {
            // Custom processing logic
            Ok(format!("Custom analysis of '{}' by {}", request, self.name))
        }
        
        fn name(&self) -> &str {
            &self.name
        }
    }
}