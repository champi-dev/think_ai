use crate::enhanced_conversation_memory::Message;
use serde::{Deserialize, Serialize};
use sled::Db;
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Clone, Debug, Serialize, Deserialize)]
pub struct PersistentSession {
    pub session_id: String,
    pub messages: Vec<Message>,
    pub created_at: u64,
    pub last_updated: u64,
}

/// Persistent version of EnhancedConversationMemory using Sled database
pub struct PersistentConversationMemory {
    db: Db,
    cache: Arc<RwLock<HashMap<String, PersistentSession>>>,
}

impl PersistentConversationMemory {
    pub fn new(db_path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let db = sled::open(db_path)?;
        let cache = Arc::new(RwLock::new(HashMap::new()));
        Ok(Self { db, cache })
    }

    pub async fn add_message(&self, session_id: String, role: String, content: String) {
        let timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs();

        let message = Message {
            role,
            content,
            timestamp,
        };

        // Try to load from DB first if not in cache
        let mut cache = self.cache.write().await;
        if !cache.contains_key(&session_id) {
            if let Ok(Some(data)) = self.db.get(format!("session:{}", session_id)) {
                if let Ok(session) = serde_json::from_slice::<PersistentSession>(&data) {
                    cache.insert(session_id.clone(), session);
                }
            }
        }

        let session = cache
            .entry(session_id.clone())
            .or_insert_with(|| PersistentSession {
                session_id: session_id.clone(),
                messages: Vec::new(),
                created_at: timestamp,
                last_updated: timestamp,
            });

        session.messages.push(message);
        session.last_updated = timestamp;

        // Persist to DB
        if let Ok(data) = serde_json::to_vec(&session) {
            let _ = self.db.insert(format!("session:{}", session_id), data);
        }
    }

    pub async fn get_conversation_context(
        &self,
        session_id: &str,
        max_messages: usize,
    ) -> Option<Vec<(String, String)>> {
        // Check cache first
        {
            let cache = self.cache.read().await;
            if let Some(session) = cache.get(session_id) {
                return Some(
                    session
                        .messages
                        .iter()
                        .rev()
                        .take(max_messages)
                        .map(|msg| (msg.role.clone(), msg.content.clone()))
                        .collect::<Vec<_>>()
                        .into_iter()
                        .rev()
                        .collect(),
                );
            }
        }

        // Try loading from DB
        if let Ok(Some(data)) = self.db.get(format!("session:{}", session_id)) {
            if let Ok(session) = serde_json::from_slice::<PersistentSession>(&data) {
                let mut cache = self.cache.write().await;
                let context = session
                    .messages
                    .iter()
                    .rev()
                    .take(max_messages)
                    .map(|msg| (msg.role.clone(), msg.content.clone()))
                    .collect::<Vec<_>>()
                    .into_iter()
                    .rev()
                    .collect();
                cache.insert(session_id.to_string(), session);
                return Some(context);
            }
        }

        None
    }

    pub async fn delete_session(&self, session_id: &str) {
        self.cache.write().await.remove(session_id);
        let _ = self.db.remove(format!("session:{}", session_id));
        let _ = self.db.flush();
    }

    pub fn check_delete_command(&self, message: &str) -> bool {
        let lower_msg = message.to_lowercase();
        lower_msg.contains("delete")
            && (lower_msg.contains("chat history")
                || lower_msg.contains("conversation history")
                || lower_msg.contains("my history")
                || lower_msg.contains("all history"))
    }
}

// Make Message serializable
impl Serialize for Message {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::Serializer,
    {
        use serde::ser::SerializeStruct;
        let mut state = serializer.serialize_struct("Message", 3)?;
        state.serialize_field("role", &self.role)?;
        state.serialize_field("content", &self.content)?;
        state.serialize_field("timestamp", &self.timestamp)?;
        state.end()
    }
}

impl<'de> Deserialize<'de> for Message {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: serde::Deserializer<'de>,
    {
        #[derive(Deserialize)]
        struct MessageHelper {
            role: String,
            content: String,
            timestamp: u64,
        }

        let helper = MessageHelper::deserialize(deserializer)?;
        Ok(Message {
            role: helper.role,
            content: helper.content,
            timestamp: helper.timestamp,
        })
    }
}
