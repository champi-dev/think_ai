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
pub mod enhanced_quantum_llm;
pub mod dynamic_loader;
pub mod response_generator;
pub mod intelligent_response_selector;
pub mod tinyllama_knowledge_builder;
pub mod self_evaluator;
pub mod intelligent_relevance;
pub mod feynman_explainer;
pub mod multi_candidate_selector;
pub mod llm_benchmarks;
pub mod benchmark_trainer;
pub mod o1_benchmark_monitor;
pub mod automated_benchmark_runner;
pub mod conversation_memory;
pub mod multilevel_cache;
pub mod multilevel_response_component;
pub mod simple_cache_component;

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
    // O(1) Performance Indexes
    topic_index: Arc<RwLock<HashMap<String, Vec<String>>>>, // topic -> node_ids
    keyword_index: Arc<RwLock<HashMap<String, Vec<String>>>>, // keyword -> node_ids  
    content_hash_index: Arc<RwLock<HashMap<String, String>>>, // content_hash -> node_id
    quick_lookup_cache: Arc<RwLock<HashMap<String, Vec<(KnowledgeNode, f32)>>>>, // query -> cached results
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
            // Initialize O(1) Performance Indexes
            topic_index: Arc::new(RwLock::new(HashMap::new())),
            keyword_index: Arc::new(RwLock::new(HashMap::new())),
            content_hash_index: Arc::new(RwLock::new(HashMap::new())),
            quick_lookup_cache: Arc::new(RwLock::new(HashMap::new())),
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
        nodes.insert(id.clone(), node.clone());

        let mut domain_index = self.domain_index.write().unwrap();
        domain_index
            .entry(domain)
            .or_insert_with(Vec::new)
            .push(id.clone());

        let mut concept_graph = self.concept_graph.write().unwrap();
        concept_graph.insert(topic.clone(), related.clone());

        // Update O(1) Performance Indexes
        self.update_indexes(&id, &node);

        let mut total = self.total_knowledge_items.write().unwrap();
        *total += 1;

        id
    }

    pub fn query(&self, query: &str) -> Option<Vec<KnowledgeNode>> {
        let query_lower = query.to_lowercase();
        
        // Check if this is a definition query ("what is X", "define X", etc.)
        let is_definition_query = query_lower.starts_with("what is ") || 
                                 query_lower.starts_with("what's ") ||
                                 query_lower.starts_with("define ") ||
                                 query_lower.starts_with("explain ");
        let key_concept = if is_definition_query {
            self.extract_key_concept(query).to_lowercase()
        } else {
            query_lower.clone()
        };
        
        // Collect results with scoring
        let mut scored_results = Vec::new();
        let mut node_ids_to_update = Vec::new();
        
        {
            let nodes = self.nodes.read().unwrap();
            
            for (_, node) in nodes.iter() {
                let topic_lower = node.topic.to_lowercase();
                let content_lower = node.content.to_lowercase();
                let mut score = 0.0f32;
                let mut matched = false;
                
                // Score exact topic matches highest
                if is_definition_query && topic_lower == key_concept {
                    score = 100.0;
                    matched = true;
                } else if topic_lower == query_lower {
                    score = 95.0;
                    matched = true;
                }
                // Score primary topic matches for definition queries
                else if is_definition_query && topic_lower.starts_with(&key_concept) && 
                        (topic_lower.len() - key_concept.len()) < 10 {
                    score = 90.0;
                    matched = true;
                }
                // Score topic word boundary matches
                else if Self::word_boundary_match(&topic_lower, &query_lower) {
                    if is_definition_query {
                        // For definition queries, prioritize based on how central the concept is
                        let words = topic_lower.split_whitespace().collect::<Vec<_>>();
                        if words.len() <= 3 && words.contains(&key_concept.as_str()) {
                            score = 85.0; // Short, focused topics
                        } else if words.contains(&key_concept.as_str()) {
                            score = 60.0; // Longer topics but contains concept
                        } else {
                            score = 40.0; // Contains query but not the key concept
                        }
                    } else {
                        score = 75.0;
                    }
                    matched = true;
                }
                // Score content matches, but boost for definition queries
                else if Self::word_boundary_match(&content_lower, &query_lower) {
                    if is_definition_query {
                        // For definition queries, content that directly defines the concept should score higher
                        let content_start = content_lower.split_whitespace().take(20).collect::<Vec<_>>().join(" ");
                        if content_start.contains(&key_concept) {
                            score = 70.0; // Higher score for content that defines the concept
                        } else {
                            score = 30.0; // Standard content match
                        }
                    } else {
                        score = 30.0;
                    }
                    matched = true;
                }
                // Check related concepts
                else {
                    for concept in &node.related_concepts {
                        let concept_lower = concept.to_lowercase();
                        if query_lower.contains(&concept_lower) || 
                           query_lower.split_whitespace().any(|word| word == concept_lower) {
                            score = 25.0;
                            matched = true;
                            break;
                        }
                    }
                }
                
                if matched {
                    // Apply domain relevance boost for definition queries
                    if is_definition_query {
                        score += Self::calculate_domain_relevance_boost(&key_concept, &node.domain);
                    }
                    
                    scored_results.push((node.clone(), score));
                    node_ids_to_update.push(node.id.clone());
                }
            }
        } // Read lock dropped here
        
        if scored_results.is_empty() {
            None
        } else {
            // Sort by score (highest first)
            scored_results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
            
            // Extract sorted nodes
            let exact_matches: Vec<KnowledgeNode> = scored_results.into_iter()
                .map(|(node, _)| node)
                .collect();
            
            // Update access count and timestamp for retrieved nodes
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
        // Extract key concept from "what is X" questions
        let processed_query = self.extract_key_concept(query);
        
        // First try direct query for exact matches on processed query
        if let Some(results) = self.fast_query(&processed_query) {
            if !results.is_empty() {
                return results;
            }
        }
        
        // If no results from processed query, try original query
        if processed_query != query {
            if let Some(results) = self.fast_query(query) {
                if !results.is_empty() {
                    return results;
                }
            }
        }
        
        // Use intelligent relevance engine for semantic understanding
        let nodes = self.nodes.read().unwrap();
        let mut scored_results: Vec<(KnowledgeNode, f64)> = Vec::new();
        
        // Try relevance search with processed query first
        for (_, node) in nodes.iter() {
            let relevance_score = self.intelligent_relevance.compute_relevance(&processed_query, node);
            if relevance_score > 0.1 { // Only include reasonably relevant results
                scored_results.push((node.clone(), relevance_score));
            }
        }
        
        // If no good results from processed query, try original query  
        if scored_results.is_empty() && processed_query != query {
            for (_, node) in nodes.iter() {
                let relevance_score = self.intelligent_relevance.compute_relevance(query, node);
                if relevance_score > 0.1 {
                    scored_results.push((node.clone(), relevance_score));
                }
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
    
    /// Extract key concept from definition questions like "what is X" -> "X"
    fn extract_key_concept(&self, query: &str) -> String {
        let query_lower = query.to_lowercase().trim().to_string();
        
        // Handle "what is X" questions
        if query_lower.starts_with("what is ") {
            let concept = query_lower.strip_prefix("what is ").unwrap_or(&query_lower);
            // Remove common question words and punctuation
            let cleaned = concept.replace("the ", "").replace("?", "");
            return cleaned.trim().to_string();
        }
        
        // Handle "what's X" questions  
        if query_lower.starts_with("what's ") {
            let concept = query_lower.strip_prefix("what's ").unwrap_or(&query_lower);
            let cleaned = concept.replace("the ", "").replace("?", "");
            return cleaned.trim().to_string();
        }
        
        // Handle "define X" questions
        if query_lower.starts_with("define ") {
            let concept = query_lower.strip_prefix("define ").unwrap_or(&query_lower);
            let cleaned = concept.replace("the ", "").replace("?", "");
            return cleaned.trim().to_string();
        }
        
        // Handle "explain X" questions
        if query_lower.starts_with("explain ") {
            let concept = query_lower.strip_prefix("explain ").unwrap_or(&query_lower);
            let cleaned = concept.replace("the ", "").replace("?", "");
            return cleaned.trim().to_string();
        }
        
        // Return original query if no pattern matches
        query.to_string()
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
    
    /// Get access to the intelligent relevance engine
    pub fn get_intelligent_relevance(&self) -> Arc<IntelligentRelevanceEngine> {
        self.intelligent_relevance.clone()
    }
    
    /// Comprehensive search that combines multiple search strategies
    pub fn search_comprehensive(&self, query: &str, domain_filter: Option<KnowledgeDomain>) -> Vec<KnowledgeNode> {
        // First try intelligent query
        let mut results = self.intelligent_query(query);
        
        // If limited results, try direct query
        if results.len() < 5 {
            if let Some(direct_results) = self.fast_query(query) {
                for node in direct_results {
                    if !results.iter().any(|r| r.id == node.id) {
                        results.push(node);
                    }
                }
            }
        }
        
        // If still limited results, try broader keyword search
        if results.len() < 5 {
            let broader_results = self.get_top_relevant(query, 10);
            for node in broader_results {
                if !results.iter().any(|r| r.id == node.id) {
                    results.push(node);
                }
            }
        }
        
        // Filter by domain if specified
        if let Some(domain) = domain_filter {
            results = results.into_iter()
                .filter(|node| node.domain == domain)
                .collect();
        }
        
        // Limit to top 10 results
        results.truncate(10);
        results
    }
    
    /// Word boundary aware matching to prevent false positives like "matter" matching "matters"
    fn word_boundary_match(text: &str, query: &str) -> bool {
        // Split query into words for multi-word queries
        let query_words: Vec<&str> = query.split_whitespace().collect();
        
        if query_words.len() == 1 {
            // Single word query - use word boundary matching
            let word = query_words[0];
            let text_words: Vec<&str> = text.split_whitespace().collect();
            
            // Check if any word in text exactly matches the query word
            text_words.iter().any(|&text_word| {
                // Remove punctuation for comparison
                let clean_text_word = text_word.trim_matches(|c: char| !c.is_alphanumeric());
                clean_text_word == word
            })
        } else {
            // Multi-word query - check if all query words appear as complete words in text
            let text_words: Vec<String> = text.split_whitespace()
                .map(|w| w.trim_matches(|c: char| !c.is_alphanumeric()).to_string())
                .collect();
            
            query_words.iter().all(|&query_word| {
                text_words.iter().any(|text_word| text_word == query_word)
            })
        }
    }
    
    /// Calculate domain relevance boost for definition queries
    fn calculate_domain_relevance_boost(concept: &str, domain: &KnowledgeDomain) -> f32 {
        match concept {
            // Space concepts - prioritize astronomy and physics
            "space" | "universe" | "cosmos" | "galaxy" | "star" | "planet" => {
                match domain {
                    KnowledgeDomain::Astronomy => 15.0,
                    KnowledgeDomain::Physics => 10.0,
                    KnowledgeDomain::Philosophy => 5.0,
                    _ => 0.0,
                }
            },
            // Matter concepts - prioritize physics and chemistry
            "matter" | "atom" | "molecule" | "element" | "compound" => {
                match domain {
                    KnowledgeDomain::Physics => 15.0,
                    KnowledgeDomain::Chemistry => 15.0,
                    KnowledgeDomain::Philosophy => 3.0,
                    _ => 0.0,
                }
            },
            // Time concepts - prioritize physics and philosophy
            "time" | "temporal" | "duration" => {
                match domain {
                    KnowledgeDomain::Physics => 15.0,
                    KnowledgeDomain::Philosophy => 10.0,
                    KnowledgeDomain::Astronomy => 8.0,
                    _ => 0.0,
                }
            },
            // Life concepts - prioritize biology and medicine
            "life" | "organism" | "cell" | "dna" | "gene" => {
                match domain {
                    KnowledgeDomain::Biology => 15.0,
                    KnowledgeDomain::Medicine => 12.0,
                    KnowledgeDomain::Philosophy => 5.0,
                    _ => 0.0,
                }
            },
            // Mind concepts - prioritize psychology and philosophy
            "mind" | "consciousness" | "thought" | "brain" => {
                match domain {
                    KnowledgeDomain::Psychology => 15.0,
                    KnowledgeDomain::Philosophy => 12.0,
                    KnowledgeDomain::Biology => 8.0,
                    _ => 0.0,
                }
            },
            // Math concepts - prioritize mathematics
            "number" | "equation" | "algebra" | "geometry" | "calculus" => {
                match domain {
                    KnowledgeDomain::Mathematics => 15.0,
                    KnowledgeDomain::Physics => 5.0,
                    _ => 0.0,
                }
            },
            // Computing concepts - prioritize computer science
            "computer" | "algorithm" | "software" | "programming" => {
                match domain {
                    KnowledgeDomain::ComputerScience => 15.0,
                    KnowledgeDomain::Engineering => 8.0,
                    _ => 0.0,
                }
            },
            // Default case - no boost
            _ => 0.0,
        }
    }

    // O(1) Performance Methods
    fn update_indexes(&self, node_id: &str, node: &KnowledgeNode) {
        // Update topic index for O(1) topic lookups
        let topic_key = node.topic.to_lowercase();
        let mut topic_index = self.topic_index.write().unwrap();
        topic_index.entry(topic_key).or_insert_with(Vec::new).push(node_id.to_string());

        // Update keyword index for O(1) keyword lookups  
        let mut keyword_index = self.keyword_index.write().unwrap();
        
        // Index topic words
        for word in node.topic.to_lowercase().split_whitespace() {
            if word.len() > 2 { // Skip very short words
                keyword_index.entry(word.to_string()).or_insert_with(Vec::new).push(node_id.to_string());
            }
        }
        
        // Index content words (first 50 words to avoid bloat)
        for word in node.content.to_lowercase().split_whitespace().take(50) {
            if word.len() > 3 { // Only meaningful words
                let clean_word = word.trim_matches(|c: char| !c.is_alphanumeric());
                if clean_word.len() > 3 {
                    keyword_index.entry(clean_word.to_string()).or_insert_with(Vec::new).push(node_id.to_string());
                }
            }
        }
        
        // Index related concepts
        for concept in &node.related_concepts {
            let concept_key = concept.to_lowercase();
            keyword_index.entry(concept_key).or_insert_with(Vec::new).push(node_id.to_string());
        }

        // Update content hash index for exact duplicate detection
        let content_hash = Self::hash_content(&node.content);
        let mut content_hash_index = self.content_hash_index.write().unwrap();
        content_hash_index.insert(content_hash, node_id.to_string());
    }

    fn hash_content(content: &str) -> String {
        use sha2::{Digest, Sha256};
        let mut hasher = Sha256::new();
        hasher.update(content.as_bytes());
        format!("{:x}", hasher.finalize())
    }

    // O(1) Fast Query - replaces the slow O(n) query method
    pub fn fast_query(&self, query: &str) -> Option<Vec<KnowledgeNode>> {
        let query_key = query.to_lowercase();
        
        // Check cache first - O(1) lookup
        {
            let cache = self.quick_lookup_cache.read().unwrap();
            if let Some(cached_results) = cache.get(&query_key) {
                return Some(cached_results.iter().map(|(node, _score)| node.clone()).collect());
            }
        }

        let mut candidate_nodes = Vec::new();
        let nodes = self.nodes.read().unwrap();

        // O(1) Topic exact match lookup
        if let Some(node_ids) = self.topic_index.read().unwrap().get(&query_key) {
            for node_id in node_ids {
                if let Some(node) = nodes.get(node_id) {
                    candidate_nodes.push((node.clone(), 100.0)); // Highest score for exact topic match
                }
            }
        }

        // O(1) Keyword lookups
        let keyword_index = self.keyword_index.read().unwrap();
        for word in query_key.split_whitespace() {
            if let Some(node_ids) = keyword_index.get(word) {
                for node_id in node_ids {
                    if let Some(node) = nodes.get(node_id) {
                        // Check if already added from topic match
                        if !candidate_nodes.iter().any(|(n, _)| n.id == node.id) {
                            let score = if node.topic.to_lowercase().contains(word) { 75.0 } else { 50.0 };
                            candidate_nodes.push((node.clone(), score));
                        }
                    }
                }
            }
        }

        // Sort by score and limit results
        candidate_nodes.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        candidate_nodes.truncate(10);

        // Cache results for O(1) future lookups
        let results: Vec<KnowledgeNode> = candidate_nodes.iter().map(|(node, _)| node.clone()).collect();
        {
            let mut cache = self.quick_lookup_cache.write().unwrap();
            cache.insert(query_key, candidate_nodes.clone());
            
            // Limit cache size to prevent memory bloat
            if cache.len() > 1000 {
                cache.clear(); // Simple cache eviction
            }
        }

        if results.is_empty() {
            None
        } else {
            Some(results)
        }
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
