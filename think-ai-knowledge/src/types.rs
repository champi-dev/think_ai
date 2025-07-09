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

pub enum ProcessType {
    Thinking,
    Dreaming,
    Learning,
    Reflecting,
}

impl std::fmt::Display for ProcessType {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ProcessType::Thinking => write!(f, "thinking"),
            ProcessType::Dreaming => write!(f, "dreaming"),
            ProcessType::Learning => write!(f, "learning"),
            ProcessType::Reflecting => write!(f, "reflecting"),
        }
    }
}

pub enum ProcessState {
    Running,
    Stopped,
    Failed,
}

pub struct ProcessMessage {
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