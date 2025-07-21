// Autonomous Agent Integration Module
//!
//! Integrates the enhanced autonomous agent with ThinkAI's existing systems
//! Provides seamless connection to knowledge bases, models, and services

use async_trait::async_trait;
use std::sync::Arc;
use tokio::sync::RwLock;
use tracing::{info, warn, error};

use crate::autonomous_agent_v2::{
    AutonomousAgentV2, TaskType, TaskPriority, AutonomousTask, TaskStatus
};
use crate::shared_knowledge::SharedKnowledge;
use crate::types::{Message, Context};

/// Integration layer for autonomous agent
pub struct AutonomousIntegration {
    /// The autonomous agent instance
    agent: Arc<AutonomousAgentV2>,
    
    /// Shared knowledge base
    knowledge_base: Arc<SharedKnowledge>,
    
    /// Integration configuration
    config: IntegrationConfig,
}

#[derive(Debug, Clone)]
pub struct IntegrationConfig {
    /// Enable autonomous responses
    pub auto_respond: bool,
    
    /// Enable background learning
    pub background_learning: bool,
    
    /// Enable self-improvement
    pub self_improvement: bool,
    
    /// Maximum concurrent tasks
    pub max_concurrent_tasks: usize,
    
    /// Human request timeout (ms)
    pub human_request_timeout: u64,
}

impl Default for IntegrationConfig {
    fn default() -> Self {
        Self {
            auto_respond: true,
            background_learning: true,
            self_improvement: true,
            max_concurrent_tasks: 10,
            human_request_timeout: 30000,
        }
    }
}

impl AutonomousIntegration {
    /// Create new integration instance
    pub async fn new(
        knowledge_base: Arc<SharedKnowledge>,
        config: Option<IntegrationConfig>,
    ) -> Result<Self, String> {
        let config = config.unwrap_or_default();
        let agent = Arc::new(AutonomousAgentV2::new(knowledge_base.clone()).await);
        
        Ok(Self {
            agent,
            knowledge_base,
            config,
        })
    }
    
    /// Initialize and start the autonomous system
    pub async fn initialize(&self) -> Result<(), String> {
        info!("Initializing autonomous integration");
        
        // Initialize agent models
        self.agent.initialize_models().await?;
        
        // Start the agent
        self.agent.start().await?;
        
        // Schedule initial tasks
        if self.config.background_learning {
            self.schedule_background_learning().await?;
        }
        
        if self.config.self_improvement {
            self.schedule_self_improvement().await?;
        }
        
        info!("Autonomous integration initialized successfully");
        Ok(())
    }
    
    /// Process a user query through the autonomous agent
    pub async fn process_query(
        &self,
        query: &str,
        session_id: &str,
        context: Option<Context>,
    ) -> Result<String, String> {
        info!("Processing query through autonomous agent: {}", query);
        
        // Check if autonomous responses are enabled
        if !self.config.auto_respond {
            return Err("Autonomous responses are disabled".to_string());
        }
        
        // Process through agent
        let response = self.agent.process_human_request(
            query.to_string(),
            session_id.to_string()
        ).await;
        
        // Store interaction in knowledge base
        if let Some(ctx) = context {
            self.store_interaction(query, &response, &ctx).await;
        }
        
        Ok(response)
    }
    
    /// Schedule background learning tasks
    async fn schedule_background_learning(&self) -> Result<(), String> {
        let topics = vec![
            "quantum computing advances",
            "artificial consciousness theories",
            "emergent behaviors in AI",
            "human-AI collaboration",
            "cognitive architectures",
        ];
        
        for topic in topics {
            self.agent.submit_task(
                TaskType::KnowledgeGathering { 
                    topic: topic.to_string() 
                },
                TaskPriority::Medium,
            ).await;
        }
        
        Ok(())
    }
    
