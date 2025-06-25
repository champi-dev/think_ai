//! Core tests

use super::*;

#[tokio::test]
async fn test_engine_initialization() {
    let engine = O1Engine::new(EngineConfig::default());
    assert!(engine.initialize().await.is_ok());
    
    let stats = engine.stats();
    assert!(stats.initialized);
    assert_eq!(stats.operation_count, 0);
}

#[test]
fn test_o1_operations() {
    let engine = O1Engine::new(EngineConfig::default());
    
    let result = ComputeResult {
        value: serde_json::json!({"answer": 42}),
        metadata: serde_json::json!({"source": "test"}),
    };
    
    engine.store("test_key", result.clone()).unwrap();
    
    let retrieved = engine.compute("test_key").unwrap();
    assert_eq!(retrieved.value, result.value);
    
    let stats = engine.stats();
    assert_eq!(stats.operation_count, 1);
    assert_eq!(stats.cache_size, 1);
}