use std::sync::Arc;
use dashmap::DashMap;
use parking_lot::RwLock;
use tokio::sync::RwLock as AsyncRwLock;
use anyhow::Result;
use serde::{Serialize, Deserialize};
use think_ai_knowledge::KnowledgeEngine;
use std::collections::{HashMap, HashSet};
use tracing::{info, debug};

const MAX_INSIGHTS: usize = 1000;
const INSIGHT_RELEVANCE_THRESHOLD: f32 = 0.7;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Insight {
    pub id: String,
    pub content: String,
    pub source_query: String,
    pub source_response: String,
    pub embedding: Vec<f32>,
    pub confidence: f32,
    pub usage_count: usize,
    pub created_at: std::time::SystemTime,
}

#[derive(Debug, Clone)]
pub struct Pattern {
    pub pattern_type: String,
    pub occurrences: usize,
    pub examples: Vec<(String, String)>, // (query, response) pairs
}

/// Shared Intelligence System - Allows threads to share learned patterns and insights
pub struct SharedIntelligence {
    insights: Arc<DashMap<String, Arc<RwLock<Insight>>>>,
    patterns: Arc<AsyncRwLock<HashMap<String, Pattern>>>,
    knowledge_engine: Arc<KnowledgeEngine>,
    embeddings_cache: Arc<DashMap<u64, Vec<f32>>>,
}

impl SharedIntelligence {
    pub async fn new(knowledge_engine: Arc<KnowledgeEngine>) -> Result<Self> {
        let system = Self {
            insights: Arc::new(DashMap::new()),
            patterns: Arc::new(AsyncRwLock::new(HashMap::new())),
            knowledge_engine,
            embeddings_cache: Arc::new(DashMap::new()),
        };
        
        // Start pattern analysis task
        let patterns_clone = system.patterns.clone();
        let insights_clone = system.insights.clone();
        tokio::spawn(async move {
            loop {
                tokio::time::sleep(tokio::time::Duration::from_secs(60)).await;
                Self::analyze_patterns(&insights_clone, &patterns_clone).await;
            }
        });
        
        info!("Shared intelligence system initialized");
        Ok(system)
    }
    
    /// Update shared intelligence with new interaction
    pub async fn update(&self, query: &str, response: &str) {
        // Generate embedding for the response
        let embedding = self.generate_embedding(response).await;
        
        // Extract key insight from the interaction
        let insight_content = self.extract_insight(query, response);
        let insight_id = self.generate_insight_id(&insight_content);
        
        if let Some(existing) = self.insights.get(&insight_id) {
            // Update existing insight
            let mut insight = existing.write();
            insight.usage_count += 1;
            insight.confidence = (insight.confidence + 0.1).min(1.0);
        } else {
            // Create new insight
            let insight = Insight {
                id: insight_id.clone(),
                content: insight_content,
                source_query: query.to_string(),
                source_response: response.to_string(),
                embedding,
                confidence: 0.5,
                usage_count: 1,
                created_at: std::time::SystemTime::now(),
            };
            
            self.insights.insert(insight_id, Arc::new(RwLock::new(insight)));
            
            // Maintain size limit
            if self.insights.len() > MAX_INSIGHTS {
                self.remove_least_useful_insight();
            }
        }
        
        debug!("Updated shared intelligence with new insight");
    }
    
    /// Get relevant insights for a query
    pub async fn get_relevant_insights(&self, query: &str) -> Result<Vec<String>> {
        let query_embedding = self.generate_embedding(query).await;
        let mut scored_insights = Vec::new();
        
        for insight_ref in self.insights.iter() {
            let insight = insight_ref.value().read();
            let similarity = self.cosine_similarity(&query_embedding, &insight.embedding);
            
            if similarity > INSIGHT_RELEVANCE_THRESHOLD {
                scored_insights.push((similarity, insight.content.clone()));
            }
        }
        
        // Sort by relevance
        scored_insights.sort_by(|a, b| b.0.partial_cmp(&a.0).unwrap());
        
        // Return top 5 insights
        Ok(scored_insights
            .into_iter()
            .take(5)
            .map(|(_, content)| content)
            .collect())
    }
    
