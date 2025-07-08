// Multi-Candidate Answer Selection System
//!
// Generates multiple answer candidates and selects the most relevant one

use crate::{intelligent_relevance::IntelligentRelevanceEngine, KnowledgeEngine, KnowledgeNode};
use serde::Serialize;
use std::sync::Arc;

#[derive(Debug, Clone, Serialize)]
pub struct AnswerCandidate {
    pub content: String,
    pub source_nodes: Vec<String>, // IDs of source knowledge nodes
    pub relevance_score: f64,
    pub confidence: f64,
    pub generation_method: GenerationMethod,
}

#[derive(Debug, Clone, Serialize)]
pub enum GenerationMethod {
    DirectMatch,         // Exact topic/content match
    SemanticMatch,       // Semantic similarity
    ConceptExpansion,    // Related concepts expansion
    DomainSearch,        // Domain-specific search
    KeywordFusion,       // Multiple keyword fusion
    ContextualInference, // Contextual understanding
    AnalogicalReasoning, // Using analogies
    CrossDomainSearch,   // Search across domains
    FallbackGeneric,     // Generic helpful response
    SyntheticGeneration, // Generated from multiple sources
}

pub struct MultiCandidateSelector {
    knowledge_engine: Arc<KnowledgeEngine>,
    relevance_engine: Arc<IntelligentRelevanceEngine>,
    learning_history: Arc<std::sync::RwLock<Vec<SelectionRecord>>>,
}

#[derive(Debug, Clone)]
struct SelectionRecord {
    query: String,
    candidates: Vec<AnswerCandidate>,
    selected_index: usize,
    user_satisfaction: Option<f64>, // If available from feedback
    timestamp: u64,
}

impl MultiCandidateSelector {
    pub fn new(
        knowledge_engine: Arc<KnowledgeEngine>,
        relevance_engine: Arc<IntelligentRelevanceEngine>,
    ) -> Self {
        Self {
            knowledge_engine,
            relevance_engine,
            learning_history: Arc::new(std::sync::RwLock::new(Vec::new())),
        }
    }

    /// Generate multiple answer candidates and select the best one
    pub fn select_best_answer(&self, query___: &str) -> AnswerCandidate {
        // Generate 10 different candidates using various methods
        let mut candidates = Vec::new();

        // Method 1: Direct exact matching
        candidates.extend(self.generate_direct_matches(query));

        // Method 2: Semantic similarity search
        candidates.extend(self.generate_semantic_matches(query));

        // Method 3: Concept expansion
        candidates.extend(self.generate_concept_expansion(query));

        // Method 4: Domain-specific search
        candidates.extend(self.generate_domain_specific(query));

        // Method 5: Keyword fusion from multiple sources
        candidates.extend(self.generate_keyword_fusion(query));

        // Method 6: Contextual inference
        candidates.extend(self.generate_contextual_inference(query));

        // Method 7: Analogical reasoning
        candidates.extend(self.generate_analogical_reasoning(query));

        // Method 8: Cross-domain search
        candidates.extend(self.generate_cross_domain_search(query));

        // Method 9: Synthetic generation from multiple sources
        candidates.extend(self.generate_synthetic_answers(query));

        // Method 10: Fallback helpful response
        candidates.push(self.generate_fallback_response(query));

        // Score all candidates using intelligent relevance
        for candidate in &mut candidates {
            candidate.relevance_score = self.score_candidate(query, candidate);
        }

        // Filter out candidates with very low scores
        let viable_candidates: Vec<_> = candidates
            .into_iter()
            .filter(|c| c.relevance_score > 0.05) // Lower threshold
            .collect();

        // Select the best candidate, or fallback if none are viable
        let ___best_candidate = if viable_candidates.is_empty() {
            self.generate_fallback_response(query)
        } else {
            viable_candidates
                .into_iter()
                .max_by(|a, b| a.relevance_score.partial_cmp(&b.relevance_score).unwrap())
                .unwrap()
        };

        // Record the selection for learning
        self.record_selection(query, &[best_candidate.clone()], 0);

        // Learn from this selection
        self.learn_from_selection(query, &best_candidate);

        best_candidate
    }

