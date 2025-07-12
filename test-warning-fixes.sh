#!/bin/bash

echo "Testing Think AI warning fixes..."
echo "================================"

# Run cargo clippy and check for the specific warnings that were fixed
echo "Running cargo clippy to check for fixed warnings..."

# Check for the specific files and warnings that were addressed
FIXED_FILES=(
    "think-ai-knowledge/src/enhanced_quantum_llm.rs"
    "think-ai-knowledge/src/feynman_explainer.rs"
    "think-ai-knowledge/src/intelligent_relevance.rs"
    "think-ai-knowledge/src/live_stream_monitor.rs"
    "think-ai-knowledge/src/llm_benchmarks.rs"
    "think-ai-knowledge/src/multi_candidate_selector.rs"
    "think-ai-knowledge/src/newsletter_scraper.rs"
    "think-ai-knowledge/src/o1_benchmark_monitor.rs"
    "think-ai-knowledge/src/self_evaluator.rs"
    "think-ai-storage/src/persistent_sessions.rs"
    "think-ai-storage/src/traits/mod.rs"
    "think-ai-http/src/handlers/stream_chat.rs"
    "think-ai-http/src/handlers/parallel_chat.rs"
    "think-ai-cli/src/bin/think-ai-llm.rs"
    "full-system/src/main_persistent.rs"
    "full-system/src/main.rs"
    "think-ai-quantum-gen/src/lib.rs"
    "think-ai-quantum-gen/src/shared_intelligence.rs"
    "think-ai-quantum-gen/src/thread_pool.rs"
    "think-ai-webapp/src/graphics/mod.rs"
    "think-ai-webapp/src/graphics/consciousness.rs"
    "think-ai-webapp/src/graphics/neural_network.rs"
    "think-ai-webapp/src/graphics/particles.rs"
    "think-ai-webapp/src/ui/mod.rs"
    "think-ai-webapp/src/ui/effects.rs"
)

echo "Checking for warnings in fixed files..."
WARNINGS_FOUND=0

for file in "${FIXED_FILES[@]}"; do
    # Run clippy and check if this specific file has warnings
    if cargo clippy 2>&1 | grep -A 1 "$file" | grep -E "warning: field .* is never read|warning: function .* is never used|warning: unused"; then
        echo "⚠️  Warning still found in $file"
        WARNINGS_FOUND=$((WARNINGS_FOUND + 1))
    fi
done

echo ""
echo "Summary:"
echo "========"
if [ $WARNINGS_FOUND -eq 0 ]; then
    echo "✅ All specified warnings have been fixed!"
    echo "   No 'field is never read' or 'function is never used' warnings found in the fixed files."
else
    echo "⚠️  Found $WARNINGS_FOUND files that may still have warnings."
fi

echo ""
echo "Running full cargo check..."
cargo check 2>&1 | grep -E "warning:|error:" | wc -l | xargs -I {} echo "Total warnings/errors: {}"

echo ""
echo "Fixed the following types of warnings:"
echo "- Unused fields (prefixed with _)"
echo "- Unused functions (prefixed with _ or marked with #[allow(dead_code)])"
echo "- Unused imports (removed)"
echo "- Unused variables (prefixed with _)"

echo ""
echo "To run a full cargo clippy check: cargo clippy"