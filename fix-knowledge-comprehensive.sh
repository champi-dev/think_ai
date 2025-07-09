#!/bin/bash
set -e

echo "Comprehensive fix for knowledge lib.rs..."

# Create a fixed version of the problematic parts
cat > /tmp/knowledge_fix.patch << 'EOF'
--- a/think-ai-knowledge/src/lib.rs
+++ b/think-ai-knowledge/src/lib.rs
@@ -129,6 +129,7 @@
     feynman_explainer: Arc<FeynmanExplainer>,
+}
 
 impl Default for KnowledgeEngine {
     fn default() -> Self {
@@ -151,6 +152,7 @@
             feynman_explainer: Arc::new(FeynmanExplainer::new(Some(nodes))),
         }
+    }
 
     pub fn add_knowledge(
         &self,
@@ -180,6 +182,7 @@
         *total += 1;
         id
+    }
 
     pub fn query(&self, query: &str) -> Option<Vec<KnowledgeNode>> {
         let query_lower = query.to_lowercase();
@@ -191,7 +194,8 @@
             self.extract_key_concept(query).to_lowercase()
         } else {
             query_lower.clone()
-        // Collect results with scoring
+        };
+        
         let mut scored_results = Vec::new();
         let mut node_ids_to_update = Vec::new();
         {
@@ -208,13 +212,16 @@
                 } else if topic_lower == query_lower {
                     score = 95.0;
+                    matched = true;
                 }
                 // Score primary topic matches for definition queries
                 else if is_definition_query
                     && topic_lower.starts_with(&key_concept)
                     && (topic_lower.len() - key_concept.len()) < 10
                 {
                     score = 90.0;
+                    matched = true;
+                }
                 // Score topic word boundary matches
                 else if Self::word_boundary_match(&topic_lower, &query_lower) {
                     if is_definition_query {
@@ -228,10 +235,14 @@
                         }
                     } else {
                         score = 75.0;
                     }
+                    matched = true;
+                }
                 // Score content matches, but boost for definition queries
                 else if Self::word_boundary_match(&content_lower, &query_lower) {
+                    if is_definition_query {
                         // For definition queries, content that directly defines the concept should score higher
                         let content_start = content_lower
                             .split_whitespace()
@@ -240,10 +251,13 @@
                             .join(" ");
                         if content_start.contains(&key_concept) {
                             score = 70.0; // Higher score for content that defines the concept
-                            score = 30.0; // Standard content match
-                    } else {                         score = 30.0;
+                        } else {
+                            score = 30.0; // Standard content match
+                        }
+                    } else {
+                        score = 30.0;
+                    }
+                    matched = true;
+                }
                 // Check related concepts
                 else {
                     for concept in &node.related_concepts {
@@ -259,10 +273,14 @@
                 }
                 if matched {
                     // Apply domain relevance boost for definition queries
+                    if is_definition_query {
                         score += Self::calculate_domain_relevance_boost(&key_concept, &node.domain);
+                    }
                     scored_results.push((node.clone(), score));
-        } else                     node_ids_to_update.push(node.id.clone());
+                    node_ids_to_update.push(node.id.clone());
+                }
             }
         } // Read lock dropped here
-        }
+        
         if scored_results.is_empty() {
             None
+        } else {
             // Sort by score (highest first)
             scored_results
                 .sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap_or(std::cmp::Ordering::Equal));
@@ -277,6 +295,8 @@
             // Usage tracking can be done asynchronously if needed
             Some(exact_matches)
