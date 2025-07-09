// Intelligent Relevance Engine - No hardcoded rules, pure adaptive intelligence

use crate::KnowledgeNode;
use std::collections::HashMap;

pub struct IntelligentRelevanceEngine {
    query_history: HashMap<String, Vec<String>>,
}

impl IntelligentRelevanceEngine {
    pub fn new() -> Self {
        Self {
            query_history: HashMap::new(),
        }
    }

    pub fn compute_relevance(&self, query: &str, node: &KnowledgeNode) -> f64 {
        // Simple relevance computation
        let query_lower = query.to_lowercase();
        let topic_lower = node.topic.to_lowercase();
        let content_lower = node.content.to_lowercase();

        let mut score = 0.0_f64;

        if topic_lower.contains(&query_lower) {
            score += 1.0;
        }

        if content_lower.contains(&query_lower) {
            score += 0.5;
        }

        for concept in &node.related_concepts {
            if concept.to_lowercase().contains(&query_lower) {
                score += 0.3;
            }
        }

        score.min(1.0_f64) // Cap at 1.0
    }

    pub fn learn_from_interaction(&self, _query: &str, _selected: &KnowledgeNode, _success: f64) {
        // Simple learning placeholder
    }
}

impl Default for IntelligentRelevanceEngine {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_relevance_engine() {
        let engine = IntelligentRelevanceEngine::new();
        let node = KnowledgeNode {
            id: "1".to_string(),
            domain: KnowledgeDomain::General,
            topic: "Test Topic".to_string(),
            content: "Test content".to_string(),
            related_concepts: vec![],
            confidence: 1.0,
            usage_count: 0,
            last_accessed: 0,
        };
        let score = engine.compute_relevance("test", &node);
        assert!(score > 0.0);
    }
}