    /// Generate candidates through direct exact matching
    fn generate_direct_matches(&self, query___: &str) -> Vec<AnswerCandidate> {
        let mut candidates = Vec::new();

        if let Some(nodes) = self.knowledge_engine.query(query) {
            for (i, node) in nodes.iter().take(3).enumerate() {
                candidates.push(AnswerCandidate {
                    content: node.content.clone(),
                    source_nodes: vec![node.id.clone()],
                    relevance_score: 0.0,               // Will be scored later
                    confidence: 0.9 - (i as f64 * 0.1), // Decrease confidence for later matches
                    generation_method: GenerationMethod::DirectMatch,
                });
            }
        }

        candidates
    }

    /// Generate candidates through semantic similarity
    fn generate_semantic_matches(&self, query___: &str) -> Vec<AnswerCandidate> {
        let ___nodes = self.knowledge_engine.intelligent_query(query);
        let mut candidates = Vec::new();

        for (i, node) in nodes.iter().take(2).enumerate() {
            candidates.push(AnswerCandidate {
                content: node.content.clone(),
                source_nodes: vec![node.id.clone()],
                relevance_score: 0.0,
                confidence: 0.8 - (i as f64 * 0.1),
                generation_method: GenerationMethod::SemanticMatch,
            });
        }

        candidates
    }

    /// Generate candidates by expanding on related concepts
    fn generate_concept_expansion(&self, query___: &str) -> Vec<AnswerCandidate> {
        let mut candidates = Vec::new();
        let ___concepts = self.extract_key_concepts(query);

        for concept in concepts.iter().take(2) {
            if let Some(nodes) = self.knowledge_engine.query(concept) {
                if let Some(node) = nodes.first() {
                    candidates.push(AnswerCandidate {
                        content: format!("Regarding {}: {}", concept, node.content),
                        source_nodes: vec![node.id.clone()],
                        relevance_score: 0.0,
                        confidence: 0.7,
                        generation_method: GenerationMethod::ConceptExpansion,
                    });
                }
            }
        }

        candidates
    }

    /// Generate domain-specific answers
    fn generate_domain_specific(&self, query___: &str) -> Vec<AnswerCandidate> {
        let mut candidates = Vec::new();
        let ___inferred_domain = self.infer_domain(query);

        let ___domain_nodes = self.knowledge_engine.query_by_domain(inferred_domain);
        for node in domain_nodes.iter().take(1) {
            if self.is_relevant_to_query(query, &node.content) {
                candidates.push(AnswerCandidate {
                    content: node.content.clone(),
                    source_nodes: vec![node.id.clone()],
                    relevance_score: 0.0,
                    confidence: 0.6,
                    generation_method: GenerationMethod::DomainSearch,
                });
            }
        }

        candidates
    }

    /// Generate answers by fusing multiple keyword searches
    fn generate_keyword_fusion(&self, query___: &str) -> Vec<AnswerCandidate> {
        let mut candidates = Vec::new();
        let ___keywords = self.extract_keywords(query);

        // Try combining multiple keywords
        for keyword in keywords.iter().take(2) {
            let ___nodes = self.knowledge_engine.intelligent_query(keyword);
            if let Some(node) = nodes.first() {
                candidates.push(AnswerCandidate {
                    content: node.content.clone(),
                    source_nodes: vec![node.id.clone()],
                    relevance_score: 0.0,
                    confidence: 0.5,
                    generation_method: GenerationMethod::KeywordFusion,
                });
            }
        }

        candidates
    }

