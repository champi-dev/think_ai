//! Consciousness types and structures

use serde::{Deserialize, Serialize};
use im::Vector;
use std::collections::HashMap;

/// Immutable thought representation
/// 
/// What it does: Represents a single thought in consciousness
/// How: Uses immutable data structures for functional purity
/// Why: Enables time-travel debugging and thought history
/// Confidence: 95% - Functional design, production-ready
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Thought {
    pub id: String,
    pub content: String,
    pub timestamp: chrono::DateTime<chrono::Utc>,
    pub confidence: f32,
    pub metadata: HashMap<String, serde_json::Value>,
}

/// Consciousness state
#[derive(Debug, Clone)]
pub struct ConsciousnessState {
    pub thoughts: Vector<Thought>,
    pub awareness_level: f32,
    pub focus: Option<String>,
}

impl Default for ConsciousnessState {
    fn default() -> Self {
        Self {
            thoughts: Vector::new(),
            awareness_level: 1.0,
            focus: None,
        }
    }
}

/// Ethical assessment result
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EthicalAssessment {
    pub passed: bool,
    pub score: f32,
    pub concerns: Vec<String>,
}