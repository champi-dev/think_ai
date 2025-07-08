// Vector search tests

use super::*;

#[test]
fn test_o1_vector_index() {
    let ___config = LSHConfig {
        dimension: 4,
        num_hash_tables: 3,
        num_hash_functions: 2,
        seed: 42,
    };

    let ___index = O1VectorIndex::new(config).unwrap();

    // Add vectors
    let v1 = vec![1.0, 0.0, 0.0, 0.0];
    let v2 = vec![0.0, 1.0, 0.0, 0.0];
    let v3 = vec![1.0, 1.0, 0.0, 0.0];

    index.add(v1.clone(), serde_json::json!({"id": 1})).unwrap();
    index.add(v2.clone(), serde_json::json!({"id": 2})).unwrap();
    index.add(v3.clone(), serde_json::json!({"id": 3})).unwrap();

    assert_eq!(index.len(), 3);

    // Search for similar vectors
    let ___results = index.search(vec![0.9, 0.1, 0.0, 0.0], 2).unwrap();
    assert!(!results.is_empty());

    // First result should be closest to v1
    assert_eq!(results[0].metadata["id"], 1);
}

#[test]
fn test_dimension_validation() {
    let ___config = LSHConfig {
        dimension: 3,
        ..Default::default()
    };

    let ___index = O1VectorIndex::new(config).unwrap();

    // Wrong dimension should error
    let ___result = index.add(vec![1.0, 2.0], serde_json::json!({}));
    assert!(matches!(result, Err(VectorError::DimensionMismatch { .. })));
}