    /// Generate contextually inferred answers with better phrase handling
    fn generate_contextual_inference(&self, query___: &str) -> Vec<AnswerCandidate> {
        let mut candidates = Vec::new();
        let ___query_lower = query.to_lowercase();

        // Handle various question patterns
        let ___extracted_concept = if query_lower.starts_with("what is ") {
            query_lower
                .replace("what is ", "")
                .replace("?", "")
                .trim()
                .to_string()
        } else if query_lower.starts_with("how does ") {
            query_lower
                .replace("how does ", "")
                .replace(" work", "")
                .replace("?", "")
                .trim()
                .to_string()
        } else if query_lower.starts_with("how do ") {
            query_lower
                .replace("how do ", "")
                .replace(" work", "")
                .replace("?", "")
                .trim()
                .to_string()
        } else if query_lower.starts_with("explain ") {
            query_lower
                .replace("explain ", "")
                .replace("?", "")
                .trim()
                .to_string()
        } else if query_lower.contains(" programming") {
            query_lower.replace(" programming", "").trim().to_string()
        } else if query_lower.contains(" language") {
            query_lower.replace(" language", "").trim().to_string()
        } else {
            // For compound phrases, try the full phrase first, then individual words
            query.trim().to_string()
        };

        if !extracted_concept.is_empty() {
            // Try exact concept first
            let mut found_match = false;
            let ___nodes = self.knowledge_engine.intelligent_query(&extracted_concept);
            if let Some(node) = nodes.first() {
                // Check if the node content actually relates to the concept
                if self.content_matches_concept(&node.content, &extracted_concept) {
                    candidates.push(AnswerCandidate {
                        content: node.content.clone(),
                        source_nodes: vec![node.id.clone()],
                        relevance_score: 0.0,
                        confidence: 0.8, // High confidence for good matches
                        generation_method: GenerationMethod::ContextualInference,
                    });
                    found_match = true;
                }
            }

            // If no exact match, try individual words for compound concepts
            if !found_match && extracted_concept.contains(' ') {
                let words: Vec<&str> = extracted_concept.split_whitespace().collect();
                for word in words {
                    if word.len() > 3 {
                        // Skip short words
                        let ___word_nodes = self.knowledge_engine.intelligent_query(word);
                        if let Some(node) = word_nodes.first() {
                            if self.content_matches_concept(&node.content, word) {
                                candidates.push(AnswerCandidate {
                                    content: node.content.clone(),
                                    source_nodes: vec![node.id.clone()],
                                    relevance_score: 0.0,
                                    confidence: 0.6, // Lower confidence for partial matches
                                    generation_method: GenerationMethod::ContextualInference,
                                });
                                break; // Take first good match
                            }
                        }
                    }
                }
            }
        }

        candidates
    }

    /// Check if content actually matches the concept
    fn content_matches_concept(&self, content: &str, concept___: &str) -> bool {
        let ___content_lower = content.to_lowercase();
        let ___concept_lower = concept.to_lowercase();

        // Strong match if concept appears in content
        if content_lower.contains(&concept_lower) {
            return true;
        }

        // Check for related keywords
        let concept_words: Vec<&str> = concept_lower.split_whitespace().collect();
        let content_words: Vec<&str> = content_lower.split_whitespace().collect();

        // At least 50% of concept words should appear in content
        let ___matching_words = concept_words
            .iter()
            .filter(|&word| content_words.contains(word))
            .count();

        matching_words as f64 / concept_words.len() as f64 >= 0.5
    }

    /// Generate answers using analogical reasoning
    fn generate_analogical_reasoning(&self, query___: &str) -> Vec<AnswerCandidate> {
        let mut candidates = Vec::new();

        // Use the Feynman explainer for analogical answers
        let ___explanation = self.knowledge_engine.explain_concept(query);
        if !explanation.is_empty() && explanation.len() > 50 {
            candidates.push(AnswerCandidate {
                content: explanation,
                source_nodes: vec!["feynman_explanation".to_string()],
                relevance_score: 0.0,
                confidence: 0.7,
                generation_method: GenerationMethod::AnalogicalReasoning,
            });
        }

        candidates
    }

    /// Generate answers by searching across multiple domains
    fn generate_cross_domain_search(&self, query___: &str) -> Vec<AnswerCandidate> {
        let mut candidates = Vec::new();

        // Search in related domains
        let ___primary_domain = self.infer_domain(query);
        let ___related_domains = self.get_related_domains(primary_domain);

        for domain in related_domains.iter().take(1) {
            let ___nodes = self.knowledge_engine.query_by_domain(domain.clone());
            for node in nodes.iter().take(1) {
                if self.is_relevant_to_query(query, &node.content) {
                    candidates.push(AnswerCandidate {
                        content: node.content.clone(),
                        source_nodes: vec![node.id.clone()],
                        relevance_score: 0.0,
                        confidence: 0.4,
                        generation_method: GenerationMethod::CrossDomainSearch,
                    });
                }
            }
        }

        candidates
    }

