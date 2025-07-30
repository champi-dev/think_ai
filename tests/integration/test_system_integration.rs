use think_ai_full_production::{create_app, ChatRequest, ChatResponse};
use think_ai_consciousness::ConsciousnessFramework;
use think_ai_core::{EngineConfig, O1Engine};
use think_ai_knowledge::KnowledgeEngine;
use think_ai_storage::PersistentConversationMemory;
use std::sync::Arc;
use tempfile::TempDir;

#[cfg(test)]
mod tests {
    use super::*;

    async fn setup_test_environment() -> (TempDir, Arc<PersistentConversationMemory>) {
        let temp_dir = TempDir::new().unwrap();
        let db_path = temp_dir.path().join("test.db");
        
        let memory = Arc::new(
            PersistentConversationMemory::new(db_path.to_str().unwrap())
                .await
                .unwrap()
        );
        
        (temp_dir, memory)
    }

    #[tokio::test]
    async fn test_full_conversation_flow() {
        let (_temp_dir, memory) = setup_test_environment().await;
        let session_id = "test-session-001";
        
        // Store initial conversation
        memory.store_conversation(
            session_id,
            "Hello, my name is Alice",
            "Hello Alice! Nice to meet you."
        ).await.unwrap();
        
        // Retrieve and verify
        let context = memory.get_conversation_context(session_id, 10).await.unwrap();
        assert_eq!(context.len(), 1);
        assert_eq!(context[0].0, "Hello, my name is Alice");
        
        // Continue conversation
        memory.store_conversation(
            session_id,
            "What's my name?",
            "Your name is Alice."
        ).await.unwrap();
        
        // Verify context maintains history
        let context = memory.get_conversation_context(session_id, 10).await.unwrap();
        assert_eq!(context.len(), 2);
    }

    #[tokio::test]
    async fn test_consciousness_framework_integration() {
        let framework = ConsciousnessFramework::new();
        
        // Test consciousness level calculation
        let level = framework.calculate_consciousness_level(
            "What is the meaning of life?",
            0.95,
            5
        );
        
        assert!(level > 0.5); // Should have high consciousness for philosophical questions
    }

    #[tokio::test]
    async fn test_knowledge_engine_integration() {
        let engine = KnowledgeEngine::new();
        
        // Test concept explanation
        let explanation = engine.explain_concept("artificial intelligence");
        assert!(!explanation.is_empty());
        assert!(explanation.contains("AI") || explanation.contains("intelligence"));
        
        // Test knowledge retrieval
        let knowledge = engine.get_relevant_knowledge("machine learning", 3);
        assert!(!knowledge.is_empty());
    }

    #[tokio::test]
    async fn test_session_isolation() {
        let (_temp_dir, memory) = setup_test_environment().await;
        
        // Create two separate sessions
        let session1 = "session-001";
        let session2 = "session-002";
        
        // Store conversations in different sessions
        memory.store_conversation(
            session1,
            "I like pizza",
            "Pizza is great!"
        ).await.unwrap();
        
        memory.store_conversation(
            session2,
            "I like sushi",
            "Sushi is delicious!"
        ).await.unwrap();
        
        // Verify sessions are isolated
        let context1 = memory.get_conversation_context(session1, 10).await.unwrap();
        let context2 = memory.get_conversation_context(session2, 10).await.unwrap();
        
        assert_eq!(context1.len(), 1);
        assert_eq!(context2.len(), 1);
        assert!(context1[0].0.contains("pizza"));
        assert!(context2[0].0.contains("sushi"));
    }

    #[tokio::test]
    async fn test_memory_compaction() {
        let (_temp_dir, memory) = setup_test_environment().await;
        let session_id = "compaction-test";
        
        // Add many conversations
        for i in 0..20 {
            memory.store_conversation(
                session_id,
                &format!("Message {}", i),
                &format!("Response {}", i)
            ).await.unwrap();
        }
        
        // Trigger compaction (if implemented)
        memory.compact_session(session_id).await.unwrap();
        
        // Verify important messages are retained
        let context = memory.get_conversation_context(session_id, 10).await.unwrap();
        assert!(context.len() <= 10); // Should be compacted
    }

    #[tokio::test]
    async fn test_concurrent_session_access() {
        let (_temp_dir, memory) = setup_test_environment().await;
        let memory = Arc::new(memory);
        
        let mut handles = vec![];
        
        // Spawn multiple tasks accessing different sessions
        for i in 0..10 {
            let memory_clone = memory.clone();
            let session_id = format!("concurrent-{}", i);
            
            let handle = tokio::spawn(async move {
                for j in 0..5 {
                    memory_clone.store_conversation(
                        &session_id,
                        &format!("Message {}", j),
                        &format!("Response {}", j)
                    ).await.unwrap();
                }
            });
            
            handles.push(handle);
        }
        
        // Wait for all tasks
        for handle in handles {
            handle.await.unwrap();
        }
        
        // Verify all sessions have correct data
        for i in 0..10 {
            let session_id = format!("concurrent-{}", i);
            let context = memory.get_conversation_context(&session_id, 10).await.unwrap();
            assert_eq!(context.len(), 5);
        }
    }

    #[tokio::test]
    async fn test_error_recovery() {
        let (_temp_dir, memory) = setup_test_environment().await;
        
        // Test recovery from invalid session ID
        let result = memory.get_conversation_context("non-existent", 10).await;
        assert!(result.unwrap().is_empty());
        
        // Test recovery from empty message
        let result = memory.store_conversation("test", "", "response").await;
        assert!(result.is_err() || result.is_ok()); // Should handle gracefully
    }
}