use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};
use think_ai_core::{O1Engine, EngineConfig, ComputeResult};
use std::collections::HashMap;

/// Benchmark O(1) cache operations with varying data sizes
fn benchmark_o1_operations(c: &mut Criterion) {
    let mut group = c.benchmark_group("O1 Performance");
    
    // Test with different cache sizes to verify O(1) behavior
    for size in [1000, 10_000, 100_000, 1_000_000].iter() {
        let config = EngineConfig {
            cache_size: *size,
            ..Default::default()
        };
        
        let engine = O1Engine::new(config);
        
        // Pre-populate cache
        for i in 0..*size / 2 {
            let key = format!("key_{}", i);
            let result = ComputeResult {
                value: serde_json::json!({ "data": i }),
                metadata: serde_json::json!({ "timestamp": i }),
            };
            engine.store(&key, result).unwrap();
        }
        
        // Benchmark lookups - should be constant time regardless of cache size
        group.bench_with_input(
            BenchmarkId::new("lookup", size),
            size,
            |b, _| {
                let key = "key_42";
                b.iter(|| {
                    black_box(engine.compute(black_box(key)));
                });
            },
        );
        
        // Benchmark insertions - should also be constant time
        group.bench_with_input(
            BenchmarkId::new("insert", size),
            size,
            |b, _| {
                let mut counter = 0;
                b.iter(|| {
                    let key = format!("new_key_{}", counter);
                    let result = ComputeResult {
                        value: serde_json::json!({ "data": counter }),
                        metadata: serde_json::json!({ "timestamp": counter }),
                    };
                    engine.store(&key, result).unwrap();
                    counter += 1;
                });
            },
        );
    }
    
    group.finish();
}

/// Compare O(1) engine with standard HashMap to show performance advantage
fn benchmark_comparison(c: &mut Criterion) {
    let mut group = c.benchmark_group("O1 vs HashMap");
    
    let size = 100_000;
    let config = EngineConfig {
        cache_size: size,
        ..Default::default()
    };
    
    let o1_engine = O1Engine::new(config);
    let mut hashmap = HashMap::with_capacity(size);
    
    // Pre-populate both
    for i in 0..size / 2 {
        let key = format!("key_{}", i);
        let result = ComputeResult {
            value: serde_json::json!({ "data": i }),
            metadata: serde_json::json!({ "timestamp": i }),
        };
        
        o1_engine.store(&key, result.clone()).unwrap();
        hashmap.insert(key, result);
    }
    
    // Compare lookup performance
    group.bench_function("O1_lookup", |b| {
        b.iter(|| {
            let key = "key_42";
            black_box(o1_engine.compute(black_box(key)));
        });
    });
    
    group.bench_function("HashMap_lookup", |b| {
        b.iter(|| {
            let key = "key_42";
            black_box(hashmap.get(black_box(key)));
        });
    });
    
    group.finish();
}

/// Verify O(1) scaling - time should remain constant as N increases
fn benchmark_scaling_verification(c: &mut Criterion) {
    let mut group = c.benchmark_group("Scaling Verification");
    group.sample_size(1000); // More samples for accurate measurement
    
    // Create engines with different sizes and measure lookup time
    let sizes = vec![1000, 10_000, 100_000, 1_000_000];
    let mut timings = Vec::new();
    
    for size in &sizes {
        let config = EngineConfig {
            cache_size: *size,
            ..Default::default()
        };
        
        let engine = O1Engine::new(config);
        
        // Fill to 80% capacity
        for i in 0..(*size * 8 / 10) {
            let key = format!("key_{}", i);
            let result = ComputeResult {
                value: serde_json::json!({ "data": i }),
                metadata: serde_json::json!({ "timestamp": i }),
            };
            engine.store(&key, result).unwrap();
        }
        
        // Measure lookup time
        let start = std::time::Instant::now();
        for _ in 0..10000 {
            engine.compute("key_42");
        }
        let elapsed = start.elapsed();
        timings.push(elapsed.as_nanos() / 10000);
        
        group.bench_with_input(
            BenchmarkId::new("scaling", size),
            size,
            |b, _| {
                b.iter(|| {
                    black_box(engine.compute(black_box("key_42")));
                });
            },
        );
    }
    
    // Print scaling analysis
    println!("\n=== O(1) Scaling Analysis ===");
    for (i, (size, timing)) in sizes.iter().zip(timings.iter()).enumerate() {
        println!("Size: {:>10} | Avg lookup time: {:>6} ns", size, timing);
        if i > 0 {
            let ratio = *timing as f64 / timings[0] as f64;
            println!("  Ratio to smallest: {:.2}x (should be ~1.0x for O(1))", ratio);
        }
    }
    
    group.finish();
}

criterion_group!(
    benches,
    benchmark_o1_operations,
    benchmark_comparison,
    benchmark_scaling_verification
);
criterion_main!(benches);