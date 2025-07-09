#!/bin/bash
set -e

echo "🔧 Fixing all remaining syntax errors..."

# Fix train-comprehensive.rs
echo "Fixing train-comprehensive.rs..."
sed -i '57s/",/");/' think-ai-cli/src/bin/train-comprehensive.rs

# Fix commands/mod.rs
echo "Fixing commands/mod.rs..."
cat > /tmp/fix-commands.py << 'EOF'
import re

# Read the file
with open('think-ai-cli/src/commands/mod.rs', 'r') as f:
    content = f.read()

# Find the problematic section around line 397-403
lines = content.split('\n')
fixed_lines = []
i = 0

while i < len(lines):
    line = lines[i]
    
    # Fix the unclosed delimiter issue around line 398-403
    if "if let Ok(Some(checkpoint)) = persistence.load_latest_checkpoint()" in line:
        fixed_lines.append(line)
        # Add proper closing for the if block
        j = i + 1
        while j < len(lines) and not lines[j].strip().startswith('}'):
            fixed_lines.append(lines[j])
            j += 1
        if j < len(lines):
            fixed_lines.append(lines[j])  # Add the closing }
        i = j
    elif "} else if let Ok(persistence) =" in line:
        # This line has mismatched delimiter, fix it
        fixed_lines.append("                }")
        i += 1
    else:
        fixed_lines.append(line)
        i += 1

# Write back
with open('think-ai-cli/src/commands/mod.rs', 'w') as f:
    f.write('\n'.join(fixed_lines))
EOF
python3 /tmp/fix-commands.py

# Fix o1_performance.rs benchmark
echo "Fixing o1_performance.rs benchmark..."
sed -i '/group.bench_with_input.*"insert"/{N;s/|b, _| {/|b, _| {\n            b.iter(|| {/;}' think-ai-core/benches/o1_performance.rs
sed -i '/black_box(o1_engine.compute(black_box(key)));/{N;s/});/            });\n        });/;}' think-ai-core/benches/o1_performance.rs

# Fix o1_integration.rs test
echo "Fixing o1_integration.rs test..."
sed -i '/assert!(/,/);/{:a;N;/);/!ba;s/assert!(\n/assert!(/;}' think-ai-core/tests/o1_integration.rs

# Fix quantum_llm_integration.rs test
echo "Fixing quantum_llm_integration.rs test..."
echo "}" >> think-ai-knowledge/tests/quantum_llm_integration.rs

# Fix benchmark.rs in qwen
echo "Fixing qwen benchmark.rs..."
cat >> think-ai-qwen/benches/benchmark.rs << 'EOF'
    });
}

criterion_group! {
    name = benches;
    config = Criterion::default();
    targets = benchmark_qwen_generation
}

criterion_main!(benches);
EOF

# Run cargo fmt on individual files that can be formatted
echo "Running targeted cargo fmt..."
for file in \
    think-ai-cli/src/bin/train-comprehensive.rs \
    think-ai-core/tests/o1_integration.rs \
    think-ai-knowledge/tests/quantum_llm_integration.rs \
    think-ai-qwen/benches/benchmark.rs
do
    if [ -f "$file" ]; then
        cargo fmt -- "$file" 2>/dev/null || echo "  Could not format $file"
    fi
done

echo "✅ Syntax fixes applied!"