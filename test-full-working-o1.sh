#!/bin/bash

echo "🔧 Testing fixes for full-working-o1.rs..."

# Change to project directory
cd /home/champi/Dev/think_ai

# Clean and build the specific binary
echo "📦 Building full-working-o1 binary..."
cargo build --release --bin full-working-o1 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed. Checking for errors..."
    cargo build --release --bin full-working-o1 2>&1 | grep -E "(error|warning)" | head -20
    exit 1
fi

# Check if the binary was created
if [ -f "./target/release/full-working-o1" ]; then
    echo "✅ Binary created successfully at: ./target/release/full-working-o1"
    
    # Run a quick test of the binary
    echo ""
    echo "🚀 Testing the binary (will run for 5 seconds)..."
    timeout 5s ./target/release/full-working-o1 &
    TEST_PID=$!
    
    sleep 2
    
    # Check if process is running
    if ps -p $TEST_PID > /dev/null; then
        echo "✅ Binary is running successfully!"
        kill $TEST_PID 2>/dev/null
    else
        echo "❌ Binary crashed during startup"
    fi
else
    echo "❌ Binary not found at expected location"
fi

echo ""
echo "📋 Summary of changes made:"
echo "- Replaced think_ai_qwen::client::QwenClient with SimpleLLM"
echo "- Removed AttentionMechanism and PrecisionMode imports"
echo "- Changed EnhancedQuantumLLMEngine from builder pattern to simple new()"
echo "- Removed RwLock wrapper from enhanced_quantum_llm"

echo ""
echo "✅ Test complete!"