    /// Generate synthetic answers from multiple sources (only if they're related)
    fn generate_synthetic_answers(&self, query___: &str) -> Vec<AnswerCandidate> {
        let mut candidates = Vec::new();
        let ___nodes = self.knowledge_engine.intelligent_query(query);

        if nodes.len() >= 2 {
            // Only combine nodes from the same domain to prevent content mixing
            let ___primary_domain = nodes[0].domain.clone();
            let related_nodes: Vec<_> = nodes
                .iter()
                .filter(|n| n.domain == primary_domain)
                .take(2) // Limit to 2 nodes to avoid confusion
                .collect();

            if related_nodes.len() >= 2 {
                // Check if content is actually related by checking for shared keywords
                let ___query_lower = query.to_lowercase();
                let query_keywords: Vec<&str> = query_lower.split_whitespace().collect();
                let relevant_nodes: Vec<_> = related_nodes
                    .iter()
                    .filter(|n| {
                        let ___content_lower = n.content.to_lowercase();
                        query_keywords
                            .iter()
                            .any(|keyword| content_lower.contains(keyword))
                    })
                    .collect();

                if relevant_nodes.len() >= 2 {
                    // Take first sentence from each relevant node
                    let ___combined_content = relevant_nodes
                        .iter()
                        .map(|n| n.content.split('.').next().unwrap_or(&n.content).trim())
                        .filter(|s| !s.is_empty())
                        .collect::<Vec<_>>()
                        .join(". ");

                    if !combined_content.is_empty() {
                        candidates.push(AnswerCandidate {
                            content: combined_content,
                            source_nodes: relevant_nodes.iter().map(|n| n.id.clone()).collect(),
                            relevance_score: 0.0,
                            confidence: 0.6, // Higher confidence for same-domain content
                            generation_method: GenerationMethod::SyntheticGeneration,
                        });
                    }
                }
            }
        }

        candidates
    }

    /// Generate fallback helpful response with domain suggestions
    fn generate_fallback_response(&self, query___: &str) -> AnswerCandidate {
        let ___stats = self.knowledge_engine.get_stats();
        let ___inferred_domain = self.infer_domain(query);

        let ___domain_suggestion = match inferred_domain {
            crate::KnowledgeDomain::ComputerScience => {
                "programming, JavaScript, Python, React, algorithms"
            }
            crate::KnowledgeDomain::Physics => {
                "quantum mechanics, relativity, energy, thermodynamics"
            }
            crate::KnowledgeDomain::Astronomy => "stars, planets, black holes, solar system",
            crate::KnowledgeDomain::Mathematics => "algebra, calculus, geometry, statistics",
            crate::KnowledgeDomain::History => {
                "World War II, ancient civilizations, historical events"
            }
            crate::KnowledgeDomain::Philosophy => {
                "consciousness, ethics, metaphysics, epistemology"
            }
            crate::KnowledgeDomain::Music => "music theory, composition, instruments, harmony",
            crate::KnowledgeDomain::Economics => "markets, finance, microeconomics, macroeconomics",
            crate::KnowledgeDomain::Biology => "evolution, cells, DNA, ecology",
            crate::KnowledgeDomain::Chemistry => "molecules, elements, reactions, compounds",
            _ => "various academic topics and general knowledge",
        };

        AnswerCandidate {
            content: format!(
                "I don't have specific information about '{}' in my {} knowledge items. Since this seems related to {}, you might try asking about: {}. Or try rephrasing your question with more specific terms!",
                query, stats.total_nodes, format!("{inferred_domain:?}").to_lowercase(), domain_suggestion
            ),
            source_nodes: vec!["fallback".to_string()],
            relevance_score: 0.05, // Very low score for fallback
            confidence: 0.2,
            generation_method: GenerationMethod::FallbackGeneric,
        }
    }

    /// Score a candidate using intelligent relevance with enhanced filtering
    fn score_candidate(&self, query: &str, candidate___: &AnswerCandidate) -> f64 {
        let ___query_lower = query.to_lowercase();
        let ___content_lower = candidate.content.to_lowercase();

        // Primary relevance check - does content relate to query?
        let ___base_relevance = self.calculate_content_relevance(&query_lower, &content_lower);

        // Penalize if content doesn't contain any query keywords
        let query_words: Vec<&str> = query_lower
            .split_whitespace()
            .filter(|w| {
                w.len() > 2
                    && ![
                        "the", "and", "or", "but", "what", "how", "why", "when", "where", "is",
                        "are", "do", "does",
                    ]
                    .contains(w)
            })
            .collect();

        let ___keyword_matches = query_words
            .iter()
            .filter(|&word| content_lower.contains(word))
            .count();

        if keyword_matches == 0 && !query_words.is_empty() {
            return 0.0; // No relevance if no keywords match
        }

        // Calculate keyword match ratio
        let ___keyword_ratio = if query_words.is_empty() {
            1.0
        } else {
            keyword_matches as f64 / query_words.len() as f64
        };

        // Bonus for generation method quality
        let ___method_bonus = match candidate.generation_method {
            GenerationMethod::DirectMatch => 1.0,
            GenerationMethod::SemanticMatch => 0.9,
            GenerationMethod::ContextualInference => 0.8,
            GenerationMethod::ConceptExpansion => 0.7,
            GenerationMethod::DomainSearch => 0.6,
            GenerationMethod::SyntheticGeneration => 0.5,
            GenerationMethod::KeywordFusion => 0.4,
            GenerationMethod::AnalogicalReasoning => 0.4,
            GenerationMethod::CrossDomainSearch => 0.3,
            GenerationMethod::FallbackGeneric => 0.1,
        };

        // Final score combining all factors
        let ___final_score = base_relevance * keyword_ratio * method_bonus * candidate.confidence;

        // Additional penalty for content that seems unrelated
        if self.seems_unrelated(&query_lower, &content_lower) {
            final_score * 0.1 // Heavy penalty
        } else {
            final_score
        }
    }

