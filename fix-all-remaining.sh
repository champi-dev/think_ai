#!/bin/bash

echo "🔧 FIXING ALL REMAINING COMPILATION ERRORS"
echo "========================================"

# 1. Fix think-ai-vector module
echo "1️⃣ Fixing think-ai-vector..."
find think-ai-vector/src -name "*.rs" -type f -exec sed -i \
    -e 's/___\([a-zA-Z_]*\)/\1/g' \
    -e 's/\([a-zA-Z_]*\)___:/\1:/g' \
    -e 's/\([a-zA-Z_]*\)_:/\1:/g' \
    -e 's/let _\([a-zA-Z_]*\) =/let \1 =/' \
    {} \;

# 2. Fix think-ai-core module  
echo "2️⃣ Fixing think-ai-core..."
find think-ai-core/src -name "*.rs" -type f -exec sed -i \
    -e 's/___\([a-zA-Z_]*\)/\1/g' \
    -e 's/\([a-zA-Z_]*\)___:/\1:/g' \
    -e 's/\([a-zA-Z_]*\)_:/\1:/g' \
    -e 's/let _\([a-zA-Z_]*\) =/let \1 =/' \
    {} \;

# 3. Fix think-ai-http module (likely has similar issues)
echo "3️⃣ Fixing think-ai-http..."
find think-ai-http/src -name "*.rs" -type f -exec sed -i \
    -e 's/___\([a-zA-Z_]*\)/\1/g' \
    -e 's/\([a-zA-Z_]*\)___:/\1:/g' \
    -e 's/\([a-zA-Z_]*\)_:/\1:/g' \
    -e 's/let _\([a-zA-Z_]*\) =/let \1 =/' \
    {} \;

# 4. Fix think-ai-knowledge module
echo "4️⃣ Fixing think-ai-knowledge..."
find think-ai-knowledge/src -name "*.rs" -type f -exec sed -i \
    -e 's/___\([a-zA-Z_]*\)/\1/g' \
    -e 's/\([a-zA-Z_]*\)___:/\1:/g' \
    -e 's/\([a-zA-Z_]*\)_:/\1:/g' \
    -e 's/let _\([a-zA-Z_]*\) =/let \1 =/' \
    {} \;

# 5. Fix think-ai-cli module
echo "5️⃣ Fixing think-ai-cli..."
find think-ai-cli/src -name "*.rs" -type f -exec sed -i \
    -e 's/___\([a-zA-Z_]*\)/\1/g' \
    -e 's/\([a-zA-Z_]*\)___:/\1:/g' \
    -e 's/\([a-zA-Z_]*\)_:/\1:/g' \
    -e 's/let _\([a-zA-Z_]*\) =/let \1 =/' \
    {} \;

# 6. Fix all remaining modules
echo "6️⃣ Fixing remaining modules..."
for module in think-ai-storage think-ai-utils think-ai-webapp think-ai-linter think-ai-process-manager think-ai-coding think-ai-llm think-ai-llm-simple think-ai-local-llm think-ai-quantum-mind think-ai-server think-ai-tinyllama think-ai-demos; do
    if [ -d "$module/src" ]; then
        echo "   Fixing $module..."
        find $module/src -name "*.rs" -type f -exec sed -i \
            -e 's/___\([a-zA-Z_]*\)/\1/g' \
            -e 's/\([a-zA-Z_]*\)___:/\1:/g' \
            -e 's/\([a-zA-Z_]*\)_:/\1:/g' \
            -e 's/let _\([a-zA-Z_]*\) =/let \1 =/' \
            {} \;
    fi
done

# 7. Remove unused imports
echo "7️⃣ Removing unused imports..."
sed -i '/use std::hash::{Hash, Hasher};/s/{Hash, }/{/' think-ai-core/src/consciousness_engine.rs
sed -i '/^[[:space:]]*use.*Hash;$/d' think-ai-vector/src/lsh/hasher.rs

# 8. Test the build
echo ""
echo "8️⃣ Testing build..."
cargo check --all 2>&1 | grep -c "error:"

echo ""
echo "✅ All fixes applied!"
echo ""
echo "To verify everything is working:"
echo "1. Run: cargo build --all"
echo "2. Run: cargo test --all"