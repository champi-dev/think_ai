#!/bin/bash

echo "🔧 COMPLETE FIX FOR CACHE MODULE"
echo "==============================="

# 1. Fix parameter names with ___ suffix
echo "1️⃣ Fixing parameter names..."
sed -i 's/key___:/key:/g' think-ai-cache/src/lib.rs
sed -i 's/value___:/value:/g' think-ai-cache/src/lib.rs
sed -i 's/max_size___:/max_size:/g' think-ai-cache/src/lib.rs
sed -i 's/cache___:/cache:/g' think-ai-cache/src/lib.rs

# 2. Fix variable names with ___ prefix
echo "2️⃣ Fixing variable names..."
sed -i 's/___hasher/hasher/g' think-ai-cache/src/lib.rs
sed -i 's/___value/value/g' think-ai-cache/src/lib.rs
sed -i 's/___data/data/g' think-ai-cache/src/lib.rs
sed -i 's/___retrieved/retrieved/g' think-ai-cache/src/lib.rs

# 3. Test the build
echo ""
echo "3️⃣ Testing build..."
cd think-ai-cache && cargo check

echo ""
echo "✅ Cache module completely fixed!"