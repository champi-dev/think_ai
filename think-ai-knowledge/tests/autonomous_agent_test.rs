// Comprehensive tests for the autonomous agent system

use std::sync::Arc;
use std::time::Duration;
use tokio::time::sleep;

use think_ai_knowledge::{
    autonomous_agent_v2::{AutonomousAgentV2, TaskType, TaskPriority, TaskStatus},
    autonomous_integration::{AutonomousIntegration, IntegrationConfig},
    command_executor::{CommandExecutor, SecurityPolicy, ExecutionResult},
    shared_knowledge::SharedKnowledge,
};

#[tokio::test]
async fn test_autonomous_agent_creation() {
    let knowledge_base = Arc::new(SharedKnowledge::new());
    let agent = AutonomousAgentV2::new(knowledge_base).await;
    
    assert_eq!(agent.consciousness_level(), 0.8);
    assert!(agent.get_active_tasks().await.is_empty());
}

#[tokio::test]
async fn test_task_submission_and_priority() {
    let knowledge_base = Arc::new(SharedKnowledge::new());
    let agent = AutonomousAgentV2::new(knowledge_base).await;
    
    // Submit tasks with different priorities
    let low_task = agent.submit_task(
        TaskType::PatternAnalysis { data_source: "test".to_string() },
        TaskPriority::Low,
    ).await;
    
    let high_task = agent.submit_task(
        TaskType::SelfImprovement { focus_area: "test".to_string() },
        TaskPriority::High,
    ).await;
    
    let critical_task = agent.submit_task(
        TaskType::HumanRequest { 
            query: "test".to_string(),
            session_id: "test".to_string()
        },
        TaskPriority::Critical,
    ).await;
    
    // Verify tasks were submitted
    assert!(!low_task.is_empty());
    assert!(!high_task.is_empty());
    assert!(!critical_task.is_empty());
}

#[tokio::test]
async fn test_integration_initialization() {
    let knowledge_base = Arc::new(SharedKnowledge::new());
    let config = IntegrationConfig {
        auto_respond: true,
        background_learning: false, // Disable for testing
        self_improvement: false,    // Disable for testing
        max_concurrent_tasks: 5,
        human_request_timeout: 5000,
    };
    
    let integration = AutonomousIntegration::new(knowledge_base, Some(config)).await;
    assert!(integration.is_ok());
}

#[tokio::test]
async fn test_command_executor_safe_commands() {
    let executor = CommandExecutor::new(None);
    
    // Test safe echo command
    let result = executor.execute("echo", &["test".to_string()], None).await;
    assert!(result.is_ok());
    let result = result.unwrap();
    assert_eq!(result.stdout.trim(), "test");
    assert_eq!(result.exit_code, Some(0));
    
    // Test safe ls command
    let result = executor.execute("ls", &["-la".to_string(), "/tmp".to_string()], None).await;
    assert!(result.is_ok());
}

#[tokio::test]
async fn test_command_executor_forbidden_commands() {
    let executor = CommandExecutor::new(None);
    
    // Test forbidden sudo command
    let result = executor.execute("sudo", &["ls".to_string()], None).await;
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("not allowed"));
    
    // Test dangerous rm command
    let result = executor.execute("rm", &["-rf".to_string(), "/".to_string()], None).await;
    assert!(result.is_err());
}

#[tokio::test]
async fn test_command_executor_rate_limiting() {
    let mut policy = SecurityPolicy::default();
    policy.rate_limit_per_minute = 2;
    
    let executor = CommandExecutor::new(Some(policy));
    
    // First two should succeed
    let result1 = executor.execute("echo", &["1".to_string()], None).await;
    assert!(result1.is_ok());
    
    let result2 = executor.execute("echo", &["2".to_string()], None).await;
    assert!(result2.is_ok());
    
    // Third should fail due to rate limit
    let result3 = executor.execute("echo", &["3".to_string()], None).await;
    assert!(result3.is_err());
    assert!(result3.unwrap_err().contains("Rate limit"));
}

#[tokio::test]
async fn test_command_executor_timeout() {
    let mut policy = SecurityPolicy::default();
    policy.max_execution_time = Duration::from_millis(100);
    
    let executor = CommandExecutor::new(Some(policy));
    
    // Command that takes too long should timeout
    let result = executor.execute("sleep", &["1".to_string()], None).await;
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("timed out"));
}

