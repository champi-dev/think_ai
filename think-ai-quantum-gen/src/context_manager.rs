use dashmap::DashMap;
use parking_lot::RwLock;
use serde::{Deserialize, Serialize};
use std::collections::VecDeque;
use std::sync::Arc;
use tracing::{debug, info};
use uuid::Uuid;

use crate::ThreadType;

const MAX_CONTEXT_HISTORY: usize = 50;
const CONTEXT_EXPIRY_MINUTES: u64 = 30;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ContextEntry {
    pub query: String,
    pub response: String,
    pub timestamp: std::time::SystemTime,
}

#[derive(Debug)]
pub struct IsolatedContext {
    pub id: Uuid,
    pub thread_type: ThreadType,
    pub history: RwLock<VecDeque<ContextEntry>>,
    pub created_at: std::time::Instant,
    pub last_accessed: RwLock<std::time::Instant>,
}

/// Context Manager - Manages isolated contexts for each thread
pub struct ContextManager {
    contexts: Arc<DashMap<Uuid, Arc<IsolatedContext>>>,
    context_index: Arc<DashMap<ThreadType, Vec<Uuid>>>,
}

impl ContextManager {
    pub fn new() -> Self {
        let manager = Self {
            contexts: Arc::new(DashMap::new()),
            context_index: Arc::new(DashMap::new()),
        };

        // Start cleanup task
        let contexts_clone = manager.contexts.clone();
        tokio::spawn(async move {
            loop {
                tokio::time::sleep(tokio::time::Duration::from_secs(300)).await;
                Self::cleanup_expired_contexts(&contexts_clone);
            }
        });

        info!("Context manager initialized");
        manager
    }

    /// Create a new isolated context
    pub fn create_context(&self, thread_type: ThreadType) -> Uuid {
        let context_id = Uuid::new_v4();
        let context = Arc::new(IsolatedContext {
            id: context_id,
            thread_type,
            history: RwLock::new(VecDeque::new()),
            created_at: std::time::Instant::now(),
            last_accessed: RwLock::new(std::time::Instant::now()),
        });

        self.contexts.insert(context_id, context.clone());

        // Update index
        self.context_index
            .entry(thread_type)
            .or_insert_with(Vec::new)
            .push(context_id);

        debug!(
            "Created context {} for thread type {:?}",
            context_id, thread_type
        );
        context_id
    }

    /// Update context with new interaction
    pub fn update_context(&self, context_id: Uuid, query: &str, response: &str) {
        if let Some(context) = self.contexts.get(&context_id) {
            let entry = ContextEntry {
                query: query.to_string(),
                response: response.to_string(),
                timestamp: std::time::SystemTime::now(),
            };

            let mut history = context.history.write();
            history.push_back(entry);

            // Maintain history size limit
            while history.len() > MAX_CONTEXT_HISTORY {
                history.pop_front();
            }

            // Update last accessed
            *context.last_accessed.write() = std::time::Instant::now();

            debug!("Updated context {} with new entry", context_id);
        }
    }

    /// Get formatted context for a given context ID
    pub fn get_context(&self, context_id: Uuid) -> Option<String> {
        self.contexts.get(&context_id).map(|context| {
            let history = context.history.read();
            let mut context_parts = Vec::new();

            // Get last 10 interactions for context
            let start_idx = history.len().saturating_sub(10);
            for entry in history.iter().skip(start_idx) {
                context_parts.push(format!(
                    "User: {}\nAssistant: {}",
                    entry.query, entry.response
                ));
            }

            // Update last accessed
            *context.last_accessed.write() = std::time::Instant::now();

            context_parts.join("\n\n")
        })
    }

    /// Get all contexts for a thread type
    pub fn get_contexts_by_type(&self, thread_type: ThreadType) -> Vec<Uuid> {
        self.context_index
            .get(&thread_type)
            .map(|contexts| contexts.clone())
            .unwrap_or_default()
    }

    /// Merge insights from multiple contexts (for shared intelligence)
    pub fn merge_contexts(&self, context_ids: &[Uuid]) -> String {
        let mut all_entries = Vec::new();

        for context_id in context_ids {
            if let Some(context) = self.contexts.get(context_id) {
                let history = context.history.read();
                for entry in history.iter() {
                    all_entries.push((entry.timestamp, entry.clone()));
                }
            }
        }

        // Sort by timestamp
        all_entries.sort_by_key(|(timestamp, _)| *timestamp);

        // Take last 20 entries
        let start_idx = all_entries.len().saturating_sub(20);
        all_entries[start_idx..]
            .iter()
            .map(|(_, entry)| format!("Q: {}\nA: {}", entry.query, entry.response))
            .collect::<Vec<_>>()
            .join("\n\n")
    }

    /// Clean up expired contexts
    fn cleanup_expired_contexts(contexts: &DashMap<Uuid, Arc<IsolatedContext>>) {
        let now = std::time::Instant::now();
        let expiry_duration = std::time::Duration::from_secs(CONTEXT_EXPIRY_MINUTES * 60);

        let expired: Vec<Uuid> = contexts
            .iter()
            .filter(|entry| {
                let last_accessed = *entry.value().last_accessed.read();
                now.duration_since(last_accessed) > expiry_duration
            })
            .map(|entry| *entry.key())
            .collect();

        for id in expired {
            contexts.remove(&id);
            debug!("Removed expired context {}", id);
        }
    }

    /// Get context statistics
    pub fn get_stats(&self) -> ContextStats {
        let total_contexts = self.contexts.len();
        let mut contexts_by_type = std::collections::HashMap::new();
        let mut total_entries = 0;

        for context in self.contexts.iter() {
            let history_len = context.history.read().len();
            total_entries += history_len;
            *contexts_by_type.entry(context.thread_type).or_insert(0) += 1;
        }

        ContextStats {
            total_contexts,
            total_entries,
            contexts_by_type,
            average_entries_per_context: if total_contexts > 0 {
                total_entries as f64 / total_contexts as f64
            } else {
                0.0
            },
        }
    }
}

#[derive(Debug, Clone)]
pub struct ContextStats {
    pub total_contexts: usize,
    pub total_entries: usize,
    pub contexts_by_type: std::collections::HashMap<ThreadType, usize>,
    pub average_entries_per_context: f64,
}
