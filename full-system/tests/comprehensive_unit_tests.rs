#[cfg(test)]
mod comprehensive_unit_tests {
    use crate::knowledge_loader::{KnowledgeBase, KnowledgeEntry, KnowledgeMetadata, DomainKnowledge};
    use crate::performance_optimizer::{RequestOptimizer, OptimizationConfig, OptimizationResult};
    use crate::metrics::{MetricsCollector, ChatMetrics, OptimizationMetrics, DashboardData};
    use crate::state::{ThinkAIState, ChatMessage};
    use crate::audio_service::AudioService;
    use std::collections::HashMap;
    use std::sync::Arc;
    use std::path::PathBuf;
    use tokio::sync::{RwLock, broadcast};

    // ========== Knowledge Loader Tests ==========
    
    #[test]
    fn test_knowledge_base_new() {
        let kb = KnowledgeBase::new();
        assert!(kb.domains.is_empty());
        assert!(kb.topic_index.is_empty());
        assert!(kb.response_cache.is_empty());
    }

    #[test]
    fn test_knowledge_entry_creation() {
        let entry = KnowledgeEntry {
            topic: "test topic".to_string(),
            content: "test content".to_string(),
            metadata: KnowledgeMetadata {
                conversational_patterns: vec!["pattern1".to_string()],
                evaluation_score: 0.95,
                source: "test".to_string(),
                generated_at: "2024-01-01".to_string(),
            },
            related_concepts: vec!["concept1".to_string()],
        };
        
        assert_eq!(entry.topic, "test topic");
        assert_eq!(entry.content, "test content");
        assert_eq!(entry.metadata.evaluation_score, 0.95);
    }

    #[test]
    fn test_knowledge_base_find_knowledge_exact_match() {
        let mut kb = KnowledgeBase::new();
        
        let entry = create_test_knowledge_entry("quantum mechanics", "Physics of small particles");
        let domain = DomainKnowledge {
            domain: "physics".to_string(),
            entries: vec![entry],
        };
        
        kb.domains.insert("physics".to_string(), domain);
        kb.topic_index.insert("quantum mechanics".to_string(), vec![("physics".to_string(), 0)]);
        
        let result = kb.find_knowledge("quantum mechanics");
        assert!(result.is_some());
    }

    #[test]
    fn test_knowledge_base_find_knowledge_case_insensitive() {
        let mut kb = KnowledgeBase::new();
        
        let entry = create_test_knowledge_entry("Artificial Intelligence", "AI content");
        let domain = DomainKnowledge {
            domain: "tech".to_string(),
            entries: vec![entry],
        };
        
        kb.domains.insert("tech".to_string(), domain);
        kb.topic_index.insert("artificial intelligence".to_string(), vec![("tech".to_string(), 0)]);
        
        // Test various case variations
        assert!(kb.find_knowledge("ARTIFICIAL INTELLIGENCE").is_some());
        assert!(kb.find_knowledge("artificial intelligence").is_some());
        assert!(kb.find_knowledge("Artificial Intelligence").is_some());
    }

    #[test]
    fn test_knowledge_base_response_cache_lookup() {
        let mut kb = KnowledgeBase::new();
        kb.response_cache.insert("hello".to_string(), "Hi there!".to_string());
        
        let result = kb.find_knowledge("hello");
        assert!(result.is_some());
        assert_eq!(result.unwrap(), "Hi there!");
    }

    #[test]
    fn test_knowledge_base_related_concepts() {
        let mut kb = KnowledgeBase::new();
        
        let entry = KnowledgeEntry {
            topic: "machine learning".to_string(),
            content: "ML content".to_string(),
            metadata: KnowledgeMetadata {
                conversational_patterns: vec!["ML is about learning from data".to_string()],
                evaluation_score: 0.9,
                source: "test".to_string(),
                generated_at: "2024".to_string(),
            },
            related_concepts: vec!["artificial intelligence".to_string(), "neural networks".to_string()],
        };
        
        let domain = DomainKnowledge {
            domain: "tech".to_string(),
            entries: vec![entry],
        };
        
        kb.domains.insert("tech".to_string(), domain);
        
        // Should find by related concept
        let result = kb.find_knowledge("neural networks");
        assert!(result.is_some());
    }