#[tokio::test]
async fn test_task_lifecycle() {
    let knowledge_base = Arc::new(SharedKnowledge::new());
    let agent = AutonomousAgentV2::new(knowledge_base).await;
    
    // Submit a task
    let task_id = agent.submit_task(
        TaskType::KnowledgeGathering { topic: "test".to_string() },
        TaskPriority::Medium,
    ).await;
    
    // Check initial status
    let status = agent.get_task_status(&task_id).await;
    assert!(status.is_some());
    let task = status.unwrap();
    assert_eq!(task.status, TaskStatus::Pending);
    assert!(task.started_at.is_none());
    assert!(task.completed_at.is_none());
}

#[tokio::test]
async fn test_improvement_metrics() {
    let knowledge_base = Arc::new(SharedKnowledge::new());
    let agent = AutonomousAgentV2::new(knowledge_base).await;
    
    let metrics = agent.get_improvement_metrics();
    
    // Check default metrics exist
    assert!(metrics.contains_key("response_quality"));
    assert!(metrics.contains_key("task_efficiency"));
    assert!(metrics.contains_key("knowledge_depth"));
    assert!(metrics.contains_key("code_quality"));
    
    // Check metric values are reasonable
    for (_, value) in metrics {
        assert!(value >= 0.0 && value <= 1.0);
    }
}

#[tokio::test]
async fn test_consciousness_level() {
    let knowledge_base = Arc::new(SharedKnowledge::new());
    let agent = AutonomousAgentV2::new(knowledge_base).await;
    
    // Initial consciousness level
    let initial_level = agent.consciousness_level();
    assert_eq!(initial_level, 0.8);
    
    // Consciousness should be between 0 and 1
    assert!(initial_level >= 0.0 && initial_level <= 1.0);
}

#[tokio::test]
async fn test_activity_logging() {
    let knowledge_base = Arc::new(SharedKnowledge::new());
    let agent = AutonomousAgentV2::new(knowledge_base).await;
    
    // Submit a task to generate activity
    let task_id = agent.submit_task(
        TaskType::SystemOptimization { target_metric: "test".to_string() },
        TaskPriority::Low,
    ).await;
    
    // Check logs exist
    let logs = agent.get_task_logs(&task_id).await;
    assert!(!logs.is_empty());
    
    // Verify log structure
    for log in logs {
        assert!(!log.task_id.is_empty());
        assert!(!log.action.is_empty());
        assert!(log.timestamp > 0);
    }
}

#[tokio::test]
async fn test_parallel_task_processing() {
    let knowledge_base = Arc::new(SharedKnowledge::new());
    let agent = AutonomousAgentV2::new(knowledge_base).await;
    
    // Submit multiple tasks
    let mut task_ids = Vec::new();
    for i in 0..5 {
        let task_id = agent.submit_task(
            TaskType::PatternAnalysis { 
                data_source: format!("source_{}", i) 
            },
            TaskPriority::Medium,
        ).await;
        task_ids.push(task_id);
    }
    
    // Verify all tasks were created
    assert_eq!(task_ids.len(), 5);
    
    // Check that tasks have unique IDs
    let unique_ids: std::collections::HashSet<_> = task_ids.iter().collect();
    assert_eq!(unique_ids.len(), 5);
}

#[tokio::test]
async fn test_human_request_priority() {
    let knowledge_base = Arc::new(SharedKnowledge::new());
    let config = IntegrationConfig {
        auto_respond: true,
        background_learning: false,
        self_improvement: false,
        max_concurrent_tasks: 10,
        human_request_timeout: 5000,
    };
    
    let integration = AutonomousIntegration::new(knowledge_base, Some(config)).await.unwrap();
    
    // Submit background tasks
    for i in 0..3 {
        integration.submit_task(
            TaskType::KnowledgeGathering { 
                topic: format!("topic_{}", i) 
            },
            TaskPriority::Low,
        ).await;
    }
    
    // Submit human request - should be prioritized
    let human_task = integration.submit_task(
        TaskType::HumanRequest {
            query: "Important human query".to_string(),
            session_id: "test_session".to_string(),
        },
        TaskPriority::Critical,
    ).await;
    
    assert!(!human_task.is_empty());
}

#[tokio::test]
async fn test_safe_script_execution() {
    let executor = CommandExecutor::new(None);
    
    // Safe script
    let safe_script = r#"
#!/bin/bash
echo "Hello from script"
date
pwd
"#;
    
    let result = executor.execute_script(safe_script).await;
    assert!(result.is_ok());
    let result = result.unwrap();
    assert!(result.stdout.contains("Hello from script"));
    
    // Dangerous script
    let dangerous_script = r#"
#!/bin/bash
sudo rm -rf /
"#;
    
    let result = executor.execute_script(dangerous_script).await;
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("dangerous pattern"));
}