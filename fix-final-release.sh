#!/bin/bash

echo "🚀 FINAL RELEASE BUILD FIX"
echo "========================"

# 1. First, check and fix remaining issues
echo "1️⃣ Checking remaining errors..."
cargo check -p think-ai-knowledge 2>&1 | grep -B 10 "error:" | head -100

# 2. Fix the f_ parameter name issue
echo ""
echo "2️⃣ Fixing f_ parameter issues..."
sed -i 's/f_:/f:/g' think-ai-knowledge/src/evidence.rs
sed -i 's/f_:/f:/g' think-ai-knowledge/src/persistence.rs

# 3. Fix the comprehensive_knowledge parameter order
echo "3️⃣ Fixing comprehensive_knowledge parameter order..."
# The immunology call has parameters in wrong order - should be: domain, topic, content, related
sed -i '/engine.add_knowledge(/,/)/ {
    /KnowledgeDomain::Medicine,$/,/"The immune system protects/ {
        /"Immunology".to_string(),$/,/"The immune system protects/ {
            # Swap the vec and content lines
            N
            N
            s/\("Immunology".to_string(),\)\n\([[:space:]]*vec!\[.*\],\)\n\([[:space:]]*"The immune system.*\)/\1\n\3\n\2/
        }
    }
}' think-ai-knowledge/src/comprehensive_knowledge.rs

# 4. Run the release build
echo ""
echo "4️⃣ Running release build..."
cargo build --release 2>&1 | tee release-build.log | tail -50

# 5. Check if build succeeded
if grep -q "Finished \`release\`" release-build.log; then
    echo ""
    echo "✅ RELEASE BUILD SUCCESSFUL!"
    echo ""
    echo "Binary locations:"
    ls -la target/release/think-ai* | head -10
else
    echo ""
    echo "❌ Release build failed. Checking errors..."
    grep -E "error:|error\[" release-build.log | head -20
fi

echo ""
echo "✅ Final release build process complete!"