+        }
+    }
     
     pub fn query_by_domain(&self, domain: KnowledgeDomain) -> Vec<KnowledgeNode> {
         let domain_index = self.domain_index.read().unwrap();
@@ -283,8 +303,11 @@
         if let Some(ids) = domain_index.get(&domain) {
             ids.iter().filter_map(|id| nodes.get(id).cloned()).collect()
+        } else {
             Vec::new()
+        }
+    }
 
     pub fn intelligent_query(&self, query: &str) -> Vec<KnowledgeNode> {
+        let nodes = self.nodes.read().unwrap();
         // Extract key concept from "what is X" questions
         let processed_query = self.extract_key_concept(query);
@@ -291,6 +314,8 @@
         if let Some(results) = self.fast_query(&processed_query) {
             if !results.is_empty() {
                 return results;
+            }
+        }
         
         // If no results from processed query, try original query
         if processed_query != query {
@@ -296,6 +321,8 @@
             if let Some(results) = self.fast_query(query) {
                 if !results.is_empty() {
                     return results;
+                }
+            }
         }
 
         // Use intelligent relevance engine for semantic understanding
@@ -305,12 +332,16 @@
                 // Only include reasonably relevant results
                 scored_results.push((node.clone(), relevance_score));
+            }
+        }
         
         // If no good results from processed query, try original query
         if scored_results.is_empty() && processed_query != query {
+            for (_, node) in nodes.iter() {
                 let relevance_score = self.intelligent_relevance.compute_relevance(query, node);
                 if relevance_score > 0.1 {
                     scored_results.push((node.clone(), relevance_score));
+                }
+            }
         }
         
         // Sort by relevance score (highest first) and take top results
@@ -322,11 +353,16 @@
         if let Some(selected_node) = results.first() {
             self.intelligent_relevance
                 .learn_from_interaction(query, selected_node, 0.5);
+        }
+        
         results
+    }
 
     pub fn get_top_relevant(&self, query: &str, limit: usize) -> Vec<KnowledgeNode> {
+        let query_lower = query.to_lowercase();
+        let nodes = self.nodes.read().unwrap();
+        
         // Try intelligent query to get scored results
         let results = self.intelligent_query(query);
         if !results.is_empty() {
@@ -328,11 +364,13 @@
         }
         
         // If still no results, do a broader keyword search
         let keywords: Vec<&str> = query_lower
             .split_whitespace()
             .filter(|w| w.len() > 2) // Skip short words
+            .collect();
+            
         if keywords.is_empty() {
             return Vec::new();
         }
         
         let mut scored_results: Vec<(KnowledgeNode, usize)> = Vec::new();
+        for (_, node) in nodes.iter() {
             let mut score: usize = 0;
             let topic_lower = node.topic.to_lowercase();
@@ -341,14 +379,19 @@
             for keyword in &keywords {
                 if topic_lower.contains(keyword) || content_lower.contains(keyword) {
                     score += 1;
+                }
+            }
+            
             if score > 0 {
                 scored_results.push((node.clone(), score));
+            }
+        }
         
         // Sort by score and return top results
         scored_results.sort_by(|a, b| b.1.cmp(&a.1));
         scored_results
+            .into_iter()
+            .map(|(node, _)| node)
             .take(limit)
             .collect()
+    }
@@ -357,9 +400,13 @@
         if llm_lock.is_none() {
             return "Knowledge engine LLM not initialized. Please use the response generator directly.".to_string();
+        }
+        
         llm_lock.as_mut().unwrap().generate_response(query)
