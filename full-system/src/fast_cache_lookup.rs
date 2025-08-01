use std::collections::HashMap;
use std::sync::Arc;
use std::path::Path;
use tokio::sync::RwLock;
use serde::{Deserialize, Serialize};
use anyhow::Result;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PrecomputedResponse {
    pub query: String,
    pub response: String,
    pub timestamp: f64,
    pub normalized_query: String,
}

pub struct FastCacheLookup {
    // Direct hash lookup for exact matches
    exact_cache: Arc<RwLock<HashMap<String, String>>>,
    // Fuzzy matching cache for similar queries
    fuzzy_cache: Arc<RwLock<Vec<(String, String)>>>,
    // Precomputed responses from disk
    precomputed: Arc<RwLock<HashMap<String, PrecomputedResponse>>>,
}

impl FastCacheLookup {
    pub fn new() -> Self {
        Self {
            exact_cache: Arc::new(RwLock::new(HashMap::new())),
            fuzzy_cache: Arc::new(RwLock::new(Vec::new())),
            precomputed: Arc::new(RwLock::new(HashMap::new())),
        }
    }

    pub async fn load_precomputed_cache(&self, cache_dir: &Path) -> Result<usize> {
        let mut loaded = 0;
        let mut precomputed = self.precomputed.write().await;
        
        if cache_dir.exists() {
            for entry in std::fs::read_dir(cache_dir)? {
                let entry = entry?;
                let path = entry.path();
                
                if path.extension().and_then(|s| s.to_str()) == Some("json") {
                    if let Ok(content) = std::fs::read_to_string(&path) {
                        if let Ok(response) = serde_json::from_str::<PrecomputedResponse>(&content) {
                            let normalized = Self::normalize_query(&response.query);
                            precomputed.insert(normalized.clone(), response.clone());
                            loaded += 1;
                        }
                    }
                }
            }
        }
        
        tracing::info!("Loaded {} precomputed responses into fast cache", loaded);
        Ok(loaded)
    }

    pub async fn lookup(&self, query: &str) -> Option<String> {
        let normalized = Self::normalize_query(query);
        
        // 1. Check exact match in memory
        {
            let exact = self.exact_cache.read().await;
            if let Some(response) = exact.get(&normalized) {
                tracing::debug!("Fast cache hit (exact): {}", query);
                return Some(response.clone());
            }
        }
        
        // 2. Check precomputed responses
        {
            let precomputed = self.precomputed.read().await;
            if let Some(response) = precomputed.get(&normalized) {
                tracing::debug!("Fast cache hit (precomputed): {}", query);
                // Add to exact cache for next time
                self.exact_cache.write().await.insert(normalized.clone(), response.response.clone());
                return Some(response.response.clone());
            }
        }
        
        // 3. Fuzzy match for similar queries
        let query_words = Self::tokenize(&normalized);
        if query_words.len() > 0 {
            let fuzzy = self.fuzzy_cache.read().await;
            for (cached_query, cached_response) in fuzzy.iter() {
                if Self::is_similar(&query_words, cached_query) {
                    tracing::debug!("Fast cache hit (fuzzy): {} -> {}", query, cached_query);
                    return Some(cached_response.clone());
                }
            }
        }
        
        None
    }

    pub async fn insert(&self, query: &str, response: String) {
        let normalized = Self::normalize_query(query);
        
        // Add to exact cache
        self.exact_cache.write().await.insert(normalized.clone(), response.clone());
        
        // Add to fuzzy cache if not too large
        let mut fuzzy = self.fuzzy_cache.write().await;
        if fuzzy.len() < 10000 { // Limit fuzzy cache size
            fuzzy.push((normalized, response));
        }
    }

    fn normalize_query(query: &str) -> String {
        query
            .to_lowercase()
            .trim()
            .chars()
            .filter(|c| c.is_alphanumeric() || c.is_whitespace())
            .collect::<String>()
            .split_whitespace()
            .collect::<Vec<_>>()
            .join(" ")
    }

    fn tokenize(text: &str) -> Vec<&str> {
        text.split_whitespace().collect()
    }

    fn is_similar(words1: &[&str], text2: &str) -> bool {
        let words2 = Self::tokenize(text2);
        
        // Check if at least 80% of words match
        if words1.len() == 0 || words2.len() == 0 {
            return false;
        }
        
        let matching_words = words1.iter()
            .filter(|w| words2.contains(w))
            .count();
        
        let similarity = matching_words as f32 / words1.len().min(words2.len()) as f32;
        similarity >= 0.8
    }
}

// Note: ResponseCache integration would go here if needed
// For now, FastCacheLookup is used as a standalone component