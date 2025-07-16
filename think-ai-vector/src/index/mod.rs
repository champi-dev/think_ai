// Vector index implementation

pub mod distance;
pub mod hash_tables;
pub mod storage;

use crate::{
    lsh,
    types::{LSHConfig, Result, VectorError},
};
use std::sync::Arc;

/// O(1) Vector Search Index using LSH
pub struct O1VectorIndex {
    pub(crate) config: Arc<LSHConfig>,
    pub(crate) hash_tables: hash_tables::HashTables,
    pub(crate) projections: Arc<Vec<ndarray::Array1<f32>>>,
    pub(crate) storage: storage::VectorStorage,
}

impl O1VectorIndex {
    pub fn new(config: LSHConfig) -> Result<Self> {
        if config.dimension == 0 {
            return Err(VectorError::InvalidConfig("Dimension must be > 0".into()));
        }

        let hash_tables = hash_tables::HashTables::new(config.num_hash_tables, config.seed);

        let projections = lsh::generate_projections(&config);

        Ok(Self {
            config: Arc::new(config),
            hash_tables,
            projections: Arc::new(projections),
            storage: storage::VectorStorage::new(),
        })
    }
}

// Include operations
include!("operations.rs");
include!("search.rs");
