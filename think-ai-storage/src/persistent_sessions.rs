use crate::{backends::sled::SledStorage, traits::Storage};
use async_trait::async_trait;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConversationMessage {
    pub role: String,
    pub content: String,
    pub timestamp: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConversationSession {
    pub id: String,
    pub messages: Vec<ConversationMessage>,
    pub created_at: u64,
    pub last_updated: u64,
    pub user_id: Option<String>,  // For future user identification
}

/// Persistent conversation memory using Sled database
pub struct PersistentConversationMemory {
    storage: Arc<SledStorage>,
    cache: Arc<RwLock<HashMap<String, ConversationSession>>>,
}

impl PersistentConversationMemory {
    pub async fn new(db_path: &str) -> Result<Self, Box<dyn std::error::Error + Send + Sync>> {
        let storage = Arc::new(SledStorage::new(db_path)?);
        let cache = Arc::new(RwLock::new(HashMap::new()));
        
        // Load all sessions into cache on startup
        // Note: In production, you might want to lazy-load instead
        let memory = Self { storage, cache };
        memory.load_all_sessions().await?;
        
        Ok(memory)
    }
    
    async fn load_all_sessions(&self) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        // This is a simplified version - in production, use proper iteration
        // For now, we'll just load sessions as they're accessed
        Ok(())
    }
    
    pub async fn add_message(
        &self,
        session_id: String,
        role: String,
        content: String,
    ) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        let timestamp = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs();
        
        let message = ConversationMessage {
            role,
            content,
            timestamp,
        };
        
        // Try to load from storage first if not in cache
        let mut cache = self.cache.write().await;
        if !cache.contains_key(&session_id) {
            if let Some(stored_session) = self.load_session(&session_id).await? {
                cache.insert(session_id.clone(), stored_session);
            }
        }
        
        let session = cache.entry(session_id.clone()).or_insert_with(|| {
            ConversationSession {
                id: session_id.clone(),
                messages: Vec::new(),
                created_at: timestamp,
                last_updated: timestamp,
                user_id: None,
            }
        });
        
        session.messages.push(message);
        session.last_updated = timestamp;
        
        // Persist to storage
        let session_data = serde_json::to_vec(&session)?;
        self.storage.set(&format!("session:{}", session_id), session_data).await?;
        
        Ok(())
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
                    session.messages
                        .iter()
                        .rev()
                        .take(max_messages)
                        .map(|msg| (msg.role.clone(), msg.content.clone()))
                        .collect::<Vec<_>>()
                        .into_iter()
                        .rev()
                        .collect()
                );
            }
        }
        
        // Try loading from storage
        if let Ok(Some(session)) = self.load_session(session_id).await {
            let mut cache = self.cache.write().await;
            let context = session.messages
                .iter()
                .rev()
                .take(max_messages)
                .map(|msg| (msg.role.clone(), msg.content.clone()))
                .collect::<Vec<_>>()
                .into_iter()
                .rev()
                .collect();
            cache.insert(session_id.to_string(), session);
            Some(context)
        } else {
            None
        }
    }
    
    async fn load_session(&self, session_id: &str) -> Result<Option<ConversationSession>, Box<dyn std::error::Error + Send + Sync>> {
        let key = format!("session:{}", session_id);
        if let Some(data) = self.storage.get(&key).await? {
            let session: ConversationSession = serde_json::from_slice(&data)?;
            Ok(Some(session))
        } else {
            Ok(None)
        }
    }
    
    pub async fn delete_session(&self, session_id: &str) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        // Remove from cache
        self.cache.write().await.remove(session_id);
        
        // Remove from storage
        let key = format!("session:{}", session_id);
        self.storage.delete(&key).await?;
        
        Ok(())
    }
    
    pub async fn check_delete_command(&self, session_id: &str, message: &str) -> bool {
        let lower_msg = message.to_lowercase();
        lower_msg.contains("delete") && 
        (lower_msg.contains("chat history") || 
         lower_msg.contains("conversation history") || 
         lower_msg.contains("my history") ||
         lower_msg.contains("all history"))
    }
}