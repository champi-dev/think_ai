//! O(1) performance benchmarks for vector search

use criterion::{criterion_group, criterion_main, Criterion};
use think_ai_vector::{O1VectorIndex, LSHConfig};

fn benchmark_vector_search(c: &mut Criterion) {
    let config = LSHConfig {
        dimension: 384,
        num_hash_tables: 10,
        num_hash_functions: 8,
        seed: 42,
    };
    
    let index = O1VectorIndex::new(config).unwrap();
    
    // Add vectors
    for i in 0..10000 {
        let vec: Vec<f32> = (0..384)
            .map(|j| ((i * j) % 100) as f32 / 100.0)
            .collect();
        index.add(vec, serde_json::json!({"id": i})).unwrap();
    }
    
    // Benchmark search
    c.bench_function("o1_vector_search", |b| {
        let query: Vec<f32> = (0..384).map(|i| i as f32 / 384.0).collect();
        b.iter(|| {
            index.search(query.clone(), 10).unwrap()
        });
    });
}

criterion_group!(benches, benchmark_vector_search);
criterion_main!(benches);