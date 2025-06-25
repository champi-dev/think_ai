//! Think AI Cache - O(1) caching layer with functional design

use std::sync::Arc;
use dashmap::DashMap;
use ahash::RandomState;
use async_trait::async_trait;
use serde::{Deserialize, Serialize};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum CacheError {
    #[error("Serialization error: {0}")]
    SerializationError(#[from] serde_json::Error),
    
    #[error("Cache miss")]
    CacheMiss,
}

pub type Result<T> = std::result::Result<T, CacheError>;

/// Trait for O(1) cache operations
#[async_trait]
pub trait O1Cache: Send + Sync {
    /// Get value with O(1) complexity
    async fn get(&self, key: &str) -> Result<Vec<u8>>;
    
    /// Set value with O(1) complexity
    async fn set(&self, key: &str, value: Vec<u8>) -> Result<()>;
    
    /// Check existence with O(1) complexity
    async fn exists(&self, key: &str) -> bool;
    
    /// Remove value with O(1) complexity
    async fn remove(&self, key: &str) -> Result<()>;
}

/// High-performance memory cache with O(1) guarantees
pub struct MemoryCache {
    data: Arc<DashMap<String, Arc<Vec<u8>>, RandomState>>,
    max_size: usize,
}

impl MemoryCache {
    pub fn new(max_size: usize) -> Self {
        let hasher = RandomState::with_seed(42);
        Self {
            data: Arc::new(DashMap::with_capacity_and_hasher(max_size, hasher)),
            max_size,
        }
    }
    
    /// Get cache statistics
    pub fn stats(&self) -> CacheStats {
        CacheStats {
            size: self.data.len(),
            capacity: self.max_size,
        }
    }
}

#[async_trait]
impl O1Cache for MemoryCache {
    async fn get(&self, key: &str) -> Result<Vec<u8>> {
        self.data
            .get(key)
            .map(|entry| entry.value().as_ref().clone())
            .ok_or(CacheError::CacheMiss)
    }
    
    async fn set(&self, key: &str, value: Vec<u8>) -> Result<()> {
        // Simple eviction if at capacity
        if self.data.len() >= self.max_size {
            // Remove first item (not LRU, but O(1))
            if let Some(entry) = self.data.iter().next() {
                self.data.remove(entry.key());
            }
        }
        
        self.data.insert(key.to_string(), Arc::new(value));
        Ok(())
    }
    
    async fn exists(&self, key: &str) -> bool {
        self.data.contains_key(key)
    }
    
    async fn remove(&self, key: &str) -> Result<()> {
        self.data.remove(key);
        Ok(())
    }
}

#[derive(Debug, Serialize)]
pub struct CacheStats {
    pub size: usize,
    pub capacity: usize,
}

/// Type-safe cache wrapper for automatic serialization
pub struct TypedCache<T> {
    inner: Arc<dyn O1Cache>,
    _phantom: std::marker::PhantomData<T>,
}

impl<T: Serialize + for<'de> Deserialize<'de>> TypedCache<T> {
    pub fn new(cache: Arc<dyn O1Cache>) -> Self {
        Self {
            inner: cache,
            _phantom: std::marker::PhantomData,
        }
    }
    
    pub async fn get(&self, key: &str) -> Result<T> {
        let bytes = self.inner.get(key).await?;
        serde_json::from_slice(&bytes).map_err(Into::into)
    }
    
    pub async fn set(&self, key: &str, value: &T) -> Result<()> {
        let bytes = serde_json::to_vec(value)?;
        self.inner.set(key, bytes).await
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_memory_cache() {
        let cache = MemoryCache::new(100);
        
        // Test set and get
        cache.set("key1", b"value1".to_vec()).await.unwrap();
        let value = cache.get("key1").await.unwrap();
        assert_eq!(value, b"value1");
        
        // Test exists
        assert!(cache.exists("key1").await);
        assert!(!cache.exists("key2").await);
        
        // Test remove
        cache.remove("key1").await.unwrap();
        assert!(!cache.exists("key1").await);
    }
    
    #[tokio::test]
    async fn test_typed_cache() {
        let cache = Arc::new(MemoryCache::new(100));
        let typed: TypedCache<serde_json::Value> = TypedCache::new(cache);
        
        let data = serde_json::json!({
            "test": "value",
            "number": 42
        });
        
        typed.set("json_key", &data).await.unwrap();
        let retrieved = typed.get("json_key").await.unwrap();
        assert_eq!(retrieved, data);
    }
}