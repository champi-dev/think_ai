#!/bin/bash

echo "🔧 Testing full-working-o1.rs compilation..."
echo ""

# Change to project directory
cd /home/champi/Dev/think_ai

echo "📋 Checking imports in the fixed file..."
echo ""
grep -n "use think_ai_knowledge" think-ai-cli/src/bin/full-working-o1.rs
echo ""
grep -n "use think_ai_qwen" think-ai-cli/src/bin/full-working-o1.rs
echo ""

echo "🔍 Checking instantiation patterns..."
echo ""
grep -n "QwenClient::new" think-ai-cli/src/bin/full-working-o1.rs
grep -n "EnhancedQuantumLLMEngine" think-ai-cli/src/bin/full-working-o1.rs | head -5
echo ""

echo "🏗️ Building the specific binary..."
cargo build --bin full-working-o1 2>&1 | tee build-output.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo "✅ Build successful! All import errors have been fixed."
    echo ""
    echo "📊 Build summary:"
    echo "- Removed incorrect imports (AttentionMechanism, PrecisionMode)"
    echo "- Fixed QwenClient initialization with QwenConfig::default()"
    echo "- Fixed EnhancedQuantumLLMEngine to use simple new() constructor"
    echo "- KnowledgeNode import is valid and remains"
else
    echo ""
    echo "❌ Build failed. Checking error details..."
    echo ""
    grep -E "error|warning" build-output.log | head -20
fi

# Clean up
rm -f build-output.log

echo ""
echo "🎯 Test complete!"