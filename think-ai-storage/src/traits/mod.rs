// Storage traits for O(1) operations

use crate::Result;
use async_trait::async_trait;
use serde::{Deserialize, Serialize};
/// Core storage trait with O(1) guarantees
///
/// What it does: Defines interface for all storage backends
/// How: Async trait with simple key-value operations
/// Why: Enables swappable backends while maintaining O(1) performance
/// Confidence: 100% - Interface design, no implementation risk
#[async_trait]
pub trait Storage: Send + Sync {
    /// Get value by key - O(1)
    async fn get(&self, key: &str) -> Result<Option<Vec<u8>>>;
    /// Set value by key - O(1)
    async fn set(&self, key: &str, value: Vec<u8>) -> Result<()>;
    /// Delete value by key - O(1)
    async fn delete(&self, key: &str) -> Result<()>;
    /// Check if key exists - O(1)
    async fn exists(&self, key: &str) -> Result<bool>;
}
/// Typed storage wrapper
pub struct TypedStorage<T> {
    inner: Box<dyn Storage>,
    _phantom: std::marker::PhantomData<T>,
}

impl<T: Serialize + for<'de> Deserialize<'de>> TypedStorage<T> {
    pub fn new(storage: Box<dyn Storage>) -> Self {
        Self {
            inner: storage,
            _phantom: std::marker::PhantomData,
        }
    }
}
