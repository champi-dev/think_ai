#!/bin/bash

# Test script for Think AI Knowledge Transfer
# This demonstrates the knowledge transfer capabilities

echo "══════════════════════════════════════════════════"
echo "🧪 THINK AI KNOWLEDGE TRANSFER TEST 🧪"
echo "Testing knowledge transfer capabilities"
echo "══════════════════════════════════════════════════"

# Quick test with 10 iterations for demonstration
ITERATIONS=${1:-10}

echo ""
echo "🔍 Running quick test with $ITERATIONS iterations..."
echo "(Use './test_knowledge_transfer.sh 1000' for full training)"
echo ""

# Build in release mode
echo "🔨 Building Think AI..."
cargo build --release --bin think-ai 2>&1 | grep -E "(error|warning|Finished)"

if [ $? -ne 0 ]; then
    echo "❌ Build failed"
    exit 1
fi

echo "✅ Build successful!"
echo ""

# Run short training session
echo "🚀 Starting knowledge transfer test..."
./target/release/think-ai train --iterations $ITERATIONS

echo ""
echo "🏁 Test complete!"
echo ""
echo "📊 Sample questions to test with 'think-ai chat':"
echo "  1. How do I implement a cache with O(1) operations?"
echo "  2. Debug my application that crashes intermittently"
echo "  3. Explain recursion in simple terms"
echo "  4. Design a high-performance messaging system"
echo "  5. What's the best way to optimize a slow database query?"
echo ""
echo "💡 Run the full training with: ./run_knowledge_transfer.sh 1000"