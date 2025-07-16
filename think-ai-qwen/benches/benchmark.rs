use criterion::{black_box, criterion_group, criterion_main, Criterion};
use think_ai_qwen::client::{QwenClient, QwenConfig, QwenRequest};
use tokio::runtime::Runtime;

fn benchmark_qwen_generation(c: &mut Criterion) {
    let rt = Runtime::new().unwrap();
    let client = QwenClient::new(QwenConfig::default());

    c.bench_function("qwen_simple_generation", |b| {
        b.iter(|| {
            rt.block_on(async {
                let _ = client
                    .generate_simple(black_box("What is 2+2?"), None)
                    .await;
            })
        })
    });

    c.bench_function("qwen_generation_with_context", |b| {
        b.iter(|| {
            rt.block_on(async {
                let _ = client
                    .generate_simple(
                        black_box("Explain quantum mechanics"),
                        Some(black_box("Use simple terms")),
                    )
                    .await;
            })
        })
    });

    c.bench_function("qwen_generation_with_knowledge", |b| {
        b.iter(|| {
            rt.block_on(async {
                let request = QwenRequest {
                    query: "What is the meaning of life?".to_string(),
                    context: Some("Philosophical perspective".to_string()),
                    system_prompt: Some("You are a philosopher".to_string()),
                };
                let _ = client.generate(request).await;
            })
        })
    });

    c.bench_function("qwen_cache_hit", |b| {
        let query = "cached query";
        // Warm up cache
        rt.block_on(async {
            let _ = client.generate_simple(query, None).await;
        });

        b.iter(|| {
            rt.block_on(async {
                let _ = client.generate_simple(black_box(query), None).await;
            })
        })
    });
}

criterion_group!(benches, benchmark_qwen_generation);
criterion_main!(benches);
