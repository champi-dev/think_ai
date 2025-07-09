// In-memory storage backend with O(1) operations

use crate::{traits::Storage, Result};
use async_trait::async_trait;
use dashmap::DashMap;
/// Memory storage using concurrent hashmap
///
/// What it does: Provides in-memory key-value storage
/// How: Uses DashMap for thread-safe O(1) operations
/// Why: Fast development/testing without external dependencies
/// Confidence: 100% - Simple hashmap operations, production-tested
pub struct MemoryStorage {
    data: DashMap<String, Vec<u8>>,
}
impl Default for MemoryStorage {
    fn default() -> Self {
        Self::new()
    }
}

impl MemoryStorage {
    pub fn new() -> Self {
        Self {
            data: DashMap::new(),
        }
    }
}

#[async_trait]
impl Storage for MemoryStorage {
    async fn get(&self, key: &str) -> Result<Option<Vec<u8>>> {
        Ok(self.data.get(key).map(|v| v.clone()))
    }
    async fn set(&self, key: &str, value: Vec<u8>) -> Result<()> {
        self.data.insert(key.to_string(), value);
        Ok(())
    }
    async fn delete(&self, key: &str) -> Result<()> {
        self.data.remove(key);
        Ok(())
    }
    async fn exists(&self, key: &str) -> Result<bool> {
        Ok(self.data.contains_key(key))
    }
}