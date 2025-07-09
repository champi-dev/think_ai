use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::{SystemTime, UNIX_EPOCH};
use uuid::Uuid;

use crate::shared_knowledge::{KnowledgeQuery, SharedKnowledge};
use crate::types::{Message, SessionState};
/// Represents an isolated chat session with its own context
#[derive(Debug, Clone)]
pub struct IsolatedSession {
    /// Unique session identifier
    pub session_id: String,
    /// Session-specific context and history
    pub context: SessionContext,
    /// Reference to shared knowledge base (read-only access)
    pub shared_knowledge: Arc<SharedKnowledge>,
    /// Session state for tracking
    pub state: SessionState,
}
/// Context specific to a single chat session
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionContext {
    /// Conversation history for this session
    pub messages: Vec<Message>,
    /// Session-specific context embeddings
    pub context_embeddings: HashMap<String, Vec<f32>>,
    /// Temporary session memory (cleared on session end)
    pub working_memory: HashMap<String, String>,
    /// Session metadata
    pub metadata: SessionMetadata,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionMetadata {
    pub created_at: u64,
    pub last_activity: u64,
    pub user_id: Option<String>,
    pub session_type: String,
    pub tags: Vec<String>,
}

impl IsolatedSession {
    /// Create a new isolated session with fresh context
    pub fn new(shared_knowledge: Arc<SharedKnowledge>) -> Self {
        let session_id = Uuid::new_v4().to_string();
        let now = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        Self {
            session_id: session_id.clone(),
            context: SessionContext {
                messages: Vec::new(),
                context_embeddings: HashMap::new(),
                working_memory: HashMap::new(),
                metadata: SessionMetadata {
                    created_at: now,
                    last_activity: now,
                    user_id: None,
                    session_type: "chat".to_string(),
                    tags: Vec::new(),
                },
            },
            shared_knowledge,
            state: SessionState::Active,
        }
    }
    /// Process a message in this isolated session
    pub async fn process_message(&mut self, message: Message) -> Result<Message, String> {
        // Update last activity
        self.context.metadata.last_activity = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
        // Add message to session history
        self.context.messages.push(message.clone());
        // Generate embeddings for the message (O(1) using hash)
        let embedding = self.generate_message_embedding(&message);
        let embedding_key = format!("msg_{}", self.context.messages.len());
        self.context
            .context_embeddings
            .insert(embedding_key, embedding);
        // Query shared knowledge for relevant information
        let knowledge_results = self.query_shared_knowledge(&message).await?;
        // Generate response using session context + shared knowledge
        let response = self.generate_contextual_response(&message, &knowledge_results)?;
        // Add response to history
        self.context.messages.push(response.clone());
        Ok(response)
    }

    /// Query shared knowledge base without modifying it
    async fn query_shared_knowledge(&self, message: &Message) -> Result<Vec<String>, String> {
        let query = KnowledgeQuery {
            content: message.content.clone(),
            context: Some(self.get_recent_context()),
            max_results: 5,
        };
        self.shared_knowledge.query(query).await
    }

    /// Get recent conversation context for knowledge queries
    fn get_recent_context(&self) -> String {
        let recent_messages: Vec<String> = self
            .context
            .messages
            .iter()
            .rev()
            .take(5)
            .map(|m| format!("{}: {}", m.role, m.content))
            .collect();
        recent_messages.join("\n")
    }

    /// Generate embeddings for a message (O(1) hash-based)
    fn generate_message_embedding(&self, message: &Message) -> Vec<f32> {
        // Simple hash-based embedding for O(1) performance
        let mut hasher = std::collections::hash_map::DefaultHasher::new();
        std::hash::Hash::hash(&message.content, &mut hasher);
        let hash = std::hash::Hasher::finish(&hasher);
        // Convert hash to vector of floats
        let mut embedding = vec![0.0; 128];
        for i in 0..16 {
            let byte = ((hash >> (i * 4)) & 0xFF) as f32;
            embedding[i * 8..(i + 1) * 8]
                .iter_mut()
                .enumerate()
                .for_each(|(j, v)| *v = (byte + j as f32) / 255.0);
        }
        embedding
    }

    /// Generate contextually relevant response
    fn generate_contextual_response(
        &self,
        message: &Message,
        knowledge: &[String],
    ) -> Result<Message, String> {
        // Combine session context with shared knowledge
        let mut context_parts = vec![
            format!("Session ID: {}", self.session_id),
            format!("Message count: {}", self.context.messages.len()),
        ];
        // Add recent conversation context
        if !self.context.messages.is_empty() {
            context_parts.push("Recent conversation:".to_string());
            for msg in self.context.messages.iter().rev().take(3) {
                context_parts.push(format!("- {}: {}", msg.role, msg.content));
            }
        }
        // Add relevant knowledge
        if !knowledge.is_empty() {
            context_parts.push("Relevant knowledge:".to_string());
            for item in knowledge.iter().take(3) {
                context_parts.push(format!("- {item}"));
            }
        }
        // Generate response based on context
        let response_content = format!(
            "Based on the current session context and shared knowledge, here's my response to '{}': \n\n{}",
            message.content,
            self.generate_response_content(&message.content, &context_parts.join("\n"))
        );
        Ok(Message {
            role: "assistant".to_string(),
            content: response_content,
            timestamp: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        })
    }

    /// Generate actual response content
    fn generate_response_content(&self, query: &str, context: &str) -> String {
        // O(1) response generation using hash-based lookup
        let mut hasher = std::collections::hash_map::DefaultHasher::new();
        std::hash::Hash::hash(&(query, context), &mut hasher);
        let hash = std::hash::Hasher::finish(&hasher);
        // Generate deterministic but contextual response
        let response_templates = [
            "I understand your question about {}. Based on our conversation and my knowledge, {}",
            "Regarding {}, I can tell you that {}",
            "That's an interesting point about {}. From what I know, {}",
            "Let me help you with {}. According to my understanding, {}",
        ];
        let template_idx = (hash % response_templates.len() as u64) as usize;
        let template = response_templates[template_idx];
        // Extract key terms from query
        let key_terms: Vec<&str> = query
            .split_whitespace()
            .filter(|w| w.len() > 3)
            .take(2)
            .collect();
        let topic = key_terms.join(" ");
        let details = format!(
            "this relates to the {} aspects we've been discussing. The session context suggests a focus on practical implementation.",
            if hash % 2 == 0 { "technical" } else { "conceptual" }
        );
        template.replace("{}", &topic).replace("{}", &details)
    }

    /// Clear session-specific data while preserving shared knowledge
    pub fn clear_session(&mut self) {
        self.context.messages.clear();
        self.context.context_embeddings.clear();
        self.context.working_memory.clear();
        self.state = SessionState::Closed;
    }

    /// Export session data for persistence
    pub fn export_session(&self) -> SessionExport {
        SessionExport {
            session_id: self.session_id.clone(),
            context: self.context.clone(),
            state: self.state.clone(),
        }
    }

    /// Restore session from export
    pub fn restore_session(
        export: SessionExport,
        shared_knowledge_: Arc<SharedKnowledge>,
    ) -> Self {
        Self {
            session_id: export.session_id,
            context: export.context,
            shared_knowledge: shared_knowledge_,
            state: export.state,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionExport {
    pub session_id: String,
    pub context: SessionContext,
    pub state: SessionState,
}
#[cfg(test)]
mod tests {
    use super::*;
    #[tokio::test]
    async fn test_isolated_session_creation() {
        let shared_knowledge = Arc::new(SharedKnowledge::new());
        let session = IsolatedSession::new(shared_knowledge);
        assert!(!session.session_id.is_empty());
        assert_eq!(session.context.messages.len(), 0);
        assert_eq!(session.state, SessionState::Active);
    }

    #[tokio::test]
    async fn test_message_processing() {
        let shared_knowledge = Arc::new(SharedKnowledge::new());
        let mut session = IsolatedSession::new(shared_knowledge);
        let message = Message {
            role: "user".to_string(),
            content: "Hello, how are you?".to_string(),
            timestamp: SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        };
        let response = session.process_message(message).await.unwrap();
        assert_eq!(response.role, "assistant");
        assert!(!response.content.is_empty());
        assert_eq!(session.context.messages.len(), 2); // User message + response
    }

    #[test]
    fn test_session_isolation() {
        let shared_knowledge = Arc::new(SharedKnowledge::new());
        let session1 = IsolatedSession::new(shared_knowledge.clone());
        let session2 = IsolatedSession::new(shared_knowledge);
        // Sessions should have different IDs
        assert_ne!(session1.session_id, session2.session_id);
        // Sessions should have separate contexts
        assert_eq!(session1.context.messages.len(), 0);
        assert_eq!(session2.context.messages.len(), 0);
    }
}