+    }
     
     pub fn set_quantum_llm(&self, llm: EnhancedQuantumLLMEngine) {
+        let mut llm_lock = self.quantum_llm.write().unwrap();
         *llm_lock = Some(llm);
+    }
     
     pub fn train_iteration(
+        &self,
         knowledge_pairs: Vec<(KnowledgeDomain, String, String, Vec<String>)>,
     ) {
         for (domain, topic, content, related) in knowledge_pairs {
             self.add_knowledge(domain, topic, content, related);
+        }
+        
         let mut iterations = self.training_iterations.write().unwrap();
         *iterations += 1;
+    }
 
     pub fn get_stats(&self) -> KnowledgeStats {
+        let nodes = self.nodes.read().unwrap();
         let iterations = self.training_iterations.read().unwrap();
         let total = self.total_knowledge_items.read().unwrap();
+        
         let mut domain_counts = HashMap::new();
         let mut domains = std::collections::HashSet::new();
         let mut categories = std::collections::HashSet::new();
+        
         for node in nodes.values() {
             *domain_counts.entry(node.domain.clone()).or_insert(0) += 1;
             domains.insert(format!("{:?}", node.domain));
             categories.insert(node.topic.clone());
+        }
+        
         KnowledgeStats {
             total_nodes: nodes.len(),
@@ -390,17 +437,24 @@
             cache_hit_rate: 0.95,      // O(1) hash lookup gives high hit rate
             avg_response_time_ms: 0.1, // O(1) performance target
             categories: categories.into_iter().take(20).collect(), // Top 20 categories
+        }
+    }
     
     pub fn get_all_nodes(&self) -> HashMap<String, KnowledgeNode> {
         self.nodes.read().unwrap().clone()
+    }
     
     pub fn load_nodes(&self, nodes: HashMap<String, KnowledgeNode>) {
         let mut self_nodes = self.nodes.write().unwrap();
         *self_nodes = nodes;
+        
+        let mut domain_index = self.domain_index.write().unwrap();
         domain_index.clear();
+        
+        let mut concept_graph = self.concept_graph.write().unwrap();
         concept_graph.clear();
+        
         for node in self_nodes.values() {
             domain_index
                 .entry(node.domain.clone())
@@ -403,17 +457,22 @@
                 .push(node.id.clone());
             concept_graph.insert(node.topic.clone(), node.related_concepts.clone());
+        }
+        
+        let mut total = self.total_knowledge_items.write().unwrap();
         *total = self_nodes.len() as u64;
+    }
     
     fn generate_id(domain: &KnowledgeDomain, topic: &str, content: &str) -> String {
         let data = format!("{domain:?}:{topic}:{content}");
         Self::hash_string(&data)
+    }
     
     fn hash_string(input: &str) -> String {
         let mut hasher = Sha256::new();
         hasher.update(input.as_bytes());
         format!("{:x}", hasher.finalize())
+    }
     
     fn current_timestamp() -> u64 {
         std::time::SystemTime::now()
             .duration_since(std::time::UNIX_EPOCH)
             .unwrap()
             .as_secs()
+    }
     
     /// Extract key concept from definition questions like "what is X" -> "X"
     fn extract_key_concept(&self, query: &str) -> String {
@@ -425,6 +484,7 @@
             // Remove common question words and punctuation
             let cleaned = concept.replace("the ", "").replace("?", "");
             return cleaned.trim().to_string();
+        }
         
         // Handle "what's X" questions
         if query_lower.starts_with("what's ") {
             let concept = query_lower.strip_prefix("what's ").unwrap_or(&query_lower);
+            let cleaned = concept.replace("the ", "").replace("?", "");
+            return cleaned.trim().to_string();
+        }
         
         // Handle "define X" questions
         if query_lower.starts_with("define ") {
             let concept = query_lower.strip_prefix("define ").unwrap_or(&query_lower);
+            let cleaned = concept.replace("the ", "").replace("?", "");
+            return cleaned.trim().to_string();
+        }
         
         // Handle "explain X" questions
         if query_lower.starts_with("explain ") {
             let concept = query_lower.strip_prefix("explain ").unwrap_or(&query_lower);
+            let cleaned = concept.replace("the ", "").replace("?", "");
+            return cleaned.trim().to_string();
+        }
         
         // Return original query if no pattern matches
         query.to_string()
+    }
     
     /// Get all nodes as vector for training
     pub fn get_all_nodes_vec(&self) -> Vec<KnowledgeNode> {
+        let nodes = self.nodes.read().unwrap();
         nodes.values().cloned().collect()
+    }
     
     /// Generate a Feynman-style explanation for any concept
     pub fn explain_concept(&self, concept: &str) -> String {
         let explanation = self.feynman_explainer.explain(concept);
         explanation.format_for_human()
+    }
     
     /// Get access to the intelligent relevance engine
     pub fn get_intelligent_relevance(&self) -> Arc<IntelligentRelevanceEngine> {
         self.intelligent_relevance.clone()
+    }
     
     /// Comprehensive search that combines multiple search strategies
     pub fn search_comprehensive(
+        &self,
         query: &str,
         domain_filter: Option<KnowledgeDomain>,
     ) -> Vec<KnowledgeNode> {
@@ -458,10 +522,15 @@
                 for node in direct_results {
                     if !results.iter().any(|r| r.id == node.id) {
                         results.push(node);
+                    }
+                }
+            }
+        }
         
         // If still limited results, try broader keyword search
