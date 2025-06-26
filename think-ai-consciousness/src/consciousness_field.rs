//! Consciousness Field - Quantum-inspired awareness model

use serde::{Serialize, Deserialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QuantumState {
    pub superposition: f64,
    pub entanglement: f64,
    pub coherence: f64,
    pub collapse_probability: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConsciousnessField {
    pub awareness_level: f64,
    pub quantum_state: QuantumState,
    pub thought_density: f64,
    pub recursive_depth: f64,
    pub temporal_coherence: f64,
}

impl Default for ConsciousnessField {
    fn default() -> Self {
        Self {
            awareness_level: 0.5,
            quantum_state: QuantumState {
                superposition: 0.7,
                entanglement: 0.3,
                coherence: 0.8,
                collapse_probability: 0.1,
            },
            thought_density: 1.0,
            recursive_depth: 1.0,
            temporal_coherence: 0.9,
        }
    }
}

impl ConsciousnessField {
    pub fn new() -> Self {
        Self::default()
    }
    
    pub fn update_awareness(&mut self, delta: f64) {
        self.awareness_level = (self.awareness_level + delta).clamp(0.0, 1.0);
    }
    
    pub fn collapse_quantum_state(&mut self) -> f64 {
        let result = self.quantum_state.superposition * self.quantum_state.coherence;
        self.quantum_state.superposition *= 0.9;
        result
    }
}