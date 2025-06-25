//! Think AI Storage - O(1) storage backend

pub mod traits;
pub mod backends;

use thiserror::Error;

#[derive(Error, Debug)]
pub enum StorageError {
    #[error("Storage error: {0}")]
    StorageError(String),
    
    #[error("Serialization error: {0}")]
    SerializationError(String),
}

pub type Result<T> = std::result::Result<T, StorageError>;

pub use traits::{Storage, TypedStorage};
pub use backends::{MemoryStorage, SledStorage};