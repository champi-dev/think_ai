#!/bin/bash
set -e

echo "🔧 Final comprehensive syntax fix..."

# 1. Fix commands/mod.rs
echo "Fixing commands/mod.rs..."
cat > /tmp/fix-commands-final.py << 'EOF'
# Read the problematic section and fix it
with open('think-ai-cli/src/commands/mod.rs', 'r') as f:
    content = f.read()

# Replace the problematic section around line 397-403
content = content.replace(
    '''            {
                if let Ok(Some(checkpoint)) = persistence.load_latest_checkpoint() {
                    println!(
                        "✅ Loaded checkpoint with {} knowledge items",
                        checkpoint.len()
                    );
            } else if let Ok(persistence) =''',
    '''            if let Ok(persistence) = KnowledgePersistence::new("knowledge_checkpoint") {
                if let Ok(Some(checkpoint)) = persistence.load_latest_checkpoint() {
                    println!(
                        "✅ Loaded checkpoint with {} knowledge items",
                        checkpoint.len()
                    );
                }
            } else if let Ok(persistence) ='''
)

with open('think-ai-cli/src/commands/mod.rs', 'w') as f:
    f.write(content)
EOF
python3 /tmp/fix-commands-final.py

# 2. Fix o1_performance.rs benchmark
echo "Fixing o1_performance.rs benchmark..."
cat > /tmp/fix-o1-perf.py << 'EOF'
with open('think-ai-core/benches/o1_performance.rs', 'r') as f:
    lines = f.readlines()

# Fix the bench_with_input section
fixed = []
for i, line in enumerate(lines):
    if "b.iter(|| {" in line and i > 30 and i < 35:
        # This is inside the bench_with_input, needs proper closure
        fixed.append(line)
        fixed.append("            });\n")
        fixed.append("        });\n")
        # Skip the next mismatched brace
        continue
    elif i > 0 and "});" in lines[i-1] and "});" in line:
        # Skip duplicate closing
        continue
    else:
        fixed.append(line)

with open('think-ai-core/benches/o1_performance.rs', 'w') as f:
    f.writelines(fixed)
EOF
python3 /tmp/fix-o1-perf.py

# 3. Fix o1_integration.rs test
echo "Fixing o1_integration.rs test..."
sed -i 's/assert!(        is_o1,/assert!(is_o1,/' think-ai-core/tests/o1_integration.rs

# 4. Fix quantum_llm_integration.rs - add missing brace
echo "Fixing quantum_llm_integration.rs..."
echo "}" >> think-ai-knowledge/tests/quantum_llm_integration.rs

# 5. Fix qwen benchmark.rs
echo "Fixing qwen benchmark.rs..."
cat > think-ai-qwen/benches/benchmark.rs << 'EOF'
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
                        Some(black_box("Use simple terms"))
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
EOF

echo "✅ All syntax fixes applied!"
echo "🔍 Running final check..."
cargo check --all 2>&1 | grep -E "(error:|warning:)" | head -20