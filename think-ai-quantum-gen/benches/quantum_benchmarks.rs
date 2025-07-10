use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion};
use std::sync::Arc;
use think_ai_knowledge::KnowledgeEngine;
use think_ai_quantum_gen::{GenerationRequest, QuantumGenerationEngine, ThreadType};
use tokio::runtime::Runtime;

fn benchmark_single_generation(c: &mut Criterion) {
    let rt = Runtime::new().unwrap();

    // Initialize engine once
    let engine = rt.block_on(async {
        let knowledge_engine = Arc::new(KnowledgeEngine::new());
        match QuantumGenerationEngine::new(knowledge_engine).await {
            Ok(e) => Some(Arc::new(e)),
            Err(_) => {
                eprintln!("Skipping benchmarks - Qwen not available");
                None
            }
        }
    });

    if let Some(engine) = engine {
        let mut group = c.benchmark_group("quantum_generation");

        // Benchmark single generation
        group.bench_function("single_generation", |b| {
            b.to_async(&rt).iter(|| async {
                let request = GenerationRequest {
                    query: black_box("What is consciousness?".to_string()),
                    context_id: None,
                    thread_type: ThreadType::UserChat,
                    temperature: Some(0.7),
                    max_tokens: None,
                };

                engine.generate(request).await.unwrap()
            });
        });

        group.finish();
    }
}

fn benchmark_cache_performance(c: &mut Criterion) {
    let rt = Runtime::new().unwrap();

    let engine = rt.block_on(async {
        let knowledge_engine = Arc::new(KnowledgeEngine::new());
        match QuantumGenerationEngine::new(knowledge_engine).await {
            Ok(e) => Some(Arc::new(e)),
            Err(_) => None,
        }
    });

    if let Some(engine) = engine {
        let mut group = c.benchmark_group("cache_performance");

        // Prepare requests with different cache hit scenarios
        let queries = vec![
            "What is love?",          // Will be cached
            "What is the universe?",  // Will be cached
            "What is consciousness?", // Will be cached
        ];

        // Pre-warm the cache
        rt.block_on(async {
            for query in &queries {
                let request = GenerationRequest {
                    query: query.to_string(),
                    context_id: None,
                    thread_type: ThreadType::UserChat,
                    temperature: Some(0.7),
                    max_tokens: None,
                };
                let _ = engine.generate(request).await;
            }
        });

        // Benchmark cache hits (should be O(1))
        group.bench_function("cache_hit", |b| {
            b.to_async(&rt).iter(|| async {
                let request = GenerationRequest {
                    query: black_box(queries[0].to_string()),
                    context_id: None,
                    thread_type: ThreadType::UserChat,
                    temperature: Some(0.7),
                    max_tokens: None,
                };

                engine.generate(request).await.unwrap()
            });
        });

        // Benchmark cache misses
        let mut counter = 0;
        group.bench_function("cache_miss", |b| {
            b.to_async(&rt).iter(|| async {
                counter += 1;
                let request = GenerationRequest {
                    query: black_box(format!("Random query {}", counter)),
                    context_id: None,
                    thread_type: ThreadType::UserChat,
                    temperature: Some(0.7),
                    max_tokens: None,
                };

                engine.generate(request).await.unwrap()
            });
        });

        group.finish();
    }
}

fn benchmark_parallel_generation(c: &mut Criterion) {
    let rt = Runtime::new().unwrap();

    let engine = rt.block_on(async {
        let knowledge_engine = Arc::new(KnowledgeEngine::new());
        match QuantumGenerationEngine::new(knowledge_engine).await {
            Ok(e) => Some(Arc::new(e)),
            Err(_) => None,
        }
    });

    if let Some(engine) = engine {
        let mut group = c.benchmark_group("parallel_generation");

        for size in [1, 2, 4, 8, 16].iter() {
            group.bench_with_input(BenchmarkId::from_parameter(size), size, |b, &size| {
                b.to_async(&rt).iter(|| async {
                    let requests: Vec<_> = (0..size)
                        .map(|i| GenerationRequest {
                            query: black_box(format!("Query number {}", i)),
                            context_id: None,
                            thread_type: match i % 3 {
                                0 => ThreadType::UserChat,
                                1 => ThreadType::Thinking,
                                _ => ThreadType::Dreaming,
                            },
                            temperature: Some(0.7),
                            max_tokens: None,
                        })
                        .collect();

                    engine.generate_parallel(requests).await.unwrap()
                });
            });
        }

        group.finish();
    }
}

fn benchmark_context_operations(c: &mut Criterion) {
    let rt = Runtime::new().unwrap();

    let engine = rt.block_on(async {
        let knowledge_engine = Arc::new(KnowledgeEngine::new());
        match QuantumGenerationEngine::new(knowledge_engine).await {
            Ok(e) => Some(Arc::new(e)),
            Err(_) => None,
        }
    });

    if let Some(engine) = engine {
        let mut group = c.benchmark_group("context_operations");

        // Create a context
        let context_id = rt.block_on(async {
            let request = GenerationRequest {
                query: "Initialize context".to_string(),
                context_id: None,
                thread_type: ThreadType::UserChat,
                temperature: Some(0.7),
                max_tokens: None,
            };

            engine.generate(request).await.unwrap().context_id
        });

        // Benchmark generation with existing context
        group.bench_function("with_context", |b| {
            b.to_async(&rt).iter(|| async {
                let request = GenerationRequest {
                    query: black_box("Continue conversation".to_string()),
                    context_id: Some(black_box(context_id)),
                    thread_type: ThreadType::UserChat,
                    temperature: Some(0.7),
                    max_tokens: None,
                };

                engine.generate(request).await.unwrap()
            });
        });

        group.finish();
    }
}

criterion_group!(
    benches,
    benchmark_single_generation,
    benchmark_cache_performance,
    benchmark_parallel_generation,
    benchmark_context_operations
);
criterion_main!(benches);