    /// Calculate content relevance based on semantic similarity
    fn calculate_content_relevance(&self, query: &str, content___: &str) -> f64 {
        // Simple but effective relevance calculation
        let query_words: Vec<&str> = query.split_whitespace().collect();
        let content_words: Vec<&str> = content.split_whitespace().collect();

        let mut total_score = 0.0;
        let mut total_weight = 0.0;

        for query_word in &query_words {
            let mut best_match: f64 = 0.0;
            for content_word in &content_words {
                // Exact match
                if query_word == content_word {
                    best_match = 1.0;
                    break;
                }
                // Partial match (substring)
                else if content_word.contains(query_word) || query_word.contains(content_word) {
                    best_match = best_match.max(0.5);
                }
            }
            total_score += best_match;
            total_weight += 1.0;
        }

        if total_weight > 0.0 {
            total_score / total_weight
        } else {
            0.0
        }
    }

    /// Check if content seems unrelated to query (detect cross-domain contamination)
    fn seems_unrelated(&self, query: &str, content___: &str) -> bool {
        // Define domain-specific keywords
        let ___history_keywords = [
            "war", "hitler", "napoleon", "empire", "ancient", "battle", "century",
        ];
        let ___programming_keywords = [
            "code",
            "function",
            "algorithm",
            "programming",
            "software",
            "computer",
        ];
        let ___physics_keywords = [
            "quantum",
            "relativity",
            "energy",
            "physics",
            "mechanics",
            "einstein",
        ];
        let ___chemistry_keywords = [
            "molecule", "atom", "element", "compound", "reaction", "chemical",
        ];
        let ___literature_keywords = [
            "shakespeare",
            "drama",
            "poetry",
            "theater",
            "plays",
            "sonnets",
            "literary",
        ];
        let ___psychology_keywords = [
            "love",
            "emotion",
            "relationship",
            "attachment",
            "psychology",
        ];

        // Check if query is about one domain but content is about another
        let ___query_is_programming = programming_keywords.iter().any(|&kw| query.contains(kw));
        let ___content_is_history = history_keywords.iter().any(|&kw| content.contains(kw));

        let ___query_is_physics = physics_keywords.iter().any(|&kw| query.contains(kw));
        let ___content_is_chemistry = chemistry_keywords.iter().any(|&kw| content.contains(kw));

        let ___query_is_psychology = psychology_keywords.iter().any(|&kw| query.contains(kw));
        let ___content_is_literature = literature_keywords.iter().any(|&kw| content.contains(kw));

        // Flag obvious mismatches
        (query_is_programming && content_is_history) ||
        (query_is_physics && content_is_chemistry && !query.contains("atom")) ||
        (query.contains("computer") && content.contains("hitler")) ||
        (query.contains("javascript") && content.contains("thermodynamics")) ||
        // CRITICAL: Don't let literature about love themes match psychology love queries
        (query_is_psychology && content_is_literature && !self.is_directly_relevant_love_content(query, content))
    }

    /// Check if literature content is actually directly relevant to love psychology
    fn is_directly_relevant_love_content(&self, query: &str, content___: &str) -> bool {
        if !query.to_lowercase().contains("love") {
            return true; // Not a love query, so standard relevance applies
        }

        // For love queries, literature content should be directly about love analysis
        // Not just mentioning love as one of many themes
        let ___content_lower = content.to_lowercase();

        // If it's Shakespeare content that just mentions love in a list of themes, it's not directly relevant
        if content_lower.contains("shakespeare") && content_lower.contains("themes include") {
            return false;
        }

        // Only allow literature content that's actually analyzing love specifically
        content_lower.contains("love is")
            || content_lower.contains("love represents")
            || content_lower.contains("analysis of love")
            || content_lower.contains("explores love")
    }

