use anyhow::{anyhow, Result};
use dashmap::DashMap;
use parking_lot::RwLock;
use std::collections::VecDeque;
use std::sync::Arc;
use tokio::sync::{Mutex, Semaphore};
use tracing::{debug, info};
use uuid::Uuid;

use crate::ThreadType;

#[derive(Debug, Clone)]
pub struct QuantumThread {
    pub id: Uuid,
    pub thread_type: ThreadType,
    pub is_active: bool,
    pub created_at: std::time::Instant,
}

/// Quantum Thread Pool - Manages isolated threads for parallel generation
pub struct QuantumThreadPool {
    threads: Arc<DashMap<Uuid, Arc<RwLock<QuantumThread>>>>,
    available_threads: Arc<Mutex<VecDeque<Uuid>>>,
    thread_semaphore: Arc<Semaphore>,
    _max_threads: usize,
}

impl QuantumThreadPool {
    pub fn new(max_threads: usize) -> Self {
        let threads = Arc::new(DashMap::new());
        let available_threads = Arc::new(Mutex::new(VecDeque::new()));
        let thread_semaphore = Arc::new(Semaphore::new(max_threads));

        // Pre-create threads for each type
        let thread_types = vec![
            ThreadType::UserChat,
            ThreadType::Thinking,
            ThreadType::Dreaming,
            ThreadType::SelfReflection,
            ThreadType::KnowledgeCreation,
            ThreadType::Training,
        ];

        for (_i, thread_type) in thread_types.iter().cycle().take(max_threads).enumerate() {
            let thread = QuantumThread {
                id: Uuid::new_v4(),
                thread_type: *thread_type,
                is_active: false,
                created_at: std::time::Instant::now(),
            };

            let thread_id = thread.id;
            threads.insert(thread_id, Arc::new(RwLock::new(thread)));

            // Make thread available
            let available_threads_clone = available_threads.clone();
            tokio::spawn(async move {
                available_threads_clone.lock().await.push_back(thread_id);
            });
        }

        info!(
            "Quantum thread pool initialized with {} threads",
            max_threads
        );

        Self {
            threads,
            available_threads,
            thread_semaphore,
            _max_threads: max_threads,
        }
    }

    /// Get an available thread for the specified type
    pub async fn get_thread(&self, preferred_type: ThreadType) -> Result<Uuid> {
        // Acquire semaphore permit
        let _permit = self
            .thread_semaphore
            .acquire()
            .await
            .map_err(|_| anyhow!("Failed to acquire thread permit"))?;

        let mut available = self.available_threads.lock().await;

        // Try to find a thread of the preferred type
        let thread_id = {
            let mut found_id = None;
            let mut fallback_id = None;

            // Look for preferred type
            for (idx, &id) in available.iter().enumerate() {
                if let Some(thread) = self.threads.get(&id) {
                    let thread_guard = thread.read();
                    if thread_guard.thread_type == preferred_type && !thread_guard.is_active {
                        found_id = Some((idx, id));
                        break;
                    } else if fallback_id.is_none() && !thread_guard.is_active {
                        fallback_id = Some((idx, id));
                    }
                }
            }

            // Use preferred or fallback
            if let Some((idx, id)) = found_id.or(fallback_id) {
                available.remove(idx);
                Some(id)
            } else {
                None
            }
        };

        if let Some(id) = thread_id {
            // Mark thread as active
            if let Some(thread) = self.threads.get(&id) {
                thread.write().is_active = true;
            }

            debug!("Thread {} acquired for {:?}", id, preferred_type);
            Ok(id)
        } else {
            Err(anyhow!("No available threads"))
        }
    }

    /// Return a thread to the pool
    pub fn return_thread(&self, thread_id: Uuid) {
        if let Some(thread) = self.threads.get(&thread_id) {
            thread.write().is_active = false;

            // Add back to available queue
            let available_threads = self.available_threads.clone();
            tokio::spawn(async move {
                available_threads.lock().await.push_back(thread_id);
            });

            debug!("Thread {} returned to pool", thread_id);
        }
    }

    /// Get current thread statistics
    pub fn get_stats(&self) -> ThreadPoolStats {
        let total_threads = self.threads.len();
        let mut active_threads = 0;
        let mut threads_by_type = std::collections::HashMap::new();

        for thread in self.threads.iter() {
            let thread_guard = thread.read();
            if thread_guard.is_active {
                active_threads += 1;
            }
            *threads_by_type.entry(thread_guard.thread_type).or_insert(0) += 1;
        }

        ThreadPoolStats {
            total_threads,
            active_threads,
            available_threads: total_threads - active_threads,
            threads_by_type,
        }
    }
}

#[derive(Debug, Clone)]
pub struct ThreadPoolStats {
    pub total_threads: usize,
    pub active_threads: usize,
    pub available_threads: usize,
    pub threads_by_type: std::collections::HashMap<ThreadType, usize>,
}
