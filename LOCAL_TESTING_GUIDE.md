# Think AI Rust - Local Testing Guide

## 🚀 Quick Start - Test Full System

### 1. Build Everything
```bash
# Build all modules in release mode for best performance
cargo build --workspace --release

# This creates optimized binaries in target/release/
```

### 2. Test Individual Components

#### Core Engine Test
```bash
# Test the O(1) hash-based core engine
cargo test --package think-ai-core -- --nocapture
```

#### Vector Search Test  
```bash
# Test LSH vector search with 100K vectors
cargo test --package think-ai-vector -- --nocapture
```

#### Process Manager Test
```bash
# Test UUID port allocation and service orchestration
cargo test --package think-ai-process-manager -- --nocapture
```

### 3. Run the O(1) Linter
```bash
# Analyze code for O(1) performance violations
./target/release/think-ai-lint . --extensions rs

# Test on specific files
./target/release/think-ai-lint think-ai-linter/tests/test_code.rs
```

### 4. Start the Process Manager
```bash
# Start all services with automatic port allocation
cargo run --bin process-manager

# Or use the release binary
./target/release/process-manager
```

### 5. Run the Main CLI
```bash
# Interactive CLI with all features
cargo run --bin think-ai

# Or release version
./target/release/think-ai
```

### 6. Start HTTP Server
```bash
# Start the main HTTP server
cargo run --bin think-ai-server

# Access at randomly generated UUID port (check logs)
```

## 🧪 Full System Integration Test

### Run Complete Test Suite
```bash
# Run all tests across all modules
cargo test --workspace -- --nocapture

# Run specific integration test
cargo test test_full_think_ai_system -- --nocapture
```

### Performance Benchmarks
```bash
# Run performance tests to verify O(1) guarantees
cargo test --release -- --nocapture | grep -E "(ns|μs|ms)"
```

## 📊 Real-World Usage Examples

### 1. Code Analysis
```bash
# Analyze your own Rust code for performance issues
./target/release/think-ai-lint /path/to/your/rust/project --fix

# Example output:
# 🚀 Think AI O(1) Linter
# File: src/main.rs
#   ⚠️  [O1_METHOD:42] Method 'contains' has O(n) complexity
```

### 2. Vector Search Demo
```bash
# Add this to test vector search capabilities
cargo run --example vector_demo --package think-ai-vector
```

### 3. Consciousness Framework
```bash
# Test ethical AI filtering
cargo run --example consciousness_demo --package think-ai-consciousness  
```

### 4. Code Generation
```bash
# Generate code in multiple languages
cargo run --example codegen_demo --package think-ai-coding
```

## 🔧 Development Workflow

### Watch Mode (auto-rebuild on changes)
```bash
# Install cargo-watch if you don't have it
cargo install cargo-watch

# Auto-rebuild and test on file changes
cargo watch -x "build --workspace" -x "test --workspace"
```

### Debug Mode
```bash
# Build with debug symbols for development
cargo build --workspace

# Run with debug logging
RUST_LOG=debug cargo run --bin think-ai-server
```

### Lint and Format
```bash
# Format all code
cargo fmt --all

# Run Clippy linter
cargo clippy --workspace --all-targets
```

## 🚨 Troubleshooting

### Port Conflicts
```bash
# If you get port binding errors, the system automatically
# generates new UUID-based ports. Check the logs for the actual port.

# Kill any existing processes if needed
pkill -f think-ai
```

### Build Issues
```bash
# Clean and rebuild if you encounter issues
cargo clean
cargo build --workspace --release
```

### Performance Testing
```bash
# Verify O(1) performance with stress test
cargo test performance -- --nocapture --release
```

## 📈 Monitoring Performance

### Real-time Performance Monitoring
```bash
# Run with performance metrics
RUST_LOG=info cargo run --bin think-ai-server

# Look for lines like:
# INFO think_ai_core: Operation completed in 156ns (O(1) ✓)
# INFO think_ai_vector: Search completed in 823μs for 100K vectors
```

### Memory Usage
```bash
# Monitor memory usage during testing
cargo build --release
time ./target/release/think-ai-server &
top -p $!
```

## 🎯 Expected Results

When everything works correctly, you should see:

1. **All tests pass** ✅
2. **Sub-millisecond operations** ✅  
3. **No O(n) violations** in linter ✅
4. **Unique port allocation** working ✅
5. **All binaries functional** ✅

## 🏆 Success Indicators

- Core engine: < 300ns per operation
- Vector search: < 1ms for 100K vectors  
- Cache access: < 100ns per operation
- Port allocation: No conflicts
- All tests: PASSED status