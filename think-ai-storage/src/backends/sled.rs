// Sled embedded database backend

use crate::{traits::Storage, Result, StorageError};
use async_trait::async_trait;
use sled::Db;
/// Sled storage for persistence
///
/// What it does: Provides persistent key-value storage
/// How: Uses Sled embedded database with O(log n) operations
/// Why: Fast persistent storage without external database
/// Confidence: 95% - Well-tested database, minimal wrapper
pub struct SledStorage {
    db: Db,
}
impl SledStorage {
    pub fn new(path: &str) -> Result<Self> {
        let db = sled::open(path).map_err(|e| StorageError::StorageError(e.to_string()))?;
        Ok(Self { db })
    }
}
#[async_trait]
impl Storage for SledStorage {
    async fn get(&self, key: &str) -> Result<Option<Vec<u8>>> {
        self.db
            .get(key)
            .map(|opt| opt.map(|v| v.to_vec()))
            .map_err(|e| StorageError::StorageError(e.to_string()))
    }
    async fn set(&self, key: &str, value: Vec<u8>) -> Result<()> {
        self.db
            .insert(key, value)
            .map_err(|e| StorageError::StorageError(e.to_string()))?;
        Ok(())
    }

    async fn delete(&self, key: &str) -> Result<()> {
        self.db
            .remove(key)
            .map_err(|e| StorageError::StorageError(e.to_string()))?;
        Ok(())
    }
    async fn exists(&self, key: &str) -> Result<bool> {
        Ok(self.db
            .contains_key(key)
            .map_err(|e| StorageError::StorageError(e.to_string()))?)
    }
}
