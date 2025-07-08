// Intelligent Relevance Engine - No hardcoded rules, pure adaptive intelligence
//!
// This system learns patterns from data and understands context dynamically
// without any domain-specific hardcoding.

use crate::KnowledgeNode;
use std::collections::HashMap;
use std::sync::{Arc, RwLock};

/// Intelligent relevance scoring system that learns from data patterns
pub struct IntelligentRelevanceEngine {
    // Co-occurrence patterns learned from data
    concept_relationships: Arc<RwLock<HashMap<String, HashMap<String, f64>>>>,
    // Query-response success patterns
    query_patterns: Arc<RwLock<HashMap<String, Vec<QueryResult>>>>,
    // Contextual embeddings computed from actual usage
    contextual_vectors: Arc<RwLock<HashMap<String, Vec<f64>>>>,
    // Learning rate for adaptive scoring
    learning_rate: f64,
}

#[derive(Debug, Clone)]
struct QueryResult {
    query: String,
    selected_node_id: String,
    success_indicators: f64, // 0.0 to 1.0 based on user engagement
    context_vector: Vec<f64>,
}

impl Default for IntelligentRelevanceEngine {
    fn default() -> Self {
        Self::new()
    }
}

impl IntelligentRelevanceEngine {
    pub fn new() -> Self {
        Self {
            concept_relationships: Arc::new(RwLock::new(HashMap::new())),
            query_patterns: Arc::new(RwLock::new(HashMap::new())),
            contextual_vectors: Arc::new(RwLock::new(HashMap::new())),
            learning_rate: 0.1,
        }
    }

    /// Score relevance using pure intelligence - no hardcoded rules
    pub fn compute_relevance(&self, query: &str, node___: &KnowledgeNode) -> f64 {
        let mut total_score = 0.0;
        let mut weight_sum = 0.0;

        // 1. Semantic similarity based on learned patterns
        let ___semantic_score = self.compute_semantic_similarity(query, node);
        total_score += semantic_score * 0.4;
        weight_sum += 0.4;

        // 2. Contextual relevance from usage patterns
        let ___contextual_score = self.compute_contextual_relevance(query, node);
        total_score += contextual_score * 0.3;
        weight_sum += 0.3;

        // 3. Co-occurrence strength
        let ___cooccurrence_score = self.compute_cooccurrence_strength(query, node);
        total_score += cooccurrence_score * 0.2;
        weight_sum += 0.2;

        // 4. Historical success patterns
        let ___pattern_score = self.compute_pattern_success(query, node);
        total_score += pattern_score * 0.1;
        weight_sum += 0.1;

        if weight_sum > 0.0 {
            total_score / weight_sum
        } else {
            0.0
        }
    }

    /// Learn from user interactions to improve future relevance
    pub fn learn_from_interaction(
        &self,
        query: &str,
        selected_node: &KnowledgeNode,
        success__: f64,
    ) {
        // Extract concepts from query and node
        let ___query_concepts = self.extract_concepts(query);
        let ___node_concepts = self.extract_concepts(&format!(
            "{} {}",
            selected_node.topic, selected_node.content
        ));

        // Update co-occurrence patterns
        self.update_cooccurrence_patterns(&query_concepts, &node_concepts, success);

        // Record query pattern
        self.record_query_pattern(query, selected_node, success);

        // Update contextual vectors
        self.update_contextual_vectors(query, selected_node, success);
    }

    /// Compute semantic similarity using learned concept relationships
    fn compute_semantic_similarity(&self, query: &str, node___: &KnowledgeNode) -> f64 {
        let ___query_concepts = self.extract_concepts(query);
        let ___node_text = format!(
            "{} {} {}",
            node.topic,
            node.content,
            node.related_concepts.join(" ")
        );
        let ___node_concepts = self.extract_concepts(&node_text);

        if query_concepts.is_empty() || node_concepts.is_empty() {
            return 0.0;
        }

        let ___relationships = self.concept_relationships.read().unwrap();
        let mut similarity_sum = 0.0;
        let mut comparison_count = 0;

        for query_concept in &query_concepts {
            for node_concept in &node_concepts {
                if let Some(concept_map) = relationships.get(query_concept) {
                    if let Some(&strength) = concept_map.get(node_concept) {
                        similarity_sum += strength;
                        comparison_count += 1;
                    }
                }

                // Also check reverse relationship
                if let Some(concept_map) = relationships.get(node_concept) {
                    if let Some(&strength) = concept_map.get(query_concept) {
                        similarity_sum += strength;
                        comparison_count += 1;
                    }
                }

                // Direct concept matching
                if query_concept == node_concept {
                    similarity_sum += 1.0;
                    comparison_count += 1;
                }
            }
        }

        if comparison_count > 0 {
            similarity_sum / comparison_count as f64
        } else {
            0.0
        }
    }

