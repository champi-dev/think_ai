// Enhanced Conversation Memory System for 24+ Hour Contextual Dialogue

use std::collections::HashMap;
use std::sync::RwLock;

pub struct EnhancedConversationMemory {
    sessions: RwLock<HashMap<String, ConversationSession>>,
}

#[derive(Clone, Debug)]
pub struct ConversationSession {
    pub session_id: String,
    pub messages: Vec<Message>,
}

#[derive(Clone, Debug)]
pub struct Message {
    pub role: String,
    pub content: String,
    pub timestamp: u64,
}

impl EnhancedConversationMemory {
    pub fn new() -> Self {
        Self {
            sessions: RwLock::new(HashMap::new()),
        }
    }

    pub fn add_message(&self, session_id: String, role: String, content: String) {
        let message = Message {
            role,
            content,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };

        let mut sessions = self.sessions.write().unwrap();
        sessions
            .entry(session_id.clone())
            .or_insert_with(|| ConversationSession {
                session_id,
                messages: Vec::new(),
            })
            .messages
            .push(message);
    }

    pub fn get_session(&self, session_id: &str) -> Option<ConversationSession> {
        let sessions = self.sessions.read().unwrap();
        sessions.get(session_id).cloned()
    }

    pub fn get_conversation_context(&self, session_id: &str, max_messages: usize) -> Option<Vec<(String, String)>> {
        let sessions = self.sessions.read().unwrap();
        sessions.get(session_id).map(|session| {
            session.messages
                .iter()
                .rev()
                .take(max_messages)
                .map(|msg| (msg.role.clone(), msg.content.clone()))
                .collect::<Vec<_>>()
                .into_iter()
                .rev()
                .collect()
        })
    }

    pub fn clear_old_sessions(&self, max_age_seconds: u64) {
        let current_time = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        let mut sessions = self.sessions.write().unwrap();
        sessions.retain(|_, session| {
            if let Some(last_msg) = session.messages.last() {
                current_time - last_msg.timestamp < max_age_seconds
            } else {
                true
            }
        });
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
        assert_eq!(memory.sessions.read().unwrap().len(), 0);
    }

    #[test]
    fn test_add_and_retrieve_messages() {
        let memory = EnhancedConversationMemory::new();
        let session_id = "test-session".to_string();
        
        memory.add_message(session_id.clone(), "user".to_string(), "Hello".to_string());
        memory.add_message(session_id.clone(), "assistant".to_string(), "Hi there!".to_string());
        
        let session = memory.get_session(&session_id);
        assert!(session.is_some());
        let session = session.unwrap();
        assert_eq!(session.messages.len(), 2);
        assert_eq!(session.messages[0].content, "Hello");
        assert_eq!(session.messages[1].content, "Hi there!");
    }

    #[test]
    fn test_conversation_context() {
        let memory = EnhancedConversationMemory::new();
        let session_id = "test-session".to_string();
        
        memory.add_message(session_id.clone(), "user".to_string(), "Message 1".to_string());
        memory.add_message(session_id.clone(), "assistant".to_string(), "Response 1".to_string());
        memory.add_message(session_id.clone(), "user".to_string(), "Message 2".to_string());
        memory.add_message(session_id.clone(), "assistant".to_string(), "Response 2".to_string());
        
        let context = memory.get_conversation_context(&session_id, 2);
        assert!(context.is_some());
        let context = context.unwrap();
        assert_eq!(context.len(), 2);
        assert_eq!(context[0].1, "Message 2");
        assert_eq!(context[1].1, "Response 2");
    }
}
