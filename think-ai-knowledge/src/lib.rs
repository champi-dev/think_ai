pub mod real_content_generator;
pub mod evidence;
pub mod persistence;
pub mod responder;
pub mod trainer;
pub mod real_knowledge;
pub mod training_system;
pub mod comprehensive_knowledge;
pub mod self_learning;
pub mod comprehensive_trainer;
pub mod llm_engine;
pub mod quantum_llm_engine;
pub mod dynamic_loader;
pub mod response_generator;
pub mod intelligent_response_selector;
pub mod tinyllama_knowledge_builder;
pub mod self_evaluator;
pub mod intelligent_relevance;
pub mod feynman_explainer;

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

use crate::quantum_llm_engine::QuantumLLMEngine;
use crate::intelligent_relevance::IntelligentRelevanceEngine;
use crate::feynman_explainer::FeynmanExplainer;

pub struct KnowledgeEngine {
    nodes: Arc<RwLock<HashMap<String, KnowledgeNode>>>,
    domain_index: Arc<RwLock<HashMap<KnowledgeDomain, Vec<String>>>>,
    concept_graph: Arc<RwLock<HashMap<String, Vec<String>>>>,
    training_iterations: Arc<RwLock<u64>>,
    total_knowledge_items: Arc<RwLock<u64>>,
    quantum_llm: Arc<RwLock<Option<QuantumLLMEngine>>>,
    intelligent_relevance: Arc<IntelligentRelevanceEngine>,
    feynman_explainer: Arc<FeynmanExplainer>,
}

impl KnowledgeEngine {
    pub fn new() -> Self {
        let nodes = Arc::new(RwLock::new(HashMap::new()));
        Self {
            nodes: nodes.clone(),
            domain_index: Arc::new(RwLock::new(HashMap::new())),
            concept_graph: Arc::new(RwLock::new(HashMap::new())),
            training_iterations: Arc::new(RwLock::new(0)),
            total_knowledge_items: Arc::new(RwLock::new(0)),
            quantum_llm: Arc::new(RwLock::new(None)),
            intelligent_relevance: Arc::new(IntelligentRelevanceEngine::new()),
            feynman_explainer: Arc::new(FeynmanExplainer::new(Some(nodes))),
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
        let query_lower = query.to_lowercase();
        
        // Collect results while holding read lock
        let mut exact_matches = Vec::new();
        let mut results = Vec::new();
        let mut partial_matches = Vec::new();
        let mut node_ids_to_update = Vec::new();
        
        {
            let nodes = self.nodes.read().unwrap();
            
            for (_, node) in nodes.iter() {
                let topic_lower = node.topic.to_lowercase();
                let content_lower = node.content.to_lowercase();
                
                // Exact topic match gets highest priority
                if topic_lower == query_lower {
                    exact_matches.push(node.clone());
                    node_ids_to_update.push(node.id.clone());
                }
                // Topic contains query
                else if topic_lower.contains(&query_lower) {
                    results.push(node.clone());
                    node_ids_to_update.push(node.id.clone());
                }
                // Content contains query
                else if content_lower.contains(&query_lower) {
                    partial_matches.push(node.clone());
                    node_ids_to_update.push(node.id.clone());
                }
                // Check related concepts
                else {
                    for concept in &node.related_concepts {
                        if concept.to_lowercase().contains(&query_lower) {
                            partial_matches.push(node.clone());
                            node_ids_to_update.push(node.id.clone());
                            break;
                        }
                    }
                }
            }
        } // Read lock dropped here
        
        // Combine results: exact matches first, then topic matches, then content matches
        exact_matches.extend(results);
        exact_matches.extend(partial_matches);

        if exact_matches.is_empty() {
            None
        } else {
            // Update access count and timestamp for retrieved nodes
            // Now we can safely acquire write lock
            let mut nodes_mut = self.nodes.write().unwrap();
            for id in &node_ids_to_update {
                if let Some(node) = nodes_mut.get_mut(id) {
                    node.usage_count += 1;
                    node.last_accessed = Self::current_timestamp();
                }
            }
            drop(nodes_mut);
            
            Some(exact_matches)
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
    
    pub fn intelligent_query(&self, query: &str) -> Vec<KnowledgeNode> {
        // First try direct query for exact matches
        if let Some(results) = self.query(query) {
            if !results.is_empty() {
                return results;
            }
        }
        
        // Use intelligent relevance engine for semantic understanding
        let nodes = self.nodes.read().unwrap();
        let mut scored_results: Vec<(KnowledgeNode, f64)> = Vec::new();
        
        for (_, node) in nodes.iter() {
            let relevance_score = self.intelligent_relevance.compute_relevance(query, node);
            if relevance_score > 0.1 { // Only include reasonably relevant results
                scored_results.push((node.clone(), relevance_score));
            }
        }
        
        // Sort by relevance score (highest first) and take top results
        scored_results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
        let results: Vec<KnowledgeNode> = scored_results.into_iter()
            .take(10)
            .map(|(node, _)| node)
            .collect();
            
        // Learn from this interaction (assume neutral success for now)
        if let Some(selected_node) = results.first() {
            self.intelligent_relevance.learn_from_interaction(query, selected_node, 0.5);
        }
        
        results
    }
    
    
    pub fn get_top_relevant(&self, query: &str, limit: usize) -> Vec<KnowledgeNode> {
        // Try intelligent query to get scored results
        let results = self.intelligent_query(query);
        if !results.is_empty() {
            return results.into_iter().take(limit).collect();
        }
        
        // If still no results, do a broader keyword search
        let query_lower = query.to_lowercase();
        let keywords: Vec<&str> = query_lower.split_whitespace()
            .filter(|w| w.len() > 2) // Skip short words
            .collect();
        
        if keywords.is_empty() {
            return Vec::new();
        }
        
        let nodes = self.nodes.read().unwrap();
        let mut scored_results: Vec<(KnowledgeNode, usize)> = Vec::new();
        
        for (_, node) in nodes.iter() {
            let mut score: usize = 0;
            let topic_lower = node.topic.to_lowercase();
            let content_lower = node.content.to_lowercase();
            
            // Looser matching - any keyword match counts
            for keyword in &keywords {
                if topic_lower.contains(keyword) || content_lower.contains(keyword) {
                    score += 1;
                }
            }
            
            if score > 0 {
                scored_results.push((node.clone(), score));
            }
        }
        
        // Sort by score and return top results
        scored_results.sort_by(|a, b| b.1.cmp(&a.1));
        scored_results.into_iter()
            .take(limit)
            .map(|(node, _)| node)
            .collect()
    }
    
    pub fn generate_llm_response(&self, query: &str) -> String {
        // Use lazy initialization to avoid circular dependency
        let mut llm_lock = self.quantum_llm.write().unwrap();
        if llm_lock.is_none() {
            // Don't create QuantumLLMEngine here to avoid circular dependency
            // Instead, return a basic response
            return "Knowledge engine LLM not initialized. Please use the response generator directly.".to_string();
        }
        llm_lock.as_mut().unwrap().generate_response(query)
    }

    pub fn set_quantum_llm(&self, llm: QuantumLLMEngine) {
        let mut llm_lock = self.quantum_llm.write().unwrap();
        *llm_lock = Some(llm);
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
    
    /// Get all nodes as vector for training
    pub fn get_all_nodes_vec(&self) -> Vec<KnowledgeNode> {
        let nodes = self.nodes.read().unwrap();
        nodes.values().cloned().collect()
    }

    /// Generate a Feynman-style explanation for any concept
    pub fn explain_concept(&self, concept: &str) -> String {
        let explanation = self.feynman_explainer.explain(concept);
        explanation.format_for_human()
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
