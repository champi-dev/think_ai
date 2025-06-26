pub mod evidence;
pub mod persistence;
pub mod responder;
pub mod trainer;

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeNode {
    pub id: String,
    pub domain: KnowledgeDomain,
    pub topic: String,
    pub content: String,
    pub related_concepts: Vec<String>,
    pub confidence: f64,
    pub usage_count: u64,
    pub last_accessed: u64,
}

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
pub enum KnowledgeDomain {
    Mathematics,
    Physics,
    Chemistry,
    Biology,
    ComputerScience,
    Engineering,
    Medicine,
    Psychology,
    Sociology,
    Economics,
    Philosophy,
    Ethics,
    Art,
    Music,
    Literature,
    History,
    Geography,
    Linguistics,
    Logic,
    Astronomy,
}

impl KnowledgeDomain {
    pub fn all_domains() -> Vec<Self> {
        vec![
            Self::Mathematics,
            Self::Physics,
            Self::Chemistry,
            Self::Biology,
            Self::ComputerScience,
            Self::Engineering,
            Self::Medicine,
            Self::Psychology,
            Self::Sociology,
            Self::Economics,
            Self::Philosophy,
            Self::Ethics,
            Self::Art,
            Self::Music,
            Self::Literature,
            Self::History,
            Self::Geography,
            Self::Linguistics,
            Self::Logic,
            Self::Astronomy,
        ]
    }
}

pub struct KnowledgeEngine {
    nodes: Arc<RwLock<HashMap<String, KnowledgeNode>>>,
    domain_index: Arc<RwLock<HashMap<KnowledgeDomain, Vec<String>>>>,
    concept_graph: Arc<RwLock<HashMap<String, Vec<String>>>>,
    training_iterations: Arc<RwLock<u64>>,
    total_knowledge_items: Arc<RwLock<u64>>,
}

impl KnowledgeEngine {
    pub fn new() -> Self {
        Self {
            nodes: Arc::new(RwLock::new(HashMap::new())),
            domain_index: Arc::new(RwLock::new(HashMap::new())),
            concept_graph: Arc::new(RwLock::new(HashMap::new())),
            training_iterations: Arc::new(RwLock::new(0)),
            total_knowledge_items: Arc::new(RwLock::new(0)),
        }
    }

    pub fn add_knowledge(
        &self,
        domain: KnowledgeDomain,
        topic: String,
        content: String,
        related: Vec<String>,
    ) -> String {
        let id = Self::generate_id(&domain, &topic, &content);

        let node = KnowledgeNode {
            id: id.clone(),
            domain: domain.clone(),
            topic: topic.clone(),
            content,
            related_concepts: related.clone(),
            confidence: 1.0,
            usage_count: 0,
            last_accessed: Self::current_timestamp(),
        };

        let mut nodes = self.nodes.write().unwrap();
        nodes.insert(id.clone(), node);

        let mut domain_index = self.domain_index.write().unwrap();
        domain_index
            .entry(domain)
            .or_insert_with(Vec::new)
            .push(id.clone());

        let mut concept_graph = self.concept_graph.write().unwrap();
        concept_graph.insert(topic.clone(), related);

        let mut total = self.total_knowledge_items.write().unwrap();
        *total += 1;

        id
    }

    pub fn query(&self, query: &str) -> Option<Vec<KnowledgeNode>> {
        let query_hash = Self::hash_string(query);
        let nodes = self.nodes.read().unwrap();

        let mut results = Vec::new();
        for (_, node) in nodes.iter() {
            if Self::hash_string(&node.topic) == query_hash
                || Self::hash_string(&node.content).contains(&query_hash[..8])
            {
                results.push(node.clone());
            }
        }

        if results.is_empty() {
            None
        } else {
            Some(results)
        }
    }

    pub fn query_by_domain(&self, domain: KnowledgeDomain) -> Vec<KnowledgeNode> {
        let domain_index = self.domain_index.read().unwrap();
        let nodes = self.nodes.read().unwrap();

        if let Some(ids) = domain_index.get(&domain) {
            ids.iter().filter_map(|id| nodes.get(id).cloned()).collect()
        } else {
            Vec::new()
        }
    }

