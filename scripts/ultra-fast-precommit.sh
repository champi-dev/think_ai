#!/bin/bash
# Ultra-Fast Pre-commit Pipeline
# Target: <10s execution time with aggressive caching

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🚀 Think AI Ultra-Fast Pre-commit Pipeline"
echo "========================================="

# Kill any existing processes on our ports
echo "🔧 Cleaning up ports..."
lsof -ti:8080 | xargs -r kill -9 2>/dev/null || true
lsof -ti:3000 | xargs -r kill -9 2>/dev/null || true

# Run Rust formatting and linting in parallel
echo "📋 Running Rust checks..."
(
    cd "$PROJECT_ROOT"
    cargo fmt --all -- --check &
    RUST_FMT_PID=$!
    
    cargo clippy --all-targets --all-features -- -D warnings &
    RUST_CLIPPY_PID=$!
    
    wait $RUST_FMT_PID $RUST_CLIPPY_PID
)

# Quick build check (debug mode for speed)
echo "🔨 Quick build check..."
cd "$PROJECT_ROOT"
cargo check --all

# Run fast unit tests only (skip integration tests)
echo "🧪 Running fast tests..."
cargo test --lib --bins -- --test-threads=8

echo "✅ Pre-commit checks passed!"
echo "Total time: ${SECONDS}s"