use std::sync::Arc;
use std::collections::HashMap;
use dashmap::DashMap;
use parking_lot::RwLock;
use tokio::sync::{mpsc, oneshot, Mutex};
use uuid::Uuid;
use anyhow::{Result, anyhow};
use serde::{Serialize, Deserialize};
use think_ai_qwen::QwenClient;
use think_ai_knowledge::KnowledgeEngine;
use arc_swap::ArcSwap;
use futures::future::join_all;
use tracing::{info, warn, error};

pub mod thread_pool;
pub mod context_manager;
pub mod shared_intelligence;

use thread_pool::QuantumThreadPool;
use context_manager::ContextManager;
use shared_intelligence::SharedIntelligence;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GenerationRequest {
    pub query: String,
    pub context_id: Option<Uuid>,
    pub thread_type: ThreadType,
    pub temperature: Option<f32>,
    pub max_tokens: Option<usize>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum ThreadType {
    UserChat,
    Thinking,
    Dreaming,
    SelfReflection,
    KnowledgeCreation,
    Training,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GenerationResponse {
    pub text: String,
    pub context_id: Uuid,
    pub thread_id: Uuid,
    pub generation_time_ms: u64,
    pub model_used: String,
}

/// Quantum Generation Engine - Ensures all generation uses Qwen
/// with isolated parallel threads and shared knowledge
pub struct QuantumGenerationEngine {
    qwen_client: Arc<QwenClient>,
    thread_pool: Arc<QuantumThreadPool>,
    context_manager: Arc<ContextManager>,
    shared_intelligence: Arc<SharedIntelligence>,
    knowledge_engine: Arc<KnowledgeEngine>,
    generation_cache: Arc<DashMap<u64, GenerationResponse>>,
}

impl QuantumGenerationEngine {
    pub async fn new(knowledge_engine: Arc<KnowledgeEngine>) -> Result<Self> {
        // Initialize Qwen client with retry logic
        let qwen_client = Arc::new(QwenClient::new());
        
        // Verify Qwen is available
        Self::verify_qwen_availability(&qwen_client).await?;
        
        // Initialize thread pool with CPU count * 2 threads
        let thread_count = num_cpus::get() * 2;
        let thread_pool = Arc::new(QuantumThreadPool::new(thread_count));
        
        // Initialize context manager for isolated contexts
        let context_manager = Arc::new(ContextManager::new());
        
        // Initialize shared intelligence system
        let shared_intelligence = Arc::new(
            SharedIntelligence::new(knowledge_engine.clone()).await?
        );
        
        Ok(Self {
            qwen_client,
            thread_pool,
            context_manager,
            shared_intelligence,
            knowledge_engine,
            generation_cache: Arc::new(DashMap::new()),
        })
    }
    
    /// Verify Qwen is available and responding
    async fn verify_qwen_availability(client: &Arc<QwenClient>) -> Result<()> {
        match client.health_check().await {
            Ok(_) => {
                info!("Qwen model verified and ready");
                Ok(())
            }
            Err(e) => {
                error!("Qwen not available: {}", e);
                Err(anyhow!("Qwen model not available. Please ensure Ollama is running with Qwen model."))
            }
        }
    }
    
    /// Generate response using Qwen with isolated context
    pub async fn generate(&self, request: GenerationRequest) -> Result<GenerationResponse> {
        let start_time = std::time::Instant::now();
        
        // Get or create context
        let context_id = request.context_id.unwrap_or_else(|| {
            self.context_manager.create_context(request.thread_type)
        });
        
        // Check cache for O(1) performance
        let cache_key = self.hash_request(&request);
        if let Some(cached) = self.generation_cache.get(&cache_key) {
            return Ok(cached.clone());
        }
        
        // Get thread from pool
        let thread_id = self.thread_pool.get_thread(request.thread_type).await?;
        
        // Prepare context with shared knowledge
        let context = self.prepare_context(&request, context_id).await?;
        
        // Generate using Qwen (no fallback - Qwen only)
        let response_text = self.qwen_client
            .generate_with_context(&request.query, &context, request.temperature)
            .await
            .map_err(|e| anyhow!("Qwen generation failed: {}. Ensure Ollama is running.", e))?;
        
        // Update shared intelligence
        self.shared_intelligence.update(&request.query, &response_text).await;
        
        // Update context
        self.context_manager.update_context(context_id, &request.query, &response_text);
        
        let response = GenerationResponse {
            text: response_text,
            context_id,
            thread_id,
            generation_time_ms: start_time.elapsed().as_millis() as u64,
            model_used: "qwen2.5:1.5b".to_string(),
        };
        
        // Cache response
        self.generation_cache.insert(cache_key, response.clone());
        
        // Return thread to pool
        self.thread_pool.return_thread(thread_id);
        
        Ok(response)
    }
    
    /// Generate multiple responses in parallel with isolated contexts
    pub async fn generate_parallel(
        &self,
        requests: Vec<GenerationRequest>
    ) -> Result<Vec<GenerationResponse>> {
        let futures = requests.into_iter().map(|req| {
            let engine = self.clone();
            async move { engine.generate(req).await }
        });
        
        let results = join_all(futures).await;
        results.into_iter().collect()
    }
    
    /// Prepare context with shared knowledge
    async fn prepare_context(&self, request: &GenerationRequest, context_id: Uuid) -> Result<String> {
        let mut context_parts = vec![];
        
        // Add thread-specific context
        if let Some(thread_context) = self.context_manager.get_context(context_id) {
            context_parts.push(format!("Previous context:\n{}", thread_context));
        }
        
        // Add shared intelligence insights
        let insights = self.shared_intelligence.get_relevant_insights(&request.query).await?;
        if !insights.is_empty() {
            context_parts.push(format!("Shared intelligence:\n{}", insights.join("\n")));
        }
        
        // Add relevant knowledge
        let knowledge = self.knowledge_engine.search(&request.query, 3);
        if !knowledge.is_empty() {
            let knowledge_text = knowledge.iter()
                .map(|k| k.content.clone())
                .collect::<Vec<_>>()
                .join("\n");
            context_parts.push(format!("Knowledge base:\n{}", knowledge_text));
        }
        
        Ok(context_parts.join("\n\n"))
    }
    
    fn hash_request(&self, request: &GenerationRequest) -> u64 {
        use std::hash::{Hash, Hasher};
        use std::collections::hash_map::DefaultHasher;
        
        let mut hasher = DefaultHasher::new();
        request.query.hash(&mut hasher);
        request.thread_type.hash(&mut hasher);
        hasher.finish()
    }
}

impl Clone for QuantumGenerationEngine {
    fn clone(&self) -> Self {
        Self {
            qwen_client: self.qwen_client.clone(),
            thread_pool: self.thread_pool.clone(),
            context_manager: self.context_manager.clone(),
            shared_intelligence: self.shared_intelligence.clone(),
            knowledge_engine: self.knowledge_engine.clone(),
            generation_cache: self.generation_cache.clone(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    
    #[tokio::test]
    async fn test_quantum_generation_engine() {
        // Test will be implemented after other modules
    }
}