    pub fn train_iteration(
        &self,
        knowledge_pairs: Vec<(KnowledgeDomain, String, String, Vec<String>)>,
    ) {
        for (domain, topic, content, related) in knowledge_pairs {
            self.add_knowledge(domain, topic, content, related);
        }

        let mut iterations = self.training_iterations.write().unwrap();
        *iterations += 1;
    }

    pub fn get_stats(&self) -> KnowledgeStats {
        let nodes = self.nodes.read().unwrap();
        let iterations = self.training_iterations.read().unwrap();
        let total = self.total_knowledge_items.read().unwrap();

        let mut domain_counts = HashMap::new();
        for node in nodes.values() {
            *domain_counts.entry(node.domain.clone()).or_insert(0) += 1;
        }

        KnowledgeStats {
            total_nodes: nodes.len(),
            training_iterations: *iterations,
            total_knowledge_items: *total,
            domain_distribution: domain_counts,
            average_confidence: if nodes.is_empty() {
                0.0
            } else {
                nodes.values().map(|n| n.confidence).sum::<f64>() / nodes.len() as f64
            },
        }
    }

    pub fn get_all_nodes(&self) -> HashMap<String, KnowledgeNode> {
        self.nodes.read().unwrap().clone()
    }

    pub fn load_nodes(&self, nodes: HashMap<String, KnowledgeNode>) {
        let mut self_nodes = self.nodes.write().unwrap();
        let mut domain_index = self.domain_index.write().unwrap();
        let mut concept_graph = self.concept_graph.write().unwrap();
        let mut total = self.total_knowledge_items.write().unwrap();

        *self_nodes = nodes;
        domain_index.clear();
        concept_graph.clear();

        for node in self_nodes.values() {
            domain_index
                .entry(node.domain.clone())
                .or_insert_with(Vec::new)
                .push(node.id.clone());

            concept_graph.insert(node.topic.clone(), node.related_concepts.clone());
        }

        *total = self_nodes.len() as u64;
    }

    fn generate_id(domain: &KnowledgeDomain, topic: &str, content: &str) -> String {
        let data = format!("{:?}:{}:{}", domain, topic, content);
        Self::hash_string(&data)
    }

    fn hash_string(input: &str) -> String {
        let mut hasher = Sha256::new();
        hasher.update(input.as_bytes());
        format!("{:x}", hasher.finalize())
    }

    fn current_timestamp() -> u64 {
        std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap()
            .as_secs()
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeStats {
    pub total_nodes: usize,
    pub training_iterations: u64,
    pub total_knowledge_items: u64,
    pub domain_distribution: HashMap<KnowledgeDomain, usize>,
    pub average_confidence: f64,
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_knowledge_engine_creation() {
        let engine = KnowledgeEngine::new();
        let stats = engine.get_stats();
        assert_eq!(stats.total_nodes, 0);
        assert_eq!(stats.training_iterations, 0);
    }

    #[test]
    fn test_add_knowledge() {
        let engine = KnowledgeEngine::new();
        let id = engine.add_knowledge(
            KnowledgeDomain::Mathematics,
            "Pythagorean Theorem".to_string(),
            "In a right triangle, a² + b² = c²".to_string(),
            vec!["geometry".to_string(), "triangles".to_string()],
        );

        assert!(!id.is_empty());
        let stats = engine.get_stats();
        assert_eq!(stats.total_nodes, 1);
        assert_eq!(stats.total_knowledge_items, 1);
    }

    #[test]
    fn test_query() {
        let engine = KnowledgeEngine::new();
        engine.add_knowledge(
            KnowledgeDomain::Physics,
            "Newton's First Law".to_string(),
            "An object at rest stays at rest unless acted upon by a force".to_string(),
            vec!["mechanics".to_string(), "motion".to_string()],
        );

        let results = engine.query("Newton's First Law");
        assert!(results.is_some());
        assert_eq!(results.unwrap().len(), 1);
    }

    #[test]
    fn test_domain_query() {
        let engine = KnowledgeEngine::new();
        engine.add_knowledge(
            KnowledgeDomain::Philosophy,
            "Cogito ergo sum".to_string(),
            "I think, therefore I am".to_string(),
            vec!["Descartes".to_string(), "epistemology".to_string()],
        );

        let results = engine.query_by_domain(KnowledgeDomain::Philosophy);
        assert_eq!(results.len(), 1);
    }
}
