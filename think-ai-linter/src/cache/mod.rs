//! O(1) result caching

use dashmap::DashMap;
use std::time::{Duration, Instant};

/// Cache entry with TTL
#[derive(Clone)]
struct CacheEntry<T> {
    value: T,
    expires_at: Instant,
}

/// O(1) cache with TTL support
pub struct ResultCache<K, V> {
    cache: DashMap<K, CacheEntry<V>>,
    ttl: Duration,
}

impl<K: Eq + std::hash::Hash, V: Clone> ResultCache<K, V> {
    pub fn new(ttl: Duration) -> Self {
        Self {
            cache: DashMap::new(),
            ttl,
        }
    }
    
    /// Get value with O(1) lookup
    pub fn get(&self, key: &K) -> Option<V> {
        if let Some(entry) = self.cache.get(key) {
            if entry.expires_at > Instant::now() {
                return Some(entry.value.clone());
            } else {
                // Expired, remove it
                drop(entry);
                self.cache.remove(key);
            }
        }
        None
    }
    
    /// Insert value with O(1) insertion
    pub fn insert(&self, key: K, value: V) {
        let entry = CacheEntry {
            value,
            expires_at: Instant::now() + self.ttl,
        };
        self.cache.insert(key, entry);
    }
}