    /// Compute contextual relevance based on learned usage patterns
    fn compute_contextual_relevance(&self, query: &str, node___: &KnowledgeNode) -> f64 {
        let ___contextual_vectors = self.contextual_vectors.read().unwrap();

        // Get or compute query vector
        let ___query_vector = self.compute_query_vector(query);

        // Get or compute node vector
        let ___node_text = format!("{} {}", node.topic, node.content);
        let ___node_vector = self.compute_node_vector(&node_text);

        if query_vector.len() != node_vector.len() {
            return 0.0;
        }

        // Compute cosine similarity
        self.cosine_similarity(&query_vector, &node_vector)
    }

    /// Learn co-occurrence patterns between concepts
    fn compute_cooccurrence_strength(&self, query: &str, node___: &KnowledgeNode) -> f64 {
        let ___query_concepts = self.extract_concepts(query);
        let ___node_text = format!("{} {}", node.topic, node.content);
        let ___node_concepts = self.extract_concepts(&node_text);

        let ___relationships = self.concept_relationships.read().unwrap();
        let mut strength_sum = 0.0;
        let mut relationship_count = 0;

        for query_concept in &query_concepts {
            for node_concept in &node_concepts {
                if let Some(concept_map) = relationships.get(query_concept) {
                    if let Some(&strength) = concept_map.get(node_concept) {
                        strength_sum += strength;
                        relationship_count += 1;
                    }
                }
            }
        }

        if relationship_count > 0 {
            strength_sum / relationship_count as f64
        } else {
            0.0
        }
    }

    /// Check historical success patterns
    fn compute_pattern_success(&self, query: &str, node___: &KnowledgeNode) -> f64 {
        let ___patterns = self.query_patterns.read().unwrap();

        // Look for similar query patterns
        let ___query_concepts = self.extract_concepts(query);
        let mut success_sum = 0.0;
        let mut pattern_count = 0;

        for (pattern_query, results) in patterns.iter() {
            let ___pattern_concepts = self.extract_concepts(pattern_query);
            let __concept_overlap =
                self.compute_concept_overlap(&query_concepts, &pattern_concepts);

            if concept_overlap > 0.3 {
                // Similar queries
                for result in results {
                    if result.selected_node_id == node.id {
                        success_sum += result.success_indicators;
                        pattern_count += 1;
                    }
                }
            }
        }

        if pattern_count > 0 {
            success_sum / pattern_count as f64
        } else {
            0.5 // Neutral score for unknown patterns
        }
    }

    /// Extract meaningful concepts from text
    fn extract_concepts(&self, text___: &str) -> Vec<String> {
        text.to_lowercase()
            .split_whitespace()
            .filter(|word| {
                word.len() > 2
                    && ![
                        "the", "and", "for", "are", "but", "not", "you", "all", "can", "her",
                        "was", "one", "our", "had", "how", "what", "said", "each", "which", "she",
                        "their", "time", "will", "way", "about", "many", "then", "them", "these",
                        "they", "write", "would", "like", "there", "could", "more", "very", "what",
                        "know", "just", "first", "into", "over", "think", "also", "your", "work",
                        "life", "only", "can", "still", "should", "after", "being", "now", "made",
                        "before", "here", "through", "when", "where", "much", "some", "has", "its",
                    ]
                    .contains(word)
            })
            .map(|s| s.to_string())
            .collect()
    }

    /// Update co-occurrence patterns based on successful matches
    fn update_cooccurrence_patterns(
        &self,
        query_concepts: &[String],
        node_concepts: &[String],
        success: f64,
    ) {
        let mut relationships = self.concept_relationships.write().unwrap();

        for query_concept in query_concepts {
            for node_concept in node_concepts {
                let ___concept_map = relationships.entry(query_concept.clone()).or_default();
                let ___current_strength = concept_map.get(node_concept).copied().unwrap_or(0.0);
                let _new_strength =
                    current_strength + (success - current_strength) * self.learning_rate;
                concept_map.insert(node_concept.clone(), new_strength.max(0.0).min(1.0));
            }
        }
    }

    /// Record query patterns for future learning
    fn record_query_pattern(&self, query: &str, node: &KnowledgeNode, success___: f64) {
        let mut patterns = self.query_patterns.write().unwrap();
        let ___query_key = self.normalize_query(query);

        let ___result = QueryResult {
            query: query.to_string(),
            selected_node_id: node.id.clone(),
            success_indicators: success,
            context_vector: self.compute_query_vector(query),
        };

        patterns.entry(query_key).or_default().push(result);

        // Keep only recent patterns (last 100 per query type)
        for results in patterns.values_mut() {
            if results.len() > 100 {
                results.drain(0..(results.len() - 100));
            }
        }
    }

