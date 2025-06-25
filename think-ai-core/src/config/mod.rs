//! Configuration module for O(1) engine

use serde::{Deserialize, Serialize};

/// Configuration for the O(1) engine
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EngineConfig {
    pub hash_seed: u64,
    pub cache_size: usize,
    pub parallel_workers: usize,
}

impl Default for EngineConfig {
    fn default() -> Self {
        Self {
            hash_seed: 42,
            cache_size: 10_000,
            parallel_workers: num_cpus::get(),
        }
    }
}