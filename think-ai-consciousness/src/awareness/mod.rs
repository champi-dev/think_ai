// Awareness and attention mechanisms

use crate::types::{ConsciousnessState, Thought};
use im::Vector;

/// Process a new thought through awareness
///
/// What it does: Integrates new thought into consciousness
/// How: Functionally transforms state with new thought
/// Why: Maintains coherent stream of consciousness
/// Confidence: 90% - Pure functional transformation
pub fn process_thought(state: ConsciousnessState, thought: Thought) -> ConsciousnessState {
    let mut new_state = state;

    // Add thought to stream
    new_state.thoughts.push_back(thought.clone());

    // Update focus if high confidence
    if thought.confidence > 0.8 {
        new_state.focus = Some(thought.id);
    }

    // Adjust awareness based on thought complexity
    let complexity = thought.content.len() as f32 / 100.0;
    new_state.awareness_level = (new_state.awareness_level + complexity).min(1.0);

    new_state
}

/// Filter thoughts by relevance
pub fn filter_relevant_thoughts(thoughts: &Vector<Thought>, query: &str) -> Vector<Thought> {
    thoughts
        .iter()
        .filter(|t| t.content.contains(query))
        .cloned()
        .collect()
}