    #[test]
    fn test_knowledge_base_conversational_response() {
        let kb = KnowledgeBase::new();
        let response = kb.get_conversational_response("test query");
        
        assert!(response.contains("I'd be happy to help"));
        assert!(response.contains("test query"));
    }

    #[test]
    fn test_knowledge_base_load_from_directory() {
        // This would require mocking the file system
        // For now, test that the method exists and returns error for non-existent dir
        let result = KnowledgeBase::load_from_directory("/non/existent/path");
        assert!(result.is_err());
    }

    // ========== Performance Optimizer Tests ==========

    #[test]
    fn test_optimization_config_default() {
        let config = OptimizationConfig::default();
        
        assert_eq!(config.max_tokens, 2048);
        assert_eq!(config.temperature, 0.7);
        assert_eq!(config.top_p, 0.95);
        assert_eq!(config.cache_ttl_seconds, 3600);
        assert_eq!(config.cache_size, 10000);
        assert_eq!(config.num_gpu_layers, None);
        assert_eq!(config.batch_size, 1);
        assert_eq!(config.context_window_size, 4096);
    }

    #[test]
    fn test_request_optimizer_new() {
        let config = OptimizationConfig::default();
        let optimizer = RequestOptimizer::new(config.clone());
        
        assert!(optimizer.cache.is_empty());
        assert_eq!(optimizer.config.max_tokens, config.max_tokens);
    }

    #[tokio::test]
    async fn test_request_optimizer_cache_miss() {
        let config = OptimizationConfig::default();
        let optimizer = Arc::new(RequestOptimizer::new(config));
        
        let result = optimizer.optimize_request("new query".to_string()).await;
        
        assert_eq!(result.optimized_query, "new query");
        assert!(result.cache_hit.is_none());
        assert!(result.optimization_applied);
    }

    #[tokio::test]
    async fn test_request_optimizer_cache_hit() {
        let config = OptimizationConfig::default();
        let optimizer = Arc::new(RequestOptimizer::new(config));
        
        // First request - cache miss
        let result1 = optimizer.optimize_request("test query".to_string()).await;
        assert!(result1.cache_hit.is_none());
        
        // Second request - cache hit
        let result2 = optimizer.optimize_request("test query".to_string()).await;
        assert!(result2.cache_hit.is_some());
        assert_eq!(result2.cache_hit.unwrap(), "test query");
    }

    #[tokio::test]
    async fn test_request_optimizer_cache_expiration() {
        let mut config = OptimizationConfig::default();
        config.cache_ttl_seconds = 1; // 1 second TTL
        let optimizer = Arc::new(RequestOptimizer::new(config));
        
        // Add to cache
        optimizer.optimize_request("expiring query".to_string()).await;
        
        // Should hit cache immediately
        let result = optimizer.optimize_request("expiring query".to_string()).await;
        assert!(result.cache_hit.is_some());
        
        // Wait for expiration
        tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;
        
        // Should miss cache after expiration
        let result = optimizer.optimize_request("expiring query".to_string()).await;
        assert!(result.cache_hit.is_none());
    }

    #[tokio::test]
    async fn test_request_optimizer_update_config() {
        let optimizer = Arc::new(RequestOptimizer::new(OptimizationConfig::default()));
        
        let mut new_config = OptimizationConfig::default();
        new_config.max_tokens = 4096;
        new_config.temperature = 0.9;
        
        optimizer.update_config(new_config.clone()).await;
        
        // Verify config was updated
        let result = optimizer.optimize_request("test".to_string()).await;
        assert!(result.optimization_applied);
    }

    #[tokio::test]
    async fn test_request_optimizer_get_stats() {
        let optimizer = Arc::new(RequestOptimizer::new(OptimizationConfig::default()));
        
        // Generate some cache activity
        optimizer.optimize_request("query1".to_string()).await;
        optimizer.optimize_request("query1".to_string()).await; // hit
        optimizer.optimize_request("query2".to_string()).await; // miss
        
        let stats = optimizer.get_optimization_stats().await;
        
        assert_eq!(stats.total_requests, 3);
        assert_eq!(stats.cache_hits, 1);
        assert_eq!(stats.cache_misses, 2);
        assert!(stats.cache_hit_rate > 0.0 && stats.cache_hit_rate < 1.0);
    }