    /// Schedule self-improvement tasks
    async fn schedule_self_improvement(&self) -> Result<(), String> {
        let areas = vec![
            "response_quality",
            "processing_speed",
            "knowledge_integration",
            "pattern_recognition",
        ];
        
        for area in areas {
            self.agent.submit_task(
                TaskType::SelfImprovement { 
                    focus_area: area.to_string() 
                },
                TaskPriority::High,
            ).await;
        }
        
        Ok(())
    }
    
    /// Store interaction in knowledge base
    async fn store_interaction(&self, query: &str, response: &str, context: &Context) {
        let message = Message {
            role: "user".to_string(),
            content: query.to_string(),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };
        
        // Store in knowledge base for future learning
        self.knowledge_base.add_knowledge(
            crate::shared_knowledge::KnowledgeItem::new(
                format!("Q: {} A: {}", query, response),
                vec![
                    "interaction".to_string(),
                    context.session_id.clone(),
                ],
                0.9,
                Some(message),
            )
        ).await;
    }
    
    /// Get agent status and metrics
    pub async fn get_status(&self) -> AgentStatus {
        let active_tasks = self.agent.get_active_tasks().await;
        let metrics = self.agent.get_improvement_metrics();
        
        AgentStatus {
            consciousness_level: self.agent.consciousness_level(),
            active_tasks: active_tasks.len(),
            completed_tasks: active_tasks.iter()
                .filter(|t| t.status == TaskStatus::Completed)
                .count(),
            failed_tasks: active_tasks.iter()
                .filter(|t| t.status == TaskStatus::Failed)
                .count(),
            improvement_metrics: metrics,
        }
    }
    
    /// Submit a custom task
    pub async fn submit_task(
        &self,
        task_type: TaskType,
        priority: TaskPriority,
    ) -> String {
        self.agent.submit_task(task_type, priority).await
    }
    
    /// Get task status by ID
    pub async fn get_task_status(&self, task_id: &str) -> Option<AutonomousTask> {
        self.agent.get_task_status(task_id).await
    }
    
    /// Shutdown the autonomous system
    pub async fn shutdown(&self) -> Result<(), String> {
        info!("Shutting down autonomous integration");
        self.agent.stop().await
    }
}

/// Agent status information
#[derive(Debug, Clone)]
pub struct AgentStatus {
    pub consciousness_level: f64,
    pub active_tasks: usize,
    pub completed_tasks: usize,
    pub failed_tasks: usize,
    pub improvement_metrics: std::collections::HashMap<String, f64>,
}

/// Trait for components that can integrate with the autonomous agent
#[async_trait]
pub trait AutonomousComponent: Send + Sync {
    /// Initialize the component with the agent
    async fn initialize(&mut self, agent: Arc<AutonomousAgentV2>) -> Result<(), String>;
    
    /// Process a request through this component
    async fn process(&self, request: &str) -> Result<String, String>;
    
    /// Get component name
    fn name(&self) -> &str;
}

/// Example usage and integration tests
#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_integration_creation() {
        let knowledge_base = Arc::new(SharedKnowledge::new());
        let integration = AutonomousIntegration::new(knowledge_base, None).await;
        
        assert!(integration.is_ok());
    }
    
    #[tokio::test]
    async fn test_query_processing() {
        let knowledge_base = Arc::new(SharedKnowledge::new());
        let integration = AutonomousIntegration::new(knowledge_base, None).await.unwrap();
        
        // Initialize without starting background tasks
        let mut config = IntegrationConfig::default();
        config.background_learning = false;
        config.self_improvement = false;
        
        let knowledge_base = Arc::new(SharedKnowledge::new());
        let integration = AutonomousIntegration::new(knowledge_base, Some(config)).await.unwrap();
        
        // Test query processing
        let result = integration.process_query(
            "What is consciousness?",
            "test_session",
            None,
        ).await;
        
        // Should fail because agent isn't initialized
        assert!(result.is_err());
    }
}