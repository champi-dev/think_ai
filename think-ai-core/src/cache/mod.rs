//! O(1) cache implementation

use std::sync::Arc;
use dashmap::DashMap;
use ahash::RandomState;
use crate::types::ComputeResult;

pub struct O1Cache {
    data: Arc<DashMap<u64, Arc<ComputeResult>, RandomState>>,
}

impl O1Cache {
    pub fn new(capacity: usize, seed: u64) -> Self {
        let hasher = RandomState::with_seed(seed as usize);
        Self {
            data: Arc::new(DashMap::with_capacity_and_hasher(
                capacity,
                hasher
            )),
        }
    }
    
    pub fn get(&self, key: u64) -> Option<Arc<ComputeResult>> {
        self.data.get(&key).map(|entry| entry.clone())
    }
    
    pub fn insert(&self, key: u64, value: ComputeResult) {
        self.data.insert(key, Arc::new(value));
    }
    
    pub fn len(&self) -> usize {
        self.data.len()
    }
}