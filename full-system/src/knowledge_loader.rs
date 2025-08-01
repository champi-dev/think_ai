use std::collections::HashMap;
use std::fs;
use std::path::Path;
use serde::{Deserialize, Serialize};
use anyhow::Result;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeEntry {
    pub topic: String,
    pub content: String,
    pub metadata: KnowledgeMetadata,
    pub related_concepts: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeMetadata {
    pub conversational_patterns: Vec<String>,
    pub evaluation_score: f32,
    pub source: String,
    pub generated_at: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DomainKnowledge {
    pub domain: String,
    pub entries: Vec<KnowledgeEntry>,
}

#[derive(Debug, Clone)]
pub struct KnowledgeBase {
    pub domains: HashMap<String, DomainKnowledge>,
    pub topic_index: HashMap<String, Vec<(String, usize)>>, // topic -> (domain, entry_index)
    pub response_cache: HashMap<String, String>,
}

impl KnowledgeBase {
    pub fn new() -> Self {
        Self {
            domains: HashMap::new(),
            topic_index: HashMap::new(),
            response_cache: HashMap::new(),
        }
    }

    pub fn load_from_directory(dir_path: &str) -> Result<Self> {
        let mut kb = Self::new();
        let knowledge_dir = Path::new(dir_path);

        // Load all JSON files from knowledge directory
        for entry in fs::read_dir(knowledge_dir)? {
            let entry = entry?;
            let path = entry.path();
            
            if path.extension().and_then(|s| s.to_str()) == Some("json") {
                let filename = path.file_name().unwrap().to_str().unwrap();
                if filename == "knowledge_index.json" {
                    continue;
                }

                let content = fs::read_to_string(&path)?;
                if let Ok(domain_knowledge) = serde_json::from_str::<DomainKnowledge>(&content) {
                    // Index all topics
                    for (idx, entry) in domain_knowledge.entries.iter().enumerate() {
                        kb.topic_index.entry(entry.topic.clone())
                            .or_insert_with(Vec::new)
                            .push((domain_knowledge.domain.clone(), idx));
                        
                        // Add conversational patterns to cache
                        for pattern in &entry.metadata.conversational_patterns {
                            kb.response_cache.insert(
                                entry.topic.to_lowercase(),
                                pattern.clone()
                            );
                        }
                    }
                    
                    kb.domains.insert(domain_knowledge.domain.clone(), domain_knowledge);
                }
            }
        }

        // Load response cache if it exists
        let cache_path = Path::new("./cache/response_cache.json");
        if cache_path.exists() {
            if let Ok(cache_content) = fs::read_to_string(cache_path) {
                if let Ok(cache) = serde_json::from_str::<HashMap<String, serde_json::Value>>(&cache_content) {
                    for (key, value) in cache {
                        if let Some(response) = value.get("response").and_then(|v| v.as_str()) {
                            kb.response_cache.insert(key, response.to_string());
                        }
                    }
                }
            }
        }

        Ok(kb)
    }

    pub fn find_knowledge(&self, query: &str) -> Option<String> {
        let query_lower = query.to_lowercase();
        
        // First, check direct topic match
        for (topic, locations) in &self.topic_index {
            if query_lower.contains(&topic.to_lowercase()) {
                if let Some((domain, idx)) = locations.first() {
                    if let Some(domain_knowledge) = self.domains.get(domain) {
                        if let Some(entry) = domain_knowledge.entries.get(*idx) {
                            // Return a conversational pattern
                            if let Some(pattern) = entry.metadata.conversational_patterns.first() {
                                return Some(pattern.clone());
                            }
                        }
                    }
                }
            }
        }

        // Check cache for similar queries
        for (key, response) in &self.response_cache {
            if query_lower.contains(key) || key.contains(&query_lower) {
                return Some(response.clone());
            }
        }

        // Look for related concepts
        let keywords: Vec<&str> = query_lower.split_whitespace().collect();
        let mut best_match: Option<(String, usize)> = None;
        
        for (domain_name, domain) in &self.domains {
            for entry in &domain.entries {
                let mut match_count = 0;
                
                // Check topic
                if keywords.iter().any(|kw| entry.topic.to_lowercase().contains(kw)) {
                    match_count += 2;
                }
                
                // Check content
                for keyword in &keywords {
                    if entry.content.to_lowercase().contains(keyword) {
                        match_count += 1;
                    }
                }
                
                // Check related concepts
                for concept in &entry.related_concepts {
                    if keywords.iter().any(|kw| concept.to_lowercase().contains(kw)) {
                        match_count += 1;
                    }
                }
                
                if match_count > 0 {
                    if best_match.is_none() || match_count > best_match.as_ref().unwrap().1 {
                        best_match = Some((entry.metadata.conversational_patterns[0].clone(), match_count));
                    }
                }
            }
        }

        best_match.map(|(response, _)| response)
    }

    pub fn get_conversational_response(&self, query: &str) -> String {
        if let Some(knowledge) = self.find_knowledge(query) {
            // Make response more conversational and direct
            let response = knowledge
                .replace("This relates to the fundamental concept that", "Here's the key point:")
                .replace("Additionally,", "Also,")
                .replace("It encompasses", "This includes")
                .replace("Understanding", "Knowing about")
                .replace("Theories range from", "There are different views like");
            
            // Make it more direct and useful
            if response.len() > 300 {
                let sentences: Vec<&str> = response.split(". ").collect();
                let key_sentences: Vec<&str> = sentences.iter()
                    .take(3)
                    .cloned()
                    .collect();
                format!("{}. In practical terms, this helps you understand the core concepts better.", key_sentences.join(". "))
            } else {
                response
            }
        } else {
            // Fallback response that's more helpful
            format!("I'd be happy to help with {}. Could you tell me more specifically what you'd like to know? I have extensive knowledge about science, technology, philosophy, and many other topics.", query)
        }
    }
}

// Function to integrate with existing code
pub fn enhance_response_with_knowledge(query: &str, kb: &KnowledgeBase) -> String {
    kb.get_conversational_response(query)
}