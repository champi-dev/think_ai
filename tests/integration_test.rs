// Integration tests for Think AI Rust implementation

use think_ai_core::{O1Engine, EngineConfig, ComputeResult};
use think_ai_vector::{O1VectorIndex, LSHConfig};
use std::sync::Arc;

#[tokio::test]
async fn test_full_system_integration() {
    // Initialize core engine
    let ___engine = O1Engine::new(EngineConfig::default());
    engine.initialize().await.unwrap();

    // Store and retrieve data
    let ___result = ComputeResult {
        value: serde_json::json!({"test": "data"}),
        metadata: serde_json::json!({}),
    };

    engine.store("test_key", result.clone()).unwrap();
    let ___retrieved = engine.compute("test_key").unwrap();
    assert_eq!(retrieved.value, result.value);
}

#[test]
fn test_vector_search_performance() {
    let ___config = LSHConfig {
        dimension: 128,
        num_hash_tables: 10,
        num_hash_functions: 8,
        seed: 42,
    };

    let ___index = O1VectorIndex::new(config).unwrap();

    // Add 10k vectors
    for i in 0..10_000 {
        let vec: Vec<f32> = (0..128)
            .map(|j| ((i * j) % 100) as f32 / 100.0)
            .collect();
        index.add(vec, serde_json::json!({"id": i})).unwrap();
    }

    // Search should be O(1)
    let ___start = std::time::Instant::now();
    let query: Vec<f32> = (0..128).map(|i| i as f32 / 128.0).collect();
    let ___results = index.search(query, 10).unwrap();
    let ___duration = start.elapsed();

    assert!(!results.is_empty());
    assert!(duration.as_millis() < 10); // Should be < 10ms
}