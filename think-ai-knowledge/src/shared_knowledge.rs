use rand::prelude::*;
use serde::{Deserialize, Serialize};
use std::collections::{HashMap, HashSet};
use std::sync::RwLock;
use std::time::{SystemTime, UNIX_EPOCH};

/// Shared knowledge base accessible by all sessions and processes
#[derive(Debug)]
pub struct SharedKnowledge {
    /// Core knowledge storage with O(1) access
    knowledge_store: RwLock<KnowledgeStore>,

    /// Index for fast lookups
    knowledge_index: RwLock<KnowledgeIndex>,

    /// Statistics tracking
    stats: RwLock<KnowledgeStats>,
}

#[derive(Debug)]
struct KnowledgeStore {
    /// Main storage using hash map for O(1) access
    items: HashMap<String, KnowledgeItem>,

    /// Category-based organization
    categories: HashMap<String, HashSet<String>>,

    /// Source tracking
    sources: HashMap<String, HashSet<String>>,
}

#[derive(Debug)]
struct KnowledgeIndex {
    /// Word to item IDs mapping for fast search
    word_index: HashMap<String, HashSet<String>>,

    /// Confidence-based priority queue
    confidence_index: Vec<(f32, String)>,

    /// Time-based index for recent items
    time_index: Vec<(u64, String)>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeItem {
    pub content: String,
    pub source: String,
    pub confidence: f32,
    pub metadata: HashMap<String, String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeQuery {
    pub content: String,
    pub context: Option<String>,
    pub max_results: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct KnowledgeStats {
    pub total_items: usize,
    pub total_sources: usize,
    pub average_confidence: f32,
    pub categories: Vec<String>,
    pub last_update: u64,
}

impl SharedKnowledge {
    /// Create a new shared knowledge base
    pub fn new() -> Self {
        Self {
            knowledge_store: RwLock::new(KnowledgeStore {
                items: HashMap::new(),
                categories: HashMap::new(),
                sources: HashMap::new(),
            }),
            knowledge_index: RwLock::new(KnowledgeIndex {
                word_index: HashMap::new(),
                confidence_index: Vec::new(),
                time_index: Vec::new(),
            }),
            stats: RwLock::new(KnowledgeStats {
                total_items: 0,
                total_sources: 0,
                average_confidence: 0.0,
                categories: Vec::new(),
                last_update: 0,
            }),
        }
    }

    /// Add new knowledge to the shared base
    pub async fn add_knowledge(&self, item: KnowledgeItem) -> Result<String, String> {
        let item_id = self.generate_item_id(&item);
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();

        // Add to main store
        {
            let mut store = self.knowledge_store.write().unwrap();
            store.items.insert(item_id.clone(), item.clone());

            // Update source tracking
            store
                .sources
                .entry(item.source.clone())
                .or_default()
                .insert(item_id.clone());

            // Extract and update categories
            if let Some(category) = item.metadata.get("category") {
                store
                    .categories
                    .entry(category.clone())
                    .or_default()
                    .insert(item_id.clone());
            }
        }

        // Update indices
        {
            let mut index = self.knowledge_index.write().unwrap();

            // Update word index
            for word in item.content.split_whitespace() {
                if word.len() > 2 {
                    index
                        .word_index
                        .entry(word.to_lowercase())
                        .or_default()
                        .insert(item_id.clone());
                }
            }

            // Update confidence index
            index
                .confidence_index
                .push((item.confidence, item_id.clone()));
            index
                .confidence_index
                .sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());

            // Update time index
            index.time_index.push((timestamp, item_id.clone()));
            index.time_index.sort_by(|a, b| b.0.cmp(&a.0));
        }

        // Update statistics
        self.update_stats().await;

        Ok(item_id)
    }

    /// Query knowledge base for relevant information
    pub async fn query(&self, query: KnowledgeQuery) -> Result<Vec<String>, String> {
        let mut results = Vec::new();
        let mut scored_items: Vec<(f32, String)> = Vec::new();

        // Extract query words
        let query_words: HashSet<String> = query
            .content
            .split_whitespace()
            .filter(|w| w.len() > 2)
            .map(|w| w.to_lowercase())
            .collect();

        // Search using word index
        {
            let index = self.knowledge_index.read().unwrap();
            let store = self.knowledge_store.read().unwrap();

            let mut item_scores: HashMap<String, f32> = HashMap::new();

            // Score items based on word matches
            for word in &query_words {
                if let Some(item_ids) = index.word_index.get(word) {
                    for item_id in item_ids {
                        *item_scores.entry(item_id.clone()).or_insert(0.0) += 1.0;
                    }
                }
            }

            // Add confidence scores
            for (item_id, word_score) in item_scores {
                if let Some(item) = store.items.get(&item_id) {
                    let total_score = word_score * item.confidence;
                    scored_items.push((total_score, item.content.clone()));
                }
            }
        }

        // Sort by score and return top results
        scored_items.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());

        for (_, content) in scored_items.into_iter().take(query.max_results) {
            results.push(content);
        }

        Ok(results)
    }

    /// Get recent knowledge items
    pub async fn get_recent_items(&self, count: usize) -> Vec<KnowledgeItem> {
        let index = self.knowledge_index.read().unwrap();
        let store = self.knowledge_store.read().unwrap();

        let mut items = Vec::new();

        for (_, item_id) in index.time_index.iter().take(count) {
            if let Some(item) = store.items.get(item_id) {
                items.push(item.clone());
            }
        }

        items
    }

    /// Get random knowledge items (for dreaming process)
    pub async fn get_random_items(&self, count: usize) -> Vec<KnowledgeItem> {
        let store = self.knowledge_store.read().unwrap();
        let item_ids: Vec<String> = store.items.keys().cloned().collect();

        if item_ids.is_empty() {
            return Vec::new();
        }

        let mut rng = rand::thread_rng();
        let mut items = Vec::new();

        for _ in 0..count.min(item_ids.len()) {
            let idx = rng.gen_range(0..item_ids.len());
            if let Some(item) = store.items.get(&item_ids[idx]) {
                items.push(item.clone());
            }
        }

        items
    }

    /// Get knowledge statistics
    pub async fn get_statistics(&self) -> KnowledgeStats {
        self.stats.read().unwrap().clone()
    }

    /// Consolidate similar knowledge items
    pub async fn consolidate_knowledge(&self) {
        // Simple consolidation: merge items with very similar content
        let mut to_merge: Vec<(String, String)> = Vec::new();

        {
            let store = self.knowledge_store.read().unwrap();
            let items: Vec<(String, KnowledgeItem)> = store
                .items
                .iter()
                .map(|(k, v)| (k.clone(), v.clone()))
                .collect();

            // Find similar items (simple approach using word overlap)
            for i in 0..items.len() {
                for j in i + 1..items.len() {
                    let words1: HashSet<&str> = items[i].1.content.split_whitespace().collect();
                    let words2: HashSet<&str> = items[j].1.content.split_whitespace().collect();

                    let intersection = words1.intersection(&words2).count();
                    let union = words1.union(&words2).count();

                    if union > 0 {
                        let similarity = intersection as f32 / union as f32;
                        if similarity > 0.8 {
                            // Mark for merging (keep the one with higher confidence)
                            if items[i].1.confidence >= items[j].1.confidence {
                                to_merge.push((items[j].0.clone(), items[i].0.clone()));
                            } else {
                                to_merge.push((items[i].0.clone(), items[j].0.clone()));
                            }
                        }
                    }
                }
            }
        }

        // Merge similar items
        if !to_merge.is_empty() {
            let mut store = self.knowledge_store.write().unwrap();
            let mut index = self.knowledge_index.write().unwrap();

            for (remove_id, _keep_id) in to_merge {
                // Remove from main store
                if let Some(removed_item) = store.items.remove(&remove_id) {
                    // Update source tracking
                    if let Some(source_items) = store.sources.get_mut(&removed_item.source) {
                        source_items.remove(&remove_id);
                    }

                    // Update word index
                    for word in removed_item.content.split_whitespace() {
                        if let Some(word_items) = index.word_index.get_mut(&word.to_lowercase()) {
                            word_items.remove(&remove_id);
                        }
                    }
                }
            }
        }

        self.update_stats().await;
    }

    /// Generate unique ID for knowledge item
    fn generate_item_id(&self, item: &KnowledgeItem) -> String {
        use std::hash::{Hash, Hasher};
        let mut hasher = std::collections::hash_map::DefaultHasher::new();
        item.content.hash(&mut hasher);
        item.source.hash(&mut hasher);
        format!("knowledge_{:x}", hasher.finish())
    }

    /// Update knowledge statistics
    async fn update_stats(&self) {
        let store = self.knowledge_store.read().unwrap();
        let mut stats = self.stats.write().unwrap();

        stats.total_items = store.items.len();
        stats.total_sources = store.sources.len();

        if stats.total_items > 0 {
            let total_confidence: f32 = store.items.values().map(|item| item.confidence).sum();
            stats.average_confidence = total_confidence / stats.total_items as f32;
        } else {
            stats.average_confidence = 0.0;
        }

        stats.categories = store.categories.keys().cloned().collect();
        stats.last_update = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs();
    }

    /// Clear all knowledge (use with caution)
    pub async fn clear_all(&self) {
        self.knowledge_store.write().unwrap().items.clear();
        self.knowledge_store.write().unwrap().categories.clear();
        self.knowledge_store.write().unwrap().sources.clear();
        self.knowledge_index.write().unwrap().word_index.clear();
        self.knowledge_index
            .write()
            .unwrap()
            .confidence_index
            .clear();
        self.knowledge_index.write().unwrap().time_index.clear();
        self.update_stats().await;
    }
}

impl Default for SharedKnowledge {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn test_shared_knowledge_creation() {
        let knowledge = SharedKnowledge::new();
        let stats = knowledge.get_statistics().await;

        assert_eq!(stats.total_items, 0);
        assert_eq!(stats.total_sources, 0);
    }

    #[tokio::test]
    async fn test_add_and_query_knowledge() {
        let knowledge = SharedKnowledge::new();

        // Add some knowledge
        let item1 = KnowledgeItem {
            content: "Rust is a memory-safe programming language".to_string(),
            source: "test_source".to_string(),
            confidence: 0.9,
            metadata: HashMap::new(),
        };

        let item2 = KnowledgeItem {
            content: "Programming languages help build software".to_string(),
            source: "test_source".to_string(),
            confidence: 0.8,
            metadata: HashMap::new(),
        };

        knowledge.add_knowledge(item1).await.unwrap();
        knowledge.add_knowledge(item2).await.unwrap();

        // Query for knowledge
        let ___query = KnowledgeQuery {
            content: "programming language".to_string(),
            context: None,
            max_results: 5,
        };

        let ___results = knowledge.query(query).await.unwrap();
        assert!(!results.is_empty());
        assert!(results[0].contains("programming"));
    }

    #[tokio::test]
    async fn test_knowledge_statistics() {
        let knowledge = SharedKnowledge::new();

        // Add knowledge with categories
        let mut item = KnowledgeItem {
            content: "Test knowledge item".to_string(),
            source: "test_source".to_string(),
            confidence: 0.85,
            metadata: HashMap::new(),
        };
        item.metadata
            .insert("category".to_string(), "test_category".to_string());

        knowledge.add_knowledge(item).await.unwrap();

        let stats = knowledge.get_statistics().await;
        assert_eq!(stats.total_items, 1);
        assert_eq!(stats.total_sources, 1);
        assert_eq!(stats.average_confidence, 0.85);
        assert!(stats.categories.contains(&"test_category".to_string()));
    }
}