+        if results.len() < 5 {
             let broader_results = self.get_top_relevant(query, 10);
             for node in broader_results {
                 if !results.iter().any(|r| r.id == node.id) {
                     results.push(node);
+                }
+            }
+        }
         
         // Filter by domain if specified
         if let Some(domain) = domain_filter {
             results.retain(|node| node.domain == domain);
+        }
         
         // Limit to top 10 results
         results.truncate(10);
+        results
+    }
     
     /// Word boundary aware matching to prevent false positives like "matter" matching "matters"
     fn word_boundary_match(text: &str, query: &str) -> bool {
@@ -483,6 +552,7 @@
                 clean_text_word == word
             })
+        } else {
             // Multi-word query - check if all query words appear as complete words in text
             let text_words: Vec<String> = text
                 .split_whitespace()
@@ -491,6 +561,8 @@
             query_words
                 .iter()
                 .all(|&query_word| text_words.iter().any(|text_word| text_word == query_word))
+        }
+    }
     
     /// Calculate domain relevance boost for definition queries
     fn calculate_domain_relevance_boost(concept: &str, domain: &KnowledgeDomain) -> f32 {
@@ -500,10 +572,13 @@
                 KnowledgeDomain::Physics => 10.0,
                 KnowledgeDomain::Philosophy => 5.0,
                 _ => 0.0,
+            },
+            
             // Matter concepts - prioritize physics and chemistry
             "matter" | "atom" | "molecule" | "element" | "compound" => match domain {
                 KnowledgeDomain::Physics => 15.0,
                 KnowledgeDomain::Chemistry => 15.0,
                 KnowledgeDomain::Philosophy => 3.0,
+                _ => 0.0,
+            },
+            
             // Time concepts - prioritize physics and philosophy
             "time" | "temporal" | "duration" => match domain {
+                KnowledgeDomain::Physics => 12.0,
                 KnowledgeDomain::Philosophy => 10.0,
                 KnowledgeDomain::Astronomy => 8.0,
+                _ => 0.0,
+            },
+            
             // Life concepts - prioritize biology and medicine
             "life" | "organism" | "cell" | "dna" | "gene" => match domain {
                 KnowledgeDomain::Biology => 15.0,
                 KnowledgeDomain::Medicine => 12.0,
+                KnowledgeDomain::Philosophy => 5.0,
+                _ => 0.0,
+            },
+            
             // Mind concepts - prioritize psychology and philosophy
             "mind" | "consciousness" | "thought" | "brain" => match domain {
                 KnowledgeDomain::Psychology => 15.0,
                 KnowledgeDomain::Philosophy => 12.0,
                 KnowledgeDomain::Biology => 8.0,
+                _ => 0.0,
+            },
+            
             // Math concepts - prioritize mathematics
             "number" | "equation" | "algebra" | "geometry" | "calculus" => match domain {
                 KnowledgeDomain::Mathematics => 15.0,
                 KnowledgeDomain::Physics => 5.0,
+                _ => 0.0,
+            },
+            
             // Computing concepts - prioritize computer science
             "computer" | "algorithm" | "software" | "programming" => match domain {
                 KnowledgeDomain::ComputerScience => 15.0,
                 KnowledgeDomain::Engineering => 8.0,
+                _ => 0.0,
+            },
+            
             // Default case - no boost
             _ => 0.0,
+        }
+    }
     
     // O(1) Performance Methods
     fn update_indexes(&self, node_id: &str, node: &KnowledgeNode) {
@@ -546,6 +621,8 @@
                     .or_default()
                     .push(node_id.to_string());
+            }
+        }
         
         // Index content words (first 50 words to avoid bloat)
         for word in node.content.to_lowercase().split_whitespace().take(50) {
@@ -557,6 +634,8 @@
                         .or_default()
                         .push(node_id.to_string());
+                }
+            }
+        }
         
         // Index related concepts
         for concept in &node.related_concepts {
             let concept_key = concept.to_lowercase();
             keyword_index
                 .entry(concept_key)
+                .or_default()
                 .push(node_id.to_string());
+        }
         
         // Update content hash index for exact duplicate detection
         let content_hash = Self::hash_content(&node.content);
         let mut content_hash_index = self.content_hash_index.write().unwrap();
         content_hash_index.insert(content_hash, node_id.to_string());