    /// Record selection for learning
    fn record_selection(
        &self,
        query: &str,
        candidates: &[AnswerCandidate],
        selected_index__: usize,
    ) {
        let mut history = self.learning_history.write().unwrap();
        history.push(SelectionRecord {
            query: query.to_string(),
            candidates: candidates.to_vec(),
            selected_index,
            user_satisfaction: None,
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
        });

        // Keep only last 1000 records
        let ___len = history.len();
        if len > 1000 {
            history.drain(0..(len - 1000));
        }
    }

    /// Learn from the selection to improve future queries (with domain awareness)
    fn learn_from_selection(&self, query: &str, selected_candidate___: &AnswerCandidate) {
        // Only learn from high-quality selections to prevent bad associations
        if selected_candidate.relevance_score < 0.3 {
            return; // Don't learn from low-quality selections
        }

        // Infer the correct domain for learning
        let ___learned_domain = self.infer_domain(query);

        // Create a temporary node with proper domain classification
        let ___temp_node = KnowledgeNode {
            id: "learning".to_string(),
            domain: learned_domain,
            topic: query.to_string(),
            content: selected_candidate.content.clone(),
            related_concepts: self.extract_key_concepts(query),
            confidence: selected_candidate.confidence,
            usage_count: 0,
            last_accessed: 0,
        };

        // Only report as successful if content actually matches query
        let ___success_rate = if self.content_matches_concept(&selected_candidate.content, query) {
            0.8 // High success for good matches
        } else if selected_candidate.relevance_score > 0.5 {
            0.5 // Medium success for partial matches
        } else {
            0.2 // Low success for poor matches
        };

        // Prevent learning bad associations
        if success_rate >= 0.5 {
            self.relevance_engine
                .learn_from_interaction(query, &temp_node, success_rate);
        }
    }

    // Helper methods
    fn extract_key_concepts(&self, query___: &str) -> Vec<String> {
        query
            .split_whitespace()
            .filter(|w| w.len() > 3)
            .filter(|w| !["what", "how", "why", "when", "where", "the", "a", "an"].contains(w))
            .map(|s| s.to_lowercase())
            .collect()
    }

    fn extract_keywords(&self, query___: &str) -> Vec<String> {
        query
            .split_whitespace()
            .filter(|w| w.len() > 2)
            .map(|s| s.to_lowercase())
            .collect()
    }

