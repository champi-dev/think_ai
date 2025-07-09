// Feynman Technique Explainer - Creates simplified, logical explanations

use crate::KnowledgeNode;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

pub struct FeynmanExplainer {
    knowledge_nodes: Option<Arc<RwLock<HashMap<String, KnowledgeNode>>>>,
}

impl FeynmanExplainer {
    pub fn new(knowledge_nodes: Option<Arc<RwLock<HashMap<String, KnowledgeNode>>>>) -> Self {
        Self { knowledge_nodes }
    }

    pub fn explain(&self, concept: &str) -> FeynmanExplanation {
        FeynmanExplanation {
            concept: concept.to_string(),
            simple_explanation: format!("Simple explanation of {concept}"),
            deeper_layers: vec![],
            examples: vec![],
            common_misconceptions: vec![],
            confidence_score: 0.8,
        }
    }
}

pub struct FeynmanExplanation {
    pub concept: String,
    pub simple_explanation: String,
    pub deeper_layers: Vec<String>,
    pub examples: Vec<String>,
    pub common_misconceptions: Vec<String>,
    pub confidence_score: f64,
}

impl FeynmanExplanation {
    pub fn format_for_human(&self) -> String {
        format!(
            "Concept: {}\nExplanation: {}\nConfidence: {:.0}%",
            self.concept,
            self.simple_explanation,
            self.confidence_score * 100.0
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_feynman_explainer() {
        let explainer = FeynmanExplainer::new(None);
        let explanation = explainer.explain("test concept");
        assert!(explanation.simple_explanation.contains("test concept"));
    }
}
