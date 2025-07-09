// Enhanced Conversation Memory System for 24+ Hour Contextual Dialogue

use std::collections::HashMap;

pub struct EnhancedConversationMemory {
    sessions: HashMap<String, ConversationSession>,
}

pub struct ConversationSession {
    pub session_id: String,
    pub messages: Vec<Message>,
}

pub struct Message {
    pub role: String,
    pub content: String,
    pub timestamp: u64,
}

impl EnhancedConversationMemory {
    pub fn new() -> Self {
        Self {
            sessions: HashMap::new(),
        }
    }

    pub fn add_message(&mut self, session_id: String, role: String, content: String) {
        let message = Message {
            role,
            content,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };

        self.sessions
            .entry(session_id.clone())
            .or_insert_with(|| ConversationSession {
                session_id,
                messages: Vec::new(),
            })
            .messages
            .push(message);
    }

    pub fn get_session(&self, session_id: &str) -> Option<&ConversationSession> {
        self.sessions.get(session_id)
    }
}

impl Default for EnhancedConversationMemory {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_memory_creation() {
        let memory = EnhancedConversationMemory::new();
        assert_eq!(memory.sessions.len(), 0);
    }
}