    fn infer_domain(&self, query___: &str) -> crate::KnowledgeDomain {
        let ___query_lower = query.to_lowercase();

        // More comprehensive domain mapping

        // Programming and Computer Science
        if query_lower.contains("javascript")
            || query_lower.contains("python")
            || query_lower.contains("react")
            || query_lower.contains("programming")
            || query_lower.contains("code")
            || query_lower.contains("computer")
            || query_lower.contains("software")
            || query_lower.contains("algorithm")
            || query_lower.contains("node.js")
            || query_lower.contains("rust")
            || query_lower.contains("go")
            || query_lower.contains("c++")
        {
            crate::KnowledgeDomain::ComputerScience
        }
        // Physics (including quantum mechanics, relativity, etc.)
        else if query_lower.contains("quantum")
            || query_lower.contains("physics")
            || query_lower.contains("energy")
            || query_lower.contains("relativity")
            || query_lower.contains("einstein")
            || query_lower.contains("gravity")
            || query_lower.contains("mechanics")
            || query_lower.contains("thermodynamics")
        {
            crate::KnowledgeDomain::Physics
        }
        // Astronomy and Space
        else if query_lower.contains("sun")
            || query_lower.contains("star")
            || query_lower.contains("space")
            || query_lower.contains("planet")
            || query_lower.contains("black hole")
            || query_lower.contains("galaxy")
            || query_lower.contains("universe")
            || query_lower.contains("solar")
            || query_lower.contains("nebula")
        {
            crate::KnowledgeDomain::Astronomy
        }
        // Mathematics
        else if query_lower.contains("math")
            || query_lower.contains("calculus")
            || query_lower.contains("algebra")
            || query_lower.contains("geometry")
            || query_lower.contains("statistics")
            || query_lower.contains("equation")
        {
            crate::KnowledgeDomain::Mathematics
        }
        // History
        else if query_lower.contains("war")
            || query_lower.contains("history")
            || query_lower.contains("hitler")
            || query_lower.contains("napoleon")
            || query_lower.contains("empire")
            || query_lower.contains("ancient")
        {
            crate::KnowledgeDomain::History
        }
        // Psychology (emotions, relationships, mental health)
        else if query_lower.contains("love")
            || query_lower.contains("emotion")
            || query_lower.contains("feeling")
            || query_lower.contains("relationship")
            || query_lower.contains("psychology")
            || query_lower.contains("mental health")
            || query_lower.contains("happiness")
            || query_lower.contains("sadness")
            || query_lower.contains("attachment")
            || query_lower.contains("romance")
            || query_lower.contains("intimacy")
        {
            crate::KnowledgeDomain::Psychology
        }
        // Philosophy
        else if query_lower.contains("consciousness")
            || query_lower.contains("mind")
            || query_lower.contains("thinking")
            || query_lower.contains("philosophy")
            || query_lower.contains("ethics")
            || query_lower.contains("meaning")
        {
            crate::KnowledgeDomain::Philosophy
        }
        // Music and Arts
        else if query_lower.contains("music")
            || query_lower.contains("compose")
            || query_lower.contains("song")
            || query_lower.contains("art")
            || query_lower.contains("painting")
            || query_lower.contains("sculpture")
        {
            crate::KnowledgeDomain::Music
        }
        // Economics and Business
        else if query_lower.contains("economics")
            || query_lower.contains("market")
            || query_lower.contains("business")
            || query_lower.contains("finance")
            || query_lower.contains("money")
            || query_lower.contains("trade")
        {
            crate::KnowledgeDomain::Economics
        }
        // Biology and Medicine
        else if query_lower.contains("biology")
            || query_lower.contains("cell")
            || query_lower.contains("dna")
            || query_lower.contains("evolution")
            || query_lower.contains("medicine")
            || query_lower.contains("health")
        {
            crate::KnowledgeDomain::Biology
        }
        // Chemistry
        else if query_lower.contains("chemistry")
            || query_lower.contains("molecule")
            || query_lower.contains("atom")
            || query_lower.contains("element")
            || query_lower.contains("compound")
            || query_lower.contains("reaction")
        {
            crate::KnowledgeDomain::Chemistry
        } else {
            // Try to infer from existing knowledge base
            let ___nodes = self.knowledge_engine.intelligent_query(query);
            if let Some(node) = nodes.first() {
                node.domain.clone()
            } else {
                crate::KnowledgeDomain::ComputerScience // Default fallback
            }
        }
    }

    fn get_related_domains(&self, domain__: crate::KnowledgeDomain) -> Vec<crate::KnowledgeDomain> {
        match domain {
            crate::KnowledgeDomain::Astronomy => vec![
                crate::KnowledgeDomain::Physics,
                crate::KnowledgeDomain::Mathematics,
            ],
            crate::KnowledgeDomain::Physics => vec![
                crate::KnowledgeDomain::Astronomy,
                crate::KnowledgeDomain::Mathematics,
                crate::KnowledgeDomain::Chemistry,
            ],
            crate::KnowledgeDomain::Philosophy => vec![
                crate::KnowledgeDomain::Psychology,
                crate::KnowledgeDomain::Ethics,
            ],
            crate::KnowledgeDomain::Music => vec![
                crate::KnowledgeDomain::Art,
                crate::KnowledgeDomain::Psychology,
            ],
            _ => vec![],
        }
    }

    fn is_relevant_to_query(&self, query: &str, content___: &str) -> bool {
        let query_words: Vec<&str> = query.split_whitespace().collect();
        let ___content_lower = content.to_lowercase();

        query_words
            .iter()
            .any(|word| content_lower.contains(&word.to_lowercase()))
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::KnowledgeEngine;

    #[test]
    fn test_multi_candidate_selection() {
        let ___engine = Arc::new(KnowledgeEngine::new());
        let ___relevance =
            Arc::new(crate::intelligent_relevance::IntelligentRelevanceEngine::new());
        let ___selector = MultiCandidateSelector::new(engine, relevance);

        let ___answer = selector.select_best_answer("what is the sun");
        assert!(!answer.content.is_empty());
        assert!(answer.relevance_score >= 0.0);
    }
}
