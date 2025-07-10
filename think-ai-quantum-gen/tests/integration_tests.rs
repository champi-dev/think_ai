use think_ai_quantum_gen::{QuantumGenerationEngine, GenerationRequest, ThreadType};
use think_ai_knowledge::KnowledgeEngine;
use std::sync::Arc;
use tokio;
use std::time::Instant;

#[tokio::test]
async fn test_quantum_generation_with_qwen() {
    // Initialize knowledge engine
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    // Create quantum generation engine
    let engine = match QuantumGenerationEngine::new(knowledge_engine.clone()).await {
        Ok(e) => e,
        Err(e) => {
            eprintln!("Skipping test - Qwen not available: {}", e);
            return;
        }
    };
    
    // Test single generation
    let request = GenerationRequest {
        query: "What is consciousness?".to_string(),
        context_id: None,
        thread_type: ThreadType::UserChat,
        temperature: Some(0.7),
        max_tokens: None,
    };
    
    let start = Instant::now();
    let response = engine.generate(request).await.unwrap();
    let duration = start.elapsed();
    
    println!("Single generation test:");
    println!("  Response: {}", response.text);
    println!("  Context ID: {}", response.context_id);
    println!("  Thread ID: {}", response.thread_id);
    println!("  Generation time: {}ms", response.generation_time_ms);
    println!("  Total time: {:?}", duration);
    println!("  Model: {}", response.model_used);
    
    assert!(!response.text.is_empty());
    assert_eq!(response.model_used, "qwen2.5:1.5b");
}

#[tokio::test]
async fn test_parallel_generation_with_isolation() {
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    let engine = match QuantumGenerationEngine::new(knowledge_engine.clone()).await {
        Ok(e) => e,
        Err(e) => {
            eprintln!("Skipping test - Qwen not available: {}", e);
            return;
        }
    };
    
    // Create multiple requests with different thread types
    let requests = vec![
        GenerationRequest {
            query: "Explain quantum entanglement".to_string(),
            context_id: None,
            thread_type: ThreadType::UserChat,
            temperature: Some(0.7),
            max_tokens: None,
        },
        GenerationRequest {
            query: "What are the implications of consciousness?".to_string(),
            context_id: None,
            thread_type: ThreadType::Thinking,
            temperature: Some(0.8),
            max_tokens: None,
        },
        GenerationRequest {
            query: "Describe the nature of reality".to_string(),
            context_id: None,
            thread_type: ThreadType::Dreaming,
            temperature: Some(0.9),
            max_tokens: None,
        },
    ];
    
    let start = Instant::now();
    let responses = engine.generate_parallel(requests).await.unwrap();
    let duration = start.elapsed();
    
    println!("\nParallel generation test:");
    println!("  Total responses: {}", responses.len());
    println!("  Total time: {:?}", duration);
    
    for (i, response) in responses.iter().enumerate() {
        println!("\n  Response {}:", i + 1);
        println!("    Text: {}", response.text);
        println!("    Context ID: {}", response.context_id);
        println!("    Thread ID: {}", response.thread_id);
        println!("    Generation time: {}ms", response.generation_time_ms);
    }
    
    // Verify all responses are unique and from different threads
    assert_eq!(responses.len(), 3);
    let thread_ids: Vec<_> = responses.iter().map(|r| r.thread_id).collect();
    let unique_threads: std::collections::HashSet<_> = thread_ids.iter().collect();
    assert_eq!(unique_threads.len(), 3, "Each response should use a different thread");
}

#[tokio::test]
async fn test_context_persistence() {
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    let engine = match QuantumGenerationEngine::new(knowledge_engine.clone()).await {
        Ok(e) => e,
        Err(e) => {
            eprintln!("Skipping test - Qwen not available: {}", e);
            return;
        }
    };
    
    // First request creates a context
    let request1 = GenerationRequest {
        query: "My name is Alice".to_string(),
        context_id: None,
        thread_type: ThreadType::UserChat,
        temperature: Some(0.7),
        max_tokens: None,
    };
    
    let response1 = engine.generate(request1).await.unwrap();
    let context_id = response1.context_id;
    
    // Second request uses the same context
    let request2 = GenerationRequest {
        query: "What is my name?".to_string(),
        context_id: Some(context_id),
        thread_type: ThreadType::UserChat,
        temperature: Some(0.7),
        max_tokens: None,
    };
    
    let response2 = engine.generate(request2).await.unwrap();
    
    println!("\nContext persistence test:");
    println!("  First response: {}", response1.text);
    println!("  Second response: {}", response2.text);
    println!("  Same context: {}", response2.context_id == context_id);
    
    assert_eq!(response2.context_id, context_id);
    // The response should demonstrate awareness of the previous interaction
    // (actual validation depends on Qwen's response)
}

#[tokio::test]
async fn test_shared_intelligence() {
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    let engine = match QuantumGenerationEngine::new(knowledge_engine.clone()).await {
        Ok(e) => e,
        Err(e) => {
            eprintln!("Skipping test - Qwen not available: {}", e);
            return;
        }
    };
    
    // Generate responses that should build shared intelligence
    let learning_requests = vec![
        GenerationRequest {
            query: "The speed of light is 299,792,458 meters per second".to_string(),
            context_id: None,
            thread_type: ThreadType::KnowledgeCreation,
            temperature: Some(0.5),
            max_tokens: None,
        },
        GenerationRequest {
            query: "Einstein's theory of relativity relates to the speed of light".to_string(),
            context_id: None,
            thread_type: ThreadType::Training,
            temperature: Some(0.5),
            max_tokens: None,
        },
    ];
    
    // Process learning requests
    for request in learning_requests {
        engine.generate(request).await.unwrap();
    }
    
    // Now ask a related question
    let test_request = GenerationRequest {
        query: "What is the speed of light and its significance?".to_string(),
        context_id: None,
        thread_type: ThreadType::UserChat,
        temperature: Some(0.7),
        max_tokens: None,
    };
    
    let response = engine.generate(test_request).await.unwrap();
    
    println!("\nShared intelligence test:");
    println!("  Response: {}", response.text);
    
    // The response should incorporate the shared knowledge
    assert!(!response.text.is_empty());
}

#[tokio::test]
async fn test_cache_performance() {
    let knowledge_engine = Arc::new(KnowledgeEngine::new());
    
    let engine = match QuantumGenerationEngine::new(knowledge_engine.clone()).await {
        Ok(e) => e,
        Err(e) => {
            eprintln!("Skipping test - Qwen not available: {}", e);
            return;
        }
    };
    
    let request = GenerationRequest {
        query: "What is the meaning of life?".to_string(),
        context_id: None,
        thread_type: ThreadType::UserChat,
        temperature: Some(0.7),
        max_tokens: None,
    };
    
    // First request (not cached)
    let start1 = Instant::now();
    let response1 = engine.generate(request.clone()).await.unwrap();
    let duration1 = start1.elapsed();
    
    // Second request (should be cached)
    let start2 = Instant::now();
    let response2 = engine.generate(request).await.unwrap();
    let duration2 = start2.elapsed();
    
    println!("\nCache performance test:");
    println!("  First request: {:?}", duration1);
    println!("  Second request (cached): {:?}", duration2);
    println!("  Speedup: {:.2}x", duration1.as_millis() as f64 / duration2.as_millis() as f64);
    
    assert_eq!(response1.text, response2.text);
    assert!(duration2 < duration1, "Cached request should be faster");
}