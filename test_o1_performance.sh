#!/bin/bash

echo "=== Think AI O(1) Performance Test ==="
echo ""

# Build in release mode
echo "Building project..."
cargo build --release -p think-ai-core

# Run integration tests
echo ""
echo "Running O(1) integration tests..."
cargo test --release -p think-ai-core o1_integration -- --nocapture

# Run benchmarks (if available)
if [ -f "think-ai-core/benches/o1_performance.rs" ]; then
    echo ""
    echo "Running performance benchmarks..."
    cargo bench -p think-ai-core --bench o1_performance -- --quick
fi

echo ""
echo "✓ Performance testing complete!"
