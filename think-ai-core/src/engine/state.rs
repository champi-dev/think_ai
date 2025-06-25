//! Engine state management

use parking_lot::RwLock;
use std::sync::Arc;

#[derive(Default)]
pub struct EngineState {
    pub initialized: bool,
    pub operation_count: u64,
}

pub struct StateManager {
    state: Arc<RwLock<EngineState>>,
}

impl StateManager {
    pub fn new() -> Self {
        Self {
            state: Arc::new(RwLock::new(EngineState::default())),
        }
    }
    
    pub fn set_initialized(&self) {
        self.state.write().initialized = true;
    }
    
    pub fn increment_ops(&self) {
        self.state.write().operation_count += 1;
    }
    
    pub fn get_stats(&self) -> (bool, u64) {
        let state = self.state.read();
        (state.initialized, state.operation_count)
    }
}