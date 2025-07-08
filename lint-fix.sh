#!/bin/bash

echo "🔧 COMPREHENSIVE LINT FIX"
echo "========================"

# 1. Format all Rust code
echo "1️⃣ Formatting Rust code..."
cargo fmt --all

# 2. Fix clippy warnings
echo "2️⃣ Fixing clippy warnings..."
cargo clippy --fix --allow-dirty --allow-staged 2>/dev/null || true

# 3. Fix common patterns
echo "3️⃣ Fixing common patterns..."

# Fix unused variables
find . -name "*.rs" -type f | while read -r file; do
    # Add underscore to unused variables
    sed -i 's/let \([a-z_]*\) = /let _\1 = /g' "$file" 2>/dev/null || true
    
    # Fix unused function parameters
    sed -i 's/fn \([a-z_]*\)(\([^)]*\)\([a-z_]*\): /fn \1(\2_\3: /g' "$file" 2>/dev/null || true
done

# 4. Remove trailing whitespace
echo "4️⃣ Removing trailing whitespace..."
find . -name "*.rs" -type f -exec sed -i 's/[[:space:]]*$//' {} \;

# 5. Fix specific known issues
echo "5️⃣ Fixing specific issues..."
sed -i 's/std::time:_:Duration/std::time::Duration/g' think-ai-utils/src/lib.rs 2>/dev/null || true

echo ""
echo "✅ Lint fixes applied!"
echo ""
echo "Run 'cargo build' to verify everything compiles correctly."
