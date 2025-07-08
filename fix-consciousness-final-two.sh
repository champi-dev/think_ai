#!/bin/bash

echo "🔧 FIXING LAST 2 ERRORS IN CONSCIOUSNESS MODULE"
echo "=============================================="

# 1. Fix _voice variable in expression.rs
echo "1️⃣ Fixing _voice variable in expression.rs..."
sed -i 's/let _voice =/let voice =/' think-ai-consciousness/src/sentience/expression.rs

# 2. Fix tuple destructuring in memory.rs
echo "2️⃣ Fixing tuple destructuring in memory.rs..."
sed -i 's/\.map(|(theme,)| theme\.to_string())/.map(|(theme, _)| theme.to_string())/' think-ai-consciousness/src/sentience/memory.rs

# 3. Test the build
echo ""
echo "3️⃣ Testing build..."
cd think-ai-consciousness && cargo check

echo ""
echo "✅ Final two fixes applied!"