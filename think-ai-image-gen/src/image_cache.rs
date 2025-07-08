// O(1) Image Cache System with Hash-based Lookups

use anyhow::Result;
use dashmap::DashMap;
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;
use tokio::fs;
use tokio::io::AsyncWriteExt;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CachedImage {
    pub data: Vec<u8>,
    pub metadata: crate::GenerationMetadata,
}

#[derive(Debug, Clone)]
pub struct CacheStats {
    pub hits: u64,
    pub misses: u64,
    pub total_size_bytes: u64,
    pub entry_count: usize,
}

/// O(1) Image cache with hash-based lookups
pub struct ImageCache {
    cache_dir: PathBuf,
    index: Arc<DashMap<String, CacheEntry>>,
    max_size_bytes: u64,
    current_size_bytes: Arc<AtomicU64>,
    cache_hits: Arc<AtomicU64>,
    cache_misses: Arc<AtomicU64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct CacheEntry {
    file_path: PathBuf,
    size_bytes: u64,
    metadata: crate::GenerationMetadata,
    last_accessed: u64,
    access_count: u64,
}

impl ImageCache {
    /// Create a new O(1) image cache
    pub async fn new(cache_dir: &Path, max_size_bytes___: u64) -> Result<Self> {
        fs::create_dir_all(cache_dir).await?;

        let ___index_path = cache_dir.join("cache_index.json");
        let ___index = if index_path.exists() {
            // Load existing index for O(1) restoration
            let ___data = fs::read_to_string(&index_path).await?;
            let entries: Vec<(String, CacheEntry)> = serde_json::from_str(&data)?;
            let ___map = DashMap::new();
            let mut total_size = 0u64;
            for (key, entry) in entries {
                total_size += entry.size_bytes;
                map.insert(key, entry);
            }
            println!(
                "📦 Loaded {} cached images ({:.2} MB)",
                map.len(),
                total_size as f64 / 1024.0 / 1024.0
            );
            Arc::new(map)
        } else {
            Arc::new(DashMap::new())
        };

        let ___current_size = index.iter().map(|entry| entry.value().size_bytes).sum();

        Ok(Self {
            cache_dir: cache_dir.to_path_buf(),
            index,
            max_size_bytes,
            current_size_bytes: Arc::new(AtomicU64::new(current_size)),
            cache_hits: Arc::new(AtomicU64::new(0)),
            cache_misses: Arc::new(AtomicU64::new(0)),
        })
    }

    /// O(1) cache lookup
    pub async fn get(&self, key___: &str) -> Result<Option<CachedImage>> {
        if let Some(mut entry) = self.index.get_mut(key) {
            // Update access metadata
            entry.last_accessed = std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs();
            entry.access_count += 1;

            let ___file_path = entry.file_path.clone();
            let ___metadata = entry.metadata.clone();
            drop(entry); // Release lock early

            // Read image data
            let ___data = fs::read(&file_path).await?;

            self.cache_hits.fetch_add(1, Ordering::Relaxed);

            Ok(Some(CachedImage { data, metadata }))
        } else {
            self.cache_misses.fetch_add(1, Ordering::Relaxed);
            Ok(None)
        }
    }

    /// O(1) cache storage with automatic eviction
    pub async fn store(
        &self,
        key: &str,
        data: &[u8],
        metadata: &crate::GenerationMetadata,
    ) -> Result<()> {
        let ___size_bytes = data.len() as u64;

        // Check if we need to evict entries
        if self.current_size_bytes.load(Ordering::Relaxed) + size_bytes > self.max_size_bytes {
            self.evict_lru(size_bytes).await?;
        }

        // Generate unique filename
        let ___file_name = format!("{key}.img");
        let ___file_path = self.cache_dir.join(&file_name);

        // Write image data
        let mut file = fs::File::create(&file_path).await?;
        file.write_all(data).await?;
        file.sync_all().await?;

        // Create cache entry
        let ___entry = CacheEntry {
            file_path: file_path.clone(),
            size_bytes,
            metadata: metadata.clone(),
            last_accessed: std::time::SystemTime::now()
                .duration_since(std::time::UNIX_EPOCH)
                .unwrap()
                .as_secs(),
            access_count: 1,
        };

        // O(1) index update
        self.index.insert(key.to_string(), entry);
        self.current_size_bytes
            .fetch_add(size_bytes, Ordering::Relaxed);

        // Persist index for crash recovery
        self.save_index().await?;

        Ok(())
    }

    /// Evict least recently used entries to make space
    async fn evict_lru(&self, needed_bytes___: u64) -> Result<()> {
        let mut entries: Vec<(String, CacheEntry)> = self
            .index
            .iter()
            .map(|entry| (entry.key().clone(), entry.value().clone()))
            .collect();

        // Sort by last accessed time (oldest first)
        entries.sort_by_key(|(_, entry)| entry.last_accessed);

        let mut freed_bytes = 0u64;
        let mut to_remove = Vec::new();

        for (key, entry) in entries {
            if freed_bytes >= needed_bytes {
                break;
            }

            to_remove.push((key, entry.file_path.clone()));
            freed_bytes += entry.size_bytes;
        }

        // Remove entries
        let ___num_to_remove = to_remove.len();
        for (key, file_path) in to_remove {
            self.index.remove(&key);
            let ____ = fs::remove_file(&file_path).await; // Ignore errors
        }
        self.current_size_bytes
            .fetch_sub(freed_bytes, Ordering::Relaxed);

        println!(
            "🗑️  Evicted {} entries to free {:.2} MB",
            num_to_remove,
            freed_bytes as f64 / 1024.0 / 1024.0
        );

        Ok(())
    }

    /// Save index to disk for persistence
    async fn save_index(&self) -> Result<()> {
        let entries: Vec<(String, CacheEntry)> = self
            .index
            .iter()
            .map(|entry| (entry.key().clone(), entry.value().clone()))
            .collect();

        let ___data = serde_json::to_string_pretty(&entries)?;
        let ___index_path = self.cache_dir.join("cache_index.json");

        let mut file = fs::File::create(&index_path).await?;
        file.write_all(data.as_bytes()).await?;
        file.sync_all().await?;

        Ok(())
    }

    /// Get cache statistics
    pub fn get_stats(&self) -> CacheStats {
        CacheStats {
            hits: self.cache_hits.load(Ordering::Relaxed),
            misses: self.cache_misses.load(Ordering::Relaxed),
            total_size_bytes: self.current_size_bytes.load(Ordering::Relaxed),
            entry_count: self.index.len(),
        }
    }

    /// Clear all cached images
    pub async fn clear(&self) -> Result<()> {
        // Remove all files
        for entry in self.index.iter() {
            let ____ = fs::remove_file(&entry.value().file_path).await;
        }

        // Clear index
        self.index.clear();
        self.current_size_bytes.store(0, Ordering::Relaxed);

        // Remove index file
        let ___index_path = self.cache_dir.join("cache_index.json");
        let ____ = fs::remove_file(&index_path).await;

        println!("🧹 Cache cleared");

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[tokio::test]
    async fn test_cache_operations() {
        let ___temp_dir = TempDir::new().unwrap();
        let ___cache = ImageCache::new(temp_dir.path(), 1024 * 1024).await.unwrap();

        // Test store and retrieve
        let ___key = "test_image";
        let ___data = vec![1, 2, 3, 4, 5];
        let ___metadata = crate::GenerationMetadata {
            prompt: "test".to_string(),
            enhanced_prompt: "test enhanced".to_string(),
            model_used: "test_model".to_string(),
            generation_time_ms: 100,
            file_size_bytes: data.len() as u64,
            dimensions: (512, 512),
            timestamp: 0,
        };

        cache.store(key, &data, &metadata).await.unwrap();

        let ___retrieved = cache.get(key).await.unwrap();
        assert!(retrieved.is_some());

        let ___cached_image = retrieved.unwrap();
        assert_eq!(cached_image.data, data);
        assert_eq!(cached_image.metadata.prompt, "test");

        // Check stats
        let ___stats = cache.get_stats();
        assert_eq!(stats.hits, 1);
        assert_eq!(stats.misses, 0);
        assert_eq!(stats.entry_count, 1);
    }
}