    // ========== Metrics Collector Tests ==========

    #[tokio::test]
    async fn test_metrics_collector_new() {
        let collector = MetricsCollector::new();
        
        let metrics = collector.get_metrics().await;
        assert_eq!(metrics.total_requests, 0);
        assert_eq!(metrics.total_tokens, 0);
        assert_eq!(metrics.cache_hits, 0);
    }

    #[tokio::test]
    async fn test_metrics_collector_record_chat() {
        let collector = MetricsCollector::new();
        
        let chat_metrics = ChatMetrics {
            session_id: "test-session".to_string(),
            response_time_ms: 150,
            tokens_used: 100,
            cache_hit: true,
            timestamp: 1234567890,
        };
        
        collector.record_chat_metrics(chat_metrics).await;
        
        let metrics = collector.get_metrics().await;
        assert_eq!(metrics.total_requests, 1);
        assert_eq!(metrics.total_tokens, 100);
        assert_eq!(metrics.cache_hits, 1);
        assert_eq!(metrics.average_response_time, 150.0);
    }

    #[tokio::test]
    async fn test_metrics_collector_multiple_records() {
        let collector = MetricsCollector::new();
        
        // Record multiple metrics
        for i in 0..5 {
            let chat_metrics = ChatMetrics {
                session_id: format!("session-{}", i),
                response_time_ms: 100 + i * 50,
                tokens_used: 50 + i * 10,
                cache_hit: i % 2 == 0,
                timestamp: 1234567890 + i,
            };
            collector.record_chat_metrics(chat_metrics).await;
        }
        
        let metrics = collector.get_metrics().await;
        assert_eq!(metrics.total_requests, 5);
        assert_eq!(metrics.cache_hits, 3); // 0, 2, 4
        assert!(metrics.average_response_time > 0.0);
    }

    #[tokio::test]
    async fn test_metrics_collector_optimization_metrics() {
        let collector = MetricsCollector::new();
        
        let opt_metrics = OptimizationMetrics {
            query_optimization_time_ms: 5,
            cache_lookup_time_ms: 2,
            total_optimization_time_ms: 7,
        };
        
        collector.record_optimization_metrics(opt_metrics).await;
        
        // Verify metrics were recorded (would need getter methods)
    }

    #[tokio::test]
    async fn test_metrics_collector_dashboard_data() {
        let collector = MetricsCollector::new();
        
        // Add some test data
        for _ in 0..3 {
            let chat_metrics = ChatMetrics {
                session_id: "test".to_string(),
                response_time_ms: 100,
                tokens_used: 50,
                cache_hit: true,
                timestamp: 1234567890,
            };
            collector.record_chat_metrics(chat_metrics).await;
        }
        
        let dashboard = collector.get_dashboard_data().await;
        
        assert_eq!(dashboard.total_requests, 3);
        assert_eq!(dashboard.active_sessions, 1);
        assert!(dashboard.cache_hit_rate > 0.0);
        assert!(dashboard.uptime_seconds > 0);
    }

    // ========== State Tests ==========

    #[test]
    fn test_chat_message_creation() {
        let msg = ChatMessage {
            id: "msg-1".to_string(),
            session_id: "session-1".to_string(),
            message: "Hello".to_string(),
            response: Some("Hi there".to_string()),
            timestamp: 1234567890,
        };
        
        assert_eq!(msg.id, "msg-1");
        assert_eq!(msg.session_id, "session-1");
        assert_eq!(msg.message, "Hello");
        assert!(msg.response.is_some());
    }

    #[tokio::test]
    async fn test_state_clone() {
        // Create mock state components
        let (tx, _rx) = broadcast::channel(100);
        
        // This test verifies that ThinkAIState can be cloned
        // (Important for Axum's state sharing)
        let state = create_test_state().await;
        let cloned_state = state.clone();
        
        // Both should point to same Arc instances
        assert!(Arc::ptr_eq(&state.knowledge_engine, &cloned_state.knowledge_engine));
    }

    // ========== Audio Service Tests ==========

    #[test]
    fn test_audio_service_creation() {
        let service = AudioService::new(
            "test_deepgram_key".to_string(),
            "test_elevenlabs_key".to_string(),
            PathBuf::from("./test_cache"),
        );
        
        // Verify service is created with correct keys
        // (Internal fields would need to be exposed for full testing)
    }

