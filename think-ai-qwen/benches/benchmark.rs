use criterion::{criterion_group, criterion_main, Criterion};
use std::time::Duration;
use think_ai_qwen::{KnowledgeResponse, QwenConfig, QwenOrchestrator, QwenRequest};
use tokio::runtime::Runtime;

fn benchmark_qwen_generation(c: &mut Criterion) {
    let rt = Runtime::new().unwrap();

    let config = QwenConfig {
        api_key: std::env::var("HUGGINGFACE_API_KEY")
            .unwrap_or_else(|_| "YOUR_HUGGINGFACE_TOKEN_HERE".to_string()),
        model_id: "Qwen/Qwen2.5-Coder-32B-Instruct".to_string(),
        max_tokens: 512,
        temperature: 0.7,
        top_p: 0.9,
        timeout_secs: 30,
        cache_enabled: true,
        cache_ttl_secs: 3600,
    };

    let orchestrator = QwenOrchestrator::new(config).unwrap();

    c.bench_function("qwen_generation_no_knowledge", |b| {
        b.to_async(&rt).iter(|| async {
            let request = QwenRequest {
                query: "What is Rust programming language?".to_string(),
                context: None,
                system_prompt: None,
            };

            orchestrator
                .process_request(request, |_| Box::pin(async { None }))
                .await
        })
    });

    c.bench_function("qwen_generation_with_knowledge", |b| {
        b.to_async(&rt).iter(|| async {
            let request = QwenRequest {
                query: "Explain O(1) time complexity".to_string(),
                context: None,
                system_prompt: None,
            };

            orchestrator.process_request(request, |_| {
                Box::pin(async {
                    Some(KnowledgeResponse {
                        content: "O(1) denotes constant time complexity where operations complete in the same time regardless of input size.".to_string(),
                        confidence: 0.95,
                        sources: vec!["Algorithm Theory".to_string()],
                        response_time_ms: 5,
                    })
                })
            }).await
        })
    });

    // Benchmark cache hits
    c.bench_function("qwen_cache_hit", |b| {
        // Pre-populate cache
        rt.block_on(async {
            let request = QwenRequest {
                query: "Cache test query".to_string(),
                context: None,
                system_prompt: None,
            };

            let _ = orchestrator
                .process_request(request, |_| Box::pin(async { None }))
                .await;
        });

        b.to_async(&rt).iter(|| async {
            let request = QwenRequest {
                query: "Cache test query".to_string(),
                context: None,
                system_prompt: None,
            };

            orchestrator
                .process_request(request, |_| Box::pin(async { None }))
                .await
        })
    });
}

criterion_group! {
    name = benches;
    config = Criterion::default()
        .measurement_time(Duration::from_secs(30))
        .sample_size(10);
    targets = benchmark_qwen_generation
}

criterion_main!(benches);
