use std::collections::HashMap;
use std::sync::Arc;
use std::time::{Duration, Instant};
use tokio::sync::RwLock;

#[derive(Clone)]
struct RateLimitEntry {
    count: u32,
    window_start: Instant,
}

pub struct RateLimiter {
    limits: Arc<RwLock<HashMap<String, RateLimitEntry>>>,
    max_requests: u32,
    window_duration: Duration,
}

impl RateLimiter {
    pub fn new(max_requests: u32, window_seconds: u64) -> Self {
        Self {
            limits: Arc::new(RwLock::new(HashMap::new())),
            max_requests,
            window_duration: Duration::from_secs(window_seconds),
        }
    }

    pub async fn check_rate_limit(&self, client_id: &str) -> Result<(), RateLimitError> {
        let mut limits = self.limits.write().await;
        let now = Instant::now();

        let entry = limits.entry(client_id.to_string()).or_insert(RateLimitEntry {
            count: 0,
            window_start: now,
        });

        // Reset window if expired
        if now.duration_since(entry.window_start) > self.window_duration {
            entry.count = 0;
            entry.window_start = now;
        }

        // Check limit
        if entry.count >= self.max_requests {
            return Err(RateLimitError::TooManyRequests {
                retry_after: self.window_duration.as_secs() - now.duration_since(entry.window_start).as_secs(),
            });
        }

        entry.count += 1;
        Ok(())
    }

    pub async fn cleanup_old_entries(&self) {
        let mut limits = self.limits.write().await;
        let now = Instant::now();
        
        limits.retain(|_, entry| {
            now.duration_since(entry.window_start) <= self.window_duration * 2
        });
    }
}

#[derive(Debug, thiserror::Error)]
pub enum RateLimitError {
    #[error("Too many requests. Retry after {retry_after} seconds")]
    TooManyRequests { retry_after: u64 },
}