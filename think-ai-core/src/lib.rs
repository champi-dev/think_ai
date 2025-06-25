//! Think AI Core - O(1) Performance Engine
//! 
//! This module implements the core engine with guaranteed O(1) performance
//! using functional programming principles and immutable data structures.

pub mod types;
pub mod config;
pub mod cache;
pub mod engine;

pub use types::{CoreError, ComputeResult, EngineStats, Result};
pub use config::EngineConfig;
pub use engine::O1Engine;

#[cfg(test)]
mod tests;