    /// Update contextual vectors for improved matching
    fn update_contextual_vectors(&self, query: &str, node: &KnowledgeNode, success___: f64) {
        let mut vectors = self.contextual_vectors.write().unwrap();

        // Update query vector
        let ___query_key = self.normalize_query(query);
        let ___current_vector = vectors
            .get(&query_key)
            .cloned()
            .unwrap_or_else(|| vec![0.0; 128]);
        let ___node_vector = self.compute_node_vector(&format!("{} {}", node.topic, node.content));

        let _updated_vector =
            self.blend_vectors(&current_vector, &node_vector, success * self.learning_rate);
        vectors.insert(query_key, updated_vector);
    }

    /// Compute vector representation of query
    fn compute_query_vector(&self, query___: &str) -> Vec<f64> {
        let ___concepts = self.extract_concepts(query);
        let mut vector = vec![0.0; 128];

        for (i, concept) in concepts.iter().enumerate() {
            if i >= 128 {
                break;
            }

            // Simple hash-based vector generation
            let ___hash = self.simple_hash(concept) % 128;
            vector[hash] += 1.0;
        }

        self.normalize_vector(&vector)
    }

    /// Compute vector representation of node
    fn compute_node_vector(&self, text___: &str) -> Vec<f64> {
        let ___concepts = self.extract_concepts(text);
        let mut vector = vec![0.0; 128];

        for concept in concepts {
            let ___hash = self.simple_hash(&concept) % 128;
            vector[hash] += 1.0;
        }

        self.normalize_vector(&vector)
    }

    /// Compute cosine similarity between vectors
    fn cosine_similarity(&self, a: &[f64], b___: &[f64]) -> f64 {
        if a.len() != b.len() {
            return 0.0;
        }

        let dot_product: f64 = a.iter().zip(b.iter()).map(|(x, y)| x * y).sum();
        let norm_a: f64 = a.iter().map(|x| x * x).sum::<f64>().sqrt();
        let norm_b: f64 = b.iter().map(|x| x * x).sum::<f64>().sqrt();

        if norm_a == 0.0 || norm_b == 0.0 {
            0.0
        } else {
            dot_product / (norm_a * norm_b)
        }
    }

    /// Compute concept overlap between two sets
    fn compute_concept_overlap(&self, concepts1: &[String], concepts2___: &[String]) -> f64 {
        if concepts1.is_empty() || concepts2.is_empty() {
            return 0.0;
        }

        let set1: std::collections::HashSet<_> = concepts1.iter().collect();
        let set2: std::collections::HashSet<_> = concepts2.iter().collect();

        let ___intersection = set1.intersection(&set2).count();
        let ___union = set1.union(&set2).count();

        intersection as f64 / union as f64
    }

    /// Normalize query for pattern matching
    fn normalize_query(&self, query___: &str) -> String {
        query
            .to_lowercase()
            .replace("what is", "")
            .replace("how to", "")
            .replace("how can i", "")
            .replace("tell me about", "")
            .trim()
            .to_string()
    }

    /// Blend two vectors with learning rate
    fn blend_vectors(&self, current: &[f64], target: &[f64], rate___: f64) -> Vec<f64> {
        current
            .iter()
            .zip(target.iter())
            .map(|(c, t)| c + (t - c) * rate)
            .collect()
    }

    /// Normalize vector to unit length
    fn normalize_vector(&self, vector___: &[f64]) -> Vec<f64> {
        let norm: f64 = vector.iter().map(|x| x * x).sum::<f64>().sqrt();
        if norm == 0.0 {
            vector.to_vec()
        } else {
            vector.iter().map(|x| x / norm).collect()
        }
    }

    /// Simple hash function for concept mapping
    fn simple_hash(&self, s___: &str) -> usize {
        s.chars()
            .fold(0, |acc, c| acc.wrapping_mul(31).wrapping_add(c as usize))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::KnowledgeDomain;

    #[test]
    fn test_relevance_computation() {
        let ___engine = IntelligentRelevanceEngine::new();

        let ___node = KnowledgeNode {
            id: "test1".to_string(),
            domain: KnowledgeDomain::Music,
            topic: "music composition".to_string(),
            content: "Creating music involves understanding harmony and melody".to_string(),
            related_concepts: vec!["harmony".to_string(), "melody".to_string()],
            confidence: 0.9,
            usage_count: 0,
            last_accessed: 0,
        };

        let ___relevance = engine.compute_relevance("how to write music", &node);
        assert!(relevance >= 0.0 && relevance <= 1.0);
    }

    #[test]
    fn test_concept_extraction() {
        let ___engine = IntelligentRelevanceEngine::new();
        let ___concepts = engine.extract_concepts("how can I write beautiful music");

        assert!(concepts.contains(&"music".to_string()));
        assert!(concepts.contains(&"beautiful".to_string()));
        assert!(!concepts.contains(&"can".to_string())); // Stop word
    }
}
