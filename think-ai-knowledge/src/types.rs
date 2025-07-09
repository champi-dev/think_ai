use serde::{Deserialize, Serialize};

/// Types for isolated sessions and parallel processing
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Message {
    pub role: String,
    pub content: String,
    pub timestamp: u64,
}
pub struct Context {
    pub session_id: String,
    pub user_context: Option<String>,
    pub system_context: Option<String>,
}

#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum SessionState {
    Active,
    Paused,
    Closed,
}

// ProcessType and ProcessState are defined below with all derives

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProcessMessage {
    pub process_type: ProcessType,
    pub state: ProcessState,
    pub message: String,
    pub process_id: String,
    pub message_type: String,
}

pub enum KnowledgeType {
    Fact,
    Pattern,
    Insight,
    Memory,
    Dream,
    Reflection,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ProcessType {
    LLM,
    Knowledge,
    Training,
    Evaluation,
}

impl std::fmt::Display for ProcessType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ProcessType::LLM => write!(f, "LLM"),
            ProcessType::Knowledge => write!(f, "Knowledge"),
            ProcessType::Training => write!(f, "Training"),
            ProcessType::Evaluation => write!(f, "Evaluation"),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ProcessState {
    Running,
    Paused,
    Stopped,
    Error,
}