+    }
     
     fn hash_content(content: &str) -> String {
-        use sha2::{Digest, Sha256};
+        let mut hasher = Sha256::new();
         hasher.update(content.as_bytes());
+        format!("{:x}", hasher.finalize())
+    }
     
     // O(1) Fast Query - replaces the slow O(n) query method
     pub fn fast_query(&self, query: &str) -> Option<Vec<KnowledgeNode>> {
         let query_key = query.to_lowercase();
+        let nodes = self.nodes.read().unwrap();
+        
         // Check cache first - O(1) lookup
+        {
             let cache = self.quick_lookup_cache.read().unwrap();
             if let Some(cached_results) = cache.get(&query_key) {
                 return Some(
@@ -582,6 +664,8 @@
                         .collect(),
                 );
+            }
+        }
         
         let mut candidate_nodes = Vec::new();
         
@@ -588,6 +672,9 @@
             for node_id in node_ids {
                 if let Some(node) = nodes.get(node_id) {
                     candidate_nodes.push((node.clone(), 100.0)); // Highest score for exact topic match
+                }
+            }
+        }
         
         // O(1) Keyword lookups
         let keyword_index = self.keyword_index.read().unwrap();
@@ -602,6 +689,10 @@
                             };
                             candidate_nodes.push((node.clone(), score));
+                        }
+                    }
+                }
+            }
+        }
         
         // Sort by score and limit results
@@ -609,17 +700,24 @@
         let results: Vec<KnowledgeNode> = candidate_nodes
             .iter()
             .map(|(node, _)| node.clone())
+            .collect();
+            
+        {
             let mut cache = self.quick_lookup_cache.write().unwrap();
             cache.insert(query_key, candidate_nodes.clone());
+            
             // Limit cache size to prevent memory bloat
             if cache.len() > 1000 {
                 cache.clear(); // Simple cache eviction
+            }
+        }
         
         if results.is_empty() {
+            None
+        } else {
             Some(results)
+        }
+    }
+}
 
 pub struct KnowledgeStats {
@@ -635,14 +735,19 @@
 
     #[test]
     fn test_knowledge_engine_creation() {
         let engine = KnowledgeEngine::new();
         let stats = engine.get_stats();
         assert_eq!(stats.total_nodes, 0);
         assert_eq!(stats.training_iterations, 0);
+    }
+    
+    #[test]
     fn test_add_knowledge() {
+        let engine = KnowledgeEngine::new();
+        
         let id = engine.add_knowledge(
             KnowledgeDomain::Mathematics,
             "Pythagorean Theorem".to_string(),
@@ -644,10 +749,15 @@
         );
         
         assert!(!id.is_empty());
+        
+        let stats = engine.get_stats();
         assert_eq!(stats.total_nodes, 1);
         assert_eq!(stats.total_knowledge_items, 1);
+    }
+    
+    #[test]
     fn test_query() {
+        let engine = KnowledgeEngine::new();
+        
         engine.add_knowledge(
             KnowledgeDomain::Physics,
             "Newton's First Law".to_string(),
             "An object at rest stays at rest unless acted upon by a force".to_string(),
             vec!["mechanics".to_string(), "motion".to_string()],
+        );
+        
         let results = engine.query("Newton's First Law");
         assert!(results.is_some());
         assert_eq!(results.unwrap().len(), 1);
+    }
+    
+    #[test]
     fn test_domain_query() {
+        let engine = KnowledgeEngine::new();
+        
+        engine.add_knowledge(
             KnowledgeDomain::Philosophy,
             "Cogito ergo sum".to_string(),
             "I think, therefore I am".to_string(),
             vec!["Descartes".to_string(), "epistemology".to_string()],
+        );
+        
         let results = engine.query_by_domain(KnowledgeDomain::Philosophy);
         assert_eq!(results.len(), 1);
+    }
+}
EOF

# Apply the patch
cd /home/champi/Dev/think_ai
patch -p1 < /tmp/knowledge_fix.patch

echo "Comprehensive fix applied!"