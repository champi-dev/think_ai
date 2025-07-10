// Think AI Core - O(1) Performance Engine
//!
// This module implements the core engine with guaranteed O(1) performance
// using functional programming principles and immutable data structures.

pub mod config;
pub mod types;
// pub mod cache; // Module removed - using think-ai-cache crate instead
pub mod consciousness_engine;
pub mod engine;
pub mod knowledge_modules;
pub mod knowledge_transfer;
pub mod lsh_engine;
pub mod qa_training;
pub mod quantum_core;
pub mod qwen_cache;
pub mod thinking_patterns;

pub use config::EngineConfig;
pub use consciousness_engine::{ConsciousnessMetrics, O1ConsciousnessEngine};
pub use engine::O1Engine;
pub use knowledge_transfer::KnowledgeTransferEngine;
pub use lsh_engine::{LSHConfig, O1VectorEngine, VectorSearchMetrics};
pub use quantum_core::QuantumInference;
pub use types::{ComputeResult, CoreError, EngineStats, Result};

#[cfg(test)]
mod tests;
