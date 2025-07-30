// Core tests

use super::*;

#[tokio::test]
async fn test_engine_initialization() {
    let engine = O1Engine::new(EngineConfig::default());
    assert!(engine.initialize().await.is_ok());

    let stats = engine.stats();
    assert!(stats.initialized);
    assert_eq!(stats.operation_count, 0);
}

#[tokio::test]
async fn test_o1_operations() {
    let engine = O1Engine::new(EngineConfig::default());

    let result = ComputeResult {
        value: serde_json::json!({"answer": 42}),
        metadata: serde_json::json!({"source": "test"}),
    };

    engine.store("test_key", result.clone()).await.unwrap();

    let retrieved = engine.compute("test_key").await;
    assert!(retrieved.is_some());
    let retrieved_result = retrieved.unwrap();
    assert_eq!(retrieved_result.value, result.value);

    let stats = engine.stats();
    assert_eq!(stats.operation_count, 1);
    assert_eq!(stats.cache_size, 1);
}
