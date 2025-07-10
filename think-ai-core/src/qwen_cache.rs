use chrono::{DateTime, Duration, Utc};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, HashMap};
use std::sync::{Arc, RwLock};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CachedEntry {
    pub key: String,
    pub value: Vec<f32>, // Embedding vector
    pub metadata: EntryMetadata,
    pub access_pattern: AccessPattern,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EntryMetadata {
    pub source: String,
    pub category: String,
    pub confidence: f32,
    pub created_at: DateTime<Utc>,
    pub last_updated: DateTime<Utc>,
    pub version: u32,
    pub dependencies: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AccessPattern {
    pub access_count: u64,
    pub last_accessed: DateTime<Utc>,
    pub access_frequency: f32, // Accesses per hour
    pub query_patterns: Vec<String>,
    pub performance_metrics: PerformanceMetrics,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PerformanceMetrics {
    pub avg_retrieval_time_us: u64,
    pub cache_hit_rate: f32,
    pub memory_usage_bytes: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct QwenCacheConfig {
    pub max_entries: usize,
    pub ttl_seconds: i64,
    pub eviction_policy: EvictionPolicy,
    pub compression_enabled: bool,
    pub prefetch_enabled: bool,
    pub similarity_threshold: f32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum EvictionPolicy {
    LRU,      // Least Recently Used
    LFU,      // Least Frequently Used
    FIFO,     // First In First Out
    Adaptive, // ML-based adaptive eviction
}

pub struct QwenKnowledgeCache {
    entries: Arc<RwLock<HashMap<String, CachedEntry>>>,
    index: Arc<RwLock<BTreeMap<DateTime<Utc>, String>>>, // For time-based operations
    embedding_index: Arc<RwLock<HashMap<String, Vec<f32>>>>, // For similarity search
    config: QwenCacheConfig,
    stats: Arc<RwLock<CacheStatistics>>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CacheStatistics {
    pub total_entries: usize,
    pub total_hits: u64,
    pub total_misses: u64,
    pub avg_retrieval_time_us: u64,
    pub memory_usage_mb: f32,
    pub evictions: u64,
}

impl QwenKnowledgeCache {
    pub fn new(config: QwenCacheConfig) -> Self {
        Self {
            entries: Arc::new(RwLock::new(HashMap::with_capacity(config.max_entries))),
            index: Arc::new(RwLock::new(BTreeMap::new())),
            embedding_index: Arc::new(RwLock::new(HashMap::new())),
            config,
            stats: Arc::new(RwLock::new(CacheStatistics {
                total_entries: 0,
                total_hits: 0,
                total_misses: 0,
                avg_retrieval_time_us: 0,
                memory_usage_mb: 0.0_f32,
                evictions: 0,
            })),
        }
    }

    pub fn store(
        &self,
        key: String,
        embedding: Vec<f32>,
        category: String,
        source: String,
        confidence: f32,
    ) -> Result<(), String> {
        let start = std::time::Instant::now();

        let entry = CachedEntry {
            key: key.clone(),
            value: embedding.clone(),
            metadata: EntryMetadata {
                source,
                category,
                confidence,
                created_at: Utc::now(),
                last_updated: Utc::now(),
                version: 1,
                dependencies: Vec::new(),
            },
            access_pattern: AccessPattern {
                access_count: 0,
                last_accessed: Utc::now(),
                access_frequency: 0.0_f32,
                query_patterns: Vec::new(),
                performance_metrics: PerformanceMetrics {
                    avg_retrieval_time_us: 0,
                    cache_hit_rate: 0.0_f32,
                    memory_usage_bytes: embedding.len() * 4,
                },
            },
        };

        // Check if we need to evict
        {
            let entries = self.entries.read().unwrap();
            if entries.len() >= self.config.max_entries {
                drop(entries);
                self.evict_entry()?;
            }
        }

        // Store the entry
        {
            let mut entries = self.entries.write().unwrap();
            let mut index = self.index.write().unwrap();
            let mut emb_index = self.embedding_index.write().unwrap();

            index.insert(entry.metadata.created_at, key.clone());
            emb_index.insert(key.clone(), embedding);
            entries.insert(key, entry);

            let mut stats = self.stats.write().unwrap();
            stats.total_entries = entries.len();
        }

        let elapsed = start.elapsed().as_micros() as u64;
        self.update_stats(elapsed, true);

        Ok(())
    }

    pub fn retrieve(&self, key: &str) -> Option<(Vec<f32>, EntryMetadata)> {
        let start = std::time::Instant::now();

        let result = {
            let mut entries = self.entries.write().unwrap();
            if let Some(entry) = entries.get_mut(key) {
                // Update access pattern
                entry.access_pattern.access_count += 1;
                entry.access_pattern.last_accessed = Utc::now();

                // Calculate access frequency
                let age_hours =
                    (Utc::now() - entry.metadata.created_at).num_seconds() as f32 / 3600.0;
                if age_hours > 0.0_f32 {
                    entry.access_pattern.access_frequency =
                        entry.access_pattern.access_count as f32 / age_hours;
                }

                Some((entry.value.clone(), entry.metadata.clone()))
            } else {
                None
            }
        };

        let elapsed = start.elapsed().as_micros() as u64;
        self.update_stats(elapsed, result.is_some());

        result
    }

    pub fn find_similar(
        &self,
        embedding: &[f32],
        threshold: f32,
    ) -> Vec<(String, f32, EntryMetadata)> {
        let emb_index = self.embedding_index.read().unwrap();
        let entries = self.entries.read().unwrap();

        let mut results = Vec::new();

        for (key, cached_embedding) in emb_index.iter() {
            let similarity = self.cosine_similarity(embedding, cached_embedding);
            if similarity >= threshold {
                if let Some(entry) = entries.get(key) {
                    results.push((key.clone(), similarity, entry.metadata.clone()));
                }
            }
        }

        // Sort by similarity descending
        results.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
        results
    }

    fn cosine_similarity(&self, a: &[f32], b: &[f32]) -> f32 {
        if a.len() != b.len() {
            return 0.0_f32;
        }

        let dot_product: f32 = a.iter().zip(b.iter()).map(|(x, y)| x * y).sum();
        let norm_a: f32 = a.iter().map(|x| x * x).sum::<f32>().sqrt();
        let norm_b: f32 = b.iter().map(|x| x * x).sum::<f32>().sqrt();

        if norm_a * norm_b > 0.0_f32 {
            dot_product / (norm_a * norm_b)
        } else {
            0.0_f32
        }
    }

    fn evict_entry(&self) -> Result<(), String> {
        match self.config.eviction_policy {
            EvictionPolicy::LRU => self.evict_lru(),
            EvictionPolicy::LFU => self.evict_lfu(),
            EvictionPolicy::FIFO => self.evict_fifo(),
            EvictionPolicy::Adaptive => self.evict_adaptive(),
        }
    }

    fn evict_lru(&self) -> Result<(), String> {
        let mut entries = self.entries.write().unwrap();
        let mut index = self.index.write().unwrap();
        let mut emb_index = self.embedding_index.write().unwrap();

        // Find least recently accessed entry
        let oldest_key = entries
            .iter()
            .min_by_key(|(_, entry)| entry.access_pattern.last_accessed)
            .map(|(key, _)| key.clone());

        if let Some(key) = oldest_key {
            if let Some(entry) = entries.remove(&key) {
                index.retain(|_, k| k != &key);
                emb_index.remove(&key);

                let mut stats = self.stats.write().unwrap();
                stats.evictions += 1;
                stats.total_entries = entries.len();
            }
        }

        Ok(())
    }

    fn evict_lfu(&self) -> Result<(), String> {
        let mut entries = self.entries.write().unwrap();
        let mut index = self.index.write().unwrap();
        let mut emb_index = self.embedding_index.write().unwrap();

        // Find least frequently accessed entry
        let least_freq_key = entries
            .iter()
            .min_by_key(|(_, entry)| (entry.access_pattern.access_frequency * 1000.0) as u64)
            .map(|(key, _)| key.clone());

        if let Some(key) = least_freq_key {
            if let Some(entry) = entries.remove(&key) {
                index.retain(|_, k| k != &key);
                emb_index.remove(&key);

                let mut stats = self.stats.write().unwrap();
                stats.evictions += 1;
                stats.total_entries = entries.len();
            }
        }

        Ok(())
    }

    fn evict_fifo(&self) -> Result<(), String> {
        let mut entries = self.entries.write().unwrap();
        let mut index = self.index.write().unwrap();
        let mut emb_index = self.embedding_index.write().unwrap();

        // Find oldest entry by creation time
        if let Some((time, key)) = index.iter().next() {
            let key = key.clone();
            let time = time.clone();

            entries.remove(&key);
            index.remove(&time);
            emb_index.remove(&key);

            let mut stats = self.stats.write().unwrap();
            stats.evictions += 1;
            stats.total_entries = entries.len();
        }

        Ok(())
    }

    fn evict_adaptive(&self) -> Result<(), String> {
        // Adaptive eviction based on multiple factors
        let mut entries = self.entries.write().unwrap();
        let mut index = self.index.write().unwrap();
        let mut emb_index = self.embedding_index.write().unwrap();

        // Score each entry based on recency, frequency, and confidence
        let scored_key = entries
            .iter()
            .map(|(key, entry)| {
                let recency_score =
                    (Utc::now() - entry.access_pattern.last_accessed).num_seconds() as f32;
                let frequency_score = 1.0_f32 / (entry.access_pattern.access_frequency + 0.1_f32);
                let confidence_penalty = 1.0_f32 - entry.metadata.confidence;
                let combined_score = recency_score * frequency_score * confidence_penalty;
                (key.clone(), combined_score)
            })
            .max_by(|a, b| a.1.partial_cmp(&b.1).unwrap())
            .map(|(key, _)| key);

        if let Some(key) = scored_key {
            if let Some(entry) = entries.remove(&key) {
                index.retain(|_, k| k != &key);
                emb_index.remove(&key);

                let mut stats = self.stats.write().unwrap();
                stats.evictions += 1;
                stats.total_entries = entries.len();
            }
        }

        Ok(())
    }

    fn update_stats(&self, retrieval_time_us: u64, hit: bool) {
        let mut stats = self.stats.write().unwrap();
        if hit {
            stats.total_hits += 1;
        } else {
            stats.total_misses += 1;
        }

        // Update average retrieval time
        let total_ops = stats.total_hits + stats.total_misses;
        stats.avg_retrieval_time_us =
            ((stats.avg_retrieval_time_us * (total_ops - 1)) + retrieval_time_us) / total_ops;

        // Estimate memory usage
        let entries = self.entries.read().unwrap();
        let total_bytes: usize = entries
            .values()
            .map(|e| e.value.len() * 4 + 200) // 4 bytes per f32 + metadata overhead
            .sum();
        stats.memory_usage_mb = total_bytes as f32 / (1024.0_f32 * 1024.0_f32);
    }

    pub fn get_statistics(&self) -> CacheStatistics {
        self.stats.read().unwrap().clone()
    }

    pub fn clear_expired(&self) {
        let cutoff = Utc::now() - Duration::seconds(self.config.ttl_seconds);
        let mut entries = self.entries.write().unwrap();
        let mut index = self.index.write().unwrap();
        let mut emb_index = self.embedding_index.write().unwrap();

        let expired_keys: Vec<String> = entries
            .iter()
            .filter(|(_, entry)| entry.access_pattern.last_accessed < cutoff)
            .map(|(key, _)| key.clone())
            .collect();

        for key in expired_keys {
            if let Some(entry) = entries.remove(&key) {
                index.retain(|_, k| k != &key);
                emb_index.remove(&key);
            }
        }

        let mut stats = self.stats.write().unwrap();
        stats.total_entries = entries.len();
    }

    pub fn export_cache(&self) -> Result<String, String> {
        let entries = self.entries.read().unwrap();
        serde_json::to_string_pretty(&*entries)
            .map_err(|e| format!("Failed to export cache: {}", e))
    }

    pub fn import_cache(&self, data: &str) -> Result<(), String> {
        let imported: HashMap<String, CachedEntry> =
            serde_json::from_str(data).map_err(|e| format!("Failed to import cache: {}", e))?;

        let mut entries = self.entries.write().unwrap();
        let mut index = self.index.write().unwrap();
        let mut emb_index = self.embedding_index.write().unwrap();

        for (key, entry) in imported {
            index.insert(entry.metadata.created_at, key.clone());
            emb_index.insert(key.clone(), entry.value.clone());
            entries.insert(key, entry);
        }

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cache_operations() {
        let config = QwenCacheConfig {
            max_entries: 100,
            ttl_seconds: 3600,
            eviction_policy: EvictionPolicy::LRU,
            compression_enabled: false,
            prefetch_enabled: false,
            similarity_threshold: 0.8_f32,
        };

        let cache = QwenKnowledgeCache::new(config);

        // Test store and retrieve
        let embedding = vec![0.1_f32, 0.2_f32, 0.3_f32, 0.4_f32, 0.5_f32];
        cache
            .store(
                "test_key".to_string(),
                embedding.clone(),
                "test_category".to_string(),
                "test_source".to_string(),
                0.95_f32,
            )
            .unwrap();

        let result = cache.retrieve("test_key");
        assert!(result.is_some());

        let (retrieved_embedding, metadata) = result.unwrap();
        assert_eq!(retrieved_embedding, embedding);
        assert_eq!(metadata.category, "test_category");
        assert_eq!(metadata.confidence, 0.95_f32);
    }

    #[test]
    fn test_similarity_search() {
        let config = QwenCacheConfig {
            max_entries: 100,
            ttl_seconds: 3600,
            eviction_policy: EvictionPolicy::LRU,
            compression_enabled: false,
            prefetch_enabled: false,
            similarity_threshold: 0.8_f32,
        };

        let cache = QwenKnowledgeCache::new(config);

        // Store multiple embeddings
        cache
            .store(
                "key1".to_string(),
                vec![1.0_f32, 0.0_f32, 0.0_f32],
                "cat1".to_string(),
                "src1".to_string(),
                0.9_f32,
            )
            .unwrap();
        cache
            .store(
                "key2".to_string(),
                vec![0.9_f32, 0.1_f32, 0.0_f32],
                "cat1".to_string(),
                "src1".to_string(),
                0.9_f32,
            )
            .unwrap();
        cache
            .store(
                "key3".to_string(),
                vec![0.0_f32, 0.0_f32, 1.0_f32],
                "cat2".to_string(),
                "src2".to_string(),
                0.8_f32,
            )
            .unwrap();

        // Search for similar embeddings
        let query = vec![0.95_f32, 0.05_f32, 0.0_f32];
        let results = cache.find_similar(&query, 0.8_f32);

        assert!(!results.is_empty());
        assert_eq!(results[0].0, "key2"); // Most similar
    }
}
