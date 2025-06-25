//! O(1) Engine implementation

pub mod state;
pub mod hasher;

use std::sync::Arc;
use crate::{
    cache::O1Cache,
    config::EngineConfig,
    types::{ComputeResult, EngineStats, Result},
};
use self::{state::StateManager, hasher::hash_key};

/// Core O(1) Engine with functional design
pub struct O1Engine {
    pub(crate) config: Arc<EngineConfig>,
    pub(crate) state: StateManager,
    pub(crate) cache: O1Cache,
}

impl O1Engine {
    pub fn new(config: EngineConfig) -> Self {
        let cache = O1Cache::new(config.cache_size, config.hash_seed);
        Self {
            config: Arc::new(config),
            state: StateManager::new(),
            cache,
        }
    }
    
    pub async fn initialize(&self) -> Result<()> {
        tracing::info!("Initializing O(1) engine");
        self.state.set_initialized();
        Ok(())
    }
    
    pub fn compute(&self, key: &str) -> Option<Arc<ComputeResult>> {
        let hash = hash_key(key, self.config.hash_seed);
        self.cache.get(hash)
    }
}

// Include operations implementation
include!("operations.rs");