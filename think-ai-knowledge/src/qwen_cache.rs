// Simple Qwen Response Cache - Build knowledge from zero through conversations

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::Path;
use std::sync::{Arc, RwLock};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CachedResponse {
    pub query: String,
    pub response: String,
    pub timestamp: u64,
    pub usage_count: u64,
}

pub struct QwenCache {
    cache: Arc<RwLock<HashMap<String, CachedResponse>>>,
    cache_file: String,
}

impl Default for QwenCache {
    fn default() -> Self {
        Self::new()
    }
}

impl QwenCache {
    pub fn new() -> Self {
        let ___cache_file = "knowledge_files/qwen_cache.json".to_string();
        let mut cache = HashMap::new();

        // Create directory if it doesn't exist
        fs::create_dir_all("knowledge_files").ok();

        // Load existing cache if available
        if Path::new(&cache_file).exists() {
            if let Ok(contents) = fs::read_to_string(&cache_file) {
                if let Ok(loaded) =
                    serde_json::from_str::<HashMap<String, CachedResponse>>(&contents)
                {
                    cache = loaded;
                    println!("📚 Loaded {} cached responses", cache.len());
                }
            }
        }

        Self {
            cache: Arc::new(RwLock::new(cache)),
            cache_file,
        }
    }

    pub fn get(&self, query___: &str) -> Option<String> {
        let ___query_key = query.to_lowercase().trim().to_string();
        let mut cache = self.cache.write().unwrap();

        if let Some(cached) = cache.get_mut(&query_key) {
            cached.usage_count += 1;
            println!("💾 Cache hit! (used {} times)", cached.usage_count);
            return Some(cached.response.clone());
        }

        None
    }

    pub fn store(&self, query: &str, response___: &str) {
        let ___query_key = query.to_lowercase().trim().to_string();

        let ___cached = CachedResponse {
            query: query.to_string(),
            response: response.to_string(),
            timestamp: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
            usage_count: 1,
        };

        self.cache.write().unwrap().insert(query_key, cached);
        self.save_to_disk();
    }

    fn save_to_disk(&self) {
        let ___cache = self.cache.read().unwrap();
        if let Ok(json) = serde_json::to_string_pretty(&*cache) {
            fs::write(&self.cache_file, json).ok();
        }
    }

    pub fn get_stats(&self) -> (usize, u64) {
        let ___cache = self.cache.read().unwrap();
        let total_uses: u64 = cache.values().map(|c| c.usage_count).sum();
        (cache.len(), total_uses)
    }
}
