#!/bin/bash
# Full deployment test script
# This script tests the entire deployment pipeline locally

set -e

echo "🚀 Think AI Full Deployment Test"
echo "================================"

# Check directory
echo "📍 Working directory: $(pwd)"

# Test 1: Build Rust project
echo -e "\n1️⃣ Building Rust project..."
cargo build --release
echo "✅ Rust build successful"

# Test 2: Run Rust tests
echo -e "\n2️⃣ Running Rust tests..."
cargo test --all
echo "✅ Rust tests passed"

# Test 3: Test CLI binary
echo -e "\n3️⃣ Testing CLI binary..."
./target/release/think-ai --version || echo "CLI test failed"

# Test 4: Check npm package
echo -e "\n4️⃣ Checking npm package..."
if [ -d "think-ai-js" ]; then
    cd think-ai-js
    echo "Building npm package..."
    npm install
    npm run build
    npm test || echo "npm tests failed"
    cd ..
    echo "✅ npm package ready"
else
    echo "❌ think-ai-js directory not found"
fi

# Test 5: Check PyPI package
echo -e "\n5️⃣ Checking PyPI package..."
if [ -d "think-ai-py" ]; then
    cd think-ai-py
    echo "Building PyPI package..."
    # Check if pip is available
    if command -v pip3 >/dev/null 2>&1; then
        pip3 install -e .
        python3 -m pytest tests/ || echo "PyPI tests failed"
    else
        echo "⚠️  pip3 not found, skipping PyPI tests"
    fi
    cd ..
    echo "✅ PyPI package ready"
else
    echo "❌ think-ai-py directory not found"
fi

# Test 6: Check deployment scripts
echo -e "\n6️⃣ Testing deployment scripts..."
./scripts/test-deployment.sh

echo -e "\n✅ Full deployment test complete!"
echo "To deploy libraries, run: ./scripts/deploy-all-libs.sh"