    /// Get learned patterns
    pub async fn get_patterns(&self) -> HashMap<String, Pattern> {
        self.patterns.read().await.clone()
    }
    
    /// Extract insight from interaction
    fn extract_insight(&self, query: &str, response: &str) -> String {
        // Simple extraction: take the first sentence or key concept
        let sentences: Vec<&str> = response.split(". ").collect();
        if let Some(first) = sentences.first() {
            format!("{} -> {}", 
                query.chars().take(50).collect::<String>(),
                first.chars().take(100).collect::<String>()
            )
        } else {
            format!("{} -> {}", 
                query.chars().take(50).collect::<String>(),
                response.chars().take(100).collect::<String>()
            )
        }
    }
    
    /// Generate embedding for text (simplified version)
    async fn generate_embedding(&self, text: &str) -> Vec<f32> {
        // Check cache
        let hash = self.hash_text(text);
        if let Some(cached) = self.embeddings_cache.get(&hash) {
            return cached.clone();
        }
        
        // Simple embedding: character frequency vector
        let mut embedding = vec![0.0; 128];
        for ch in text.chars().take(1000) {
            let idx = (ch as u32 % 128) as usize;
            embedding[idx] += 1.0;
        }
        
        // Normalize
        let sum: f32 = embedding.iter().sum();
        if sum > 0.0 {
            for val in &mut embedding {
                *val /= sum;
            }
        }
        
        // Cache
        self.embeddings_cache.insert(hash, embedding.clone());
        
        embedding
    }
    
    /// Calculate cosine similarity
    fn cosine_similarity(&self, a: &[f32], b: &[f32]) -> f32 {
        if a.len() != b.len() {
            return 0.0;
        }
        
        let dot_product: f32 = a.iter().zip(b.iter()).map(|(x, y)| x * y).sum();
        let norm_a: f32 = a.iter().map(|x| x * x).sum::<f32>().sqrt();
        let norm_b: f32 = b.iter().map(|x| x * x).sum::<f32>().sqrt();
        
        if norm_a * norm_b > 0.0 {
            dot_product / (norm_a * norm_b)
        } else {
            0.0
        }
    }
    
    /// Analyze patterns in insights
    async fn analyze_patterns(
        insights: &DashMap<String, Arc<RwLock<Insight>>>,
        patterns: &AsyncRwLock<HashMap<String, Pattern>>
    ) {
        let mut pattern_map = HashMap::new();
        
        // Simple pattern detection: group by common words
        for insight_ref in insights.iter() {
            let insight = insight_ref.value().read();
            let words: HashSet<String> = insight.content
                .split_whitespace()
                .filter(|w| w.len() > 4)
                .map(|w| w.to_lowercase())
                .collect();
            
            for word in words {
                let pattern = pattern_map.entry(word.clone()).or_insert(Pattern {
                    pattern_type: "keyword".to_string(),
                    occurrences: 0,
                    examples: Vec::new(),
                });
                
                pattern.occurrences += 1;
                if pattern.examples.len() < 5 {
                    pattern.examples.push((
                        insight.source_query.clone(),
                        insight.source_response.clone()
                    ));
                }
            }
        }
        
        // Keep only significant patterns
        pattern_map.retain(|_, pattern| pattern.occurrences >= 3);
        
        *patterns.write().await = pattern_map;
    }
    
    /// Remove least useful insight
    fn remove_least_useful_insight(&self) {
        if let Some(entry) = self.insights.iter()
            .min_by_key(|entry| {
                let insight = entry.value().read();
                (insight.usage_count as i32) * 1000 + (insight.confidence * 1000.0) as i32
            })
        {
            let id = entry.key().clone();
            drop(entry);  // Release the reference before removing
            self.insights.remove(&id);
        }
    }
    
    fn generate_insight_id(&self, content: &str) -> String {
        format!("insight_{}", self.hash_text(content))
    }
    
    fn hash_text(&self, text: &str) -> u64 {
        use std::hash::{Hash, Hasher};
        use std::collections::hash_map::DefaultHasher;
        
        let mut hasher = DefaultHasher::new();
        text.hash(&mut hasher);
        hasher.finish()
    }
}