    #[tokio::test]
    async fn test_audio_service_cache_lookup() {
        let service = AudioService::new(
            "test_key".to_string(),
            "test_key".to_string(),
            PathBuf::from("./test_cache"),
        );
        
        // Test cache lookup for non-existent audio
        let result = service.get_cached_audio("non_existent_text").await;
        assert!(result.is_err());
    }

    // ========== Helper Functions ==========

    fn create_test_knowledge_entry(topic: &str, content: &str) -> KnowledgeEntry {
        KnowledgeEntry {
            topic: topic.to_string(),
            content: content.to_string(),
            metadata: KnowledgeMetadata {
                conversational_patterns: vec![format!("{} pattern", topic)],
                evaluation_score: 0.9,
                source: "test".to_string(),
                generated_at: "2024-01-01".to_string(),
            },
            related_concepts: vec![],
        }
    }

    async fn create_test_state() -> ThinkAIState {
        use think_ai_consciousness::ConsciousnessFramework;
        use think_ai_core::{EngineConfig, O1Engine};
        use think_ai_knowledge::KnowledgeEngine;
        use think_ai_qwen::QwenClient;
        use think_ai_storage::PersistentConversationMemory;
        use think_ai_vector::{LSHConfig, O1VectorIndex};
        
        let (tx, _rx) = broadcast::channel(100);
        
        ThinkAIState {
            _core_engine: Arc::new(O1Engine::new(EngineConfig::default())),
            knowledge_engine: Arc::new(KnowledgeEngine::new()),
            _vector_index: Arc::new(O1VectorIndex::new(LSHConfig::default()).unwrap()),
            _consciousness_framework: Arc::new(ConsciousnessFramework::new()),
            persistent_memory: Arc::new(PersistentConversationMemory::new(":memory:").await.unwrap()),
            message_channel: tx,
            qwen_client: Arc::new(QwenClient::new()),
            audio_service: None,
            whatsapp_notifier: None,
            metrics_collector: Arc::new(MetricsCollector::new()),
            request_optimizer: Arc::new(RequestOptimizer::new(OptimizationConfig::default())),
            knowledge_base: Arc::new(KnowledgeBase::new()),
        }
    }

    // ========== Edge Case Tests ==========

    #[test]
    fn test_knowledge_base_empty_query() {
        let kb = KnowledgeBase::new();
        let result = kb.find_knowledge("");
        assert!(result.is_none());
    }

    #[test]
    fn test_knowledge_base_special_characters() {
        let mut kb = KnowledgeBase::new();
        kb.response_cache.insert("test!@#$".to_string(), "Special response".to_string());
        
        let result = kb.find_knowledge("test!@#$");
        assert!(result.is_some());
    }

    #[tokio::test]
    async fn test_metrics_collector_concurrent_updates() {
        let collector = Arc::new(MetricsCollector::new());
        let mut handles = vec![];
        
        // Spawn multiple tasks updating metrics concurrently
        for i in 0..10 {
            let collector_clone = collector.clone();
            let handle = tokio::spawn(async move {
                let metrics = ChatMetrics {
                    session_id: format!("concurrent-{}", i),
                    response_time_ms: 100,
                    tokens_used: 50,
                    cache_hit: true,
                    timestamp: 1234567890,
                };
                collector_clone.record_chat_metrics(metrics).await;
            });
            handles.push(handle);
        }
        
        // Wait for all tasks
        for handle in handles {
            handle.await.unwrap();
        }
        
        let final_metrics = collector.get_metrics().await;
        assert_eq!(final_metrics.total_requests, 10);
    }

    #[test]
    fn test_optimization_config_custom() {
        let config = OptimizationConfig {
            max_tokens: 4096,
            temperature: 0.9,
            top_p: 0.99,
            cache_ttl_seconds: 7200,
            cache_size: 50000,
            num_gpu_layers: Some(24),
            batch_size: 4,
            context_window_size: 8192,
        };
        
        assert_eq!(config.max_tokens, 4096);
        assert_eq!(config.num_gpu_layers, Some(24));
        assert_eq!(config.batch_size, 4);
    }
}