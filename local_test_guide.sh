#!/bin/bash

echo "🧪 Think AI Benchmark System - Local Testing Guide"
echo "=================================================="

# Step 1: Add required dependencies
echo "📦 Step 1: Adding required dependencies to Cargo.toml..."

# Check if we need to add dependencies
if ! grep -q "clap" Cargo.toml; then
    echo "Adding missing dependencies..."
    cat >> Cargo.toml << 'EOF'

# CLI dependencies
clap = "2.34"
ctrlc = "3.4"
tokio = { version = "1.0", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
EOF
fi

echo "✅ Dependencies configured"

# Step 2: Build the project
echo ""
echo "🔨 Step 2: Building the project..."
cargo build --release --bin simple_benchmark_demo

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed. Let's try a simpler approach..."
    echo "Building just the core library..."
    cargo build --lib
fi

# Step 3: Run tests
echo ""
echo "🧪 Step 3: Running unit tests..."
cargo test --lib llm_benchmarks

echo ""
echo "📊 Step 4: Available test commands:"
echo ""
echo "Basic functionality tests:"
echo "  cargo test --lib                                    # Run all unit tests"
echo "  cargo test llm_benchmarks                          # Test benchmark framework"
echo "  cargo test benchmark_trainer                       # Test training pipeline"
echo ""
echo "If the build succeeds, run the demo:"
echo "  cargo run --release --bin simple_benchmark_demo    # Full benchmark demo"
echo ""
echo "Manual testing approaches:"
echo "  1. Test individual modules with 'cargo test <module_name>'"
echo "  2. Use 'cargo check' to verify compilation without running"
echo "  3. Run 'cargo doc --open' to view generated documentation"
echo ""
echo "🔍 Troubleshooting:"
echo "If you get compilation errors:"
echo "  1. Run 'cargo clean' first"
echo "  2. Check Rust version: 'rustc --version' (needs 1.70+)"
echo "  3. Update dependencies: 'cargo update'"
echo ""