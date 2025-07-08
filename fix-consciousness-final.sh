#!/bin/bash

echo "🔧 FINAL FIX FOR CONSCIOUSNESS MODULE"
echo "===================================="

# 1. Fix perception_ parameter in desires.rs
echo "1️⃣ Fixing perception_ parameter in desires.rs..."
sed -i 's/perception_:/perception:/g' think-ai-consciousness/src/sentience/desires.rs
sed -i 's/perception_\./perception./g' think-ai-consciousness/src/sentience/desires.rs

# 2. Fix _evolution_score in evolution.rs
echo "2️⃣ Fixing _evolution_score in evolution.rs..."
sed -i 's/let _evolution_score =/let evolution_score =/' think-ai-consciousness/src/sentience/evolution.rs

# 3. Fix _pattern in evolution.rs
echo "3️⃣ Fixing _pattern in evolution.rs..."
sed -i 's/let _pattern =/let pattern =/' think-ai-consciousness/src/sentience/evolution.rs

# 4. Fix all underscore-prefixed variable definitions
echo "4️⃣ Fixing all underscore-prefixed variable definitions..."
find think-ai-consciousness/src -name "*.rs" -type f -exec sed -i \
    -e 's/let _\([a-zA-Z_]*\) =/let \1 =/' \
    {} \;

# 5. Fix all underscore-suffixed parameters
echo "5️⃣ Fixing all underscore-suffixed parameters..."
find think-ai-consciousness/src -name "*.rs" -type f -exec sed -i \
    -e 's/\([a-zA-Z_]*\)_:/\1:/g' \
    -e 's/\([a-zA-Z_]*\)_\./\1./g' \
    {} \;

# 6. Fix specific cases where we have both issues
echo "6️⃣ Fixing mixed underscore issues..."
# Fix references to variables that were defined with underscore prefix
find think-ai-consciousness/src -name "*.rs" -type f -exec sed -i \
    -e 's/\b_\([a-zA-Z_]*\)\b/\1/g' \
    {} \;

# 7. Fix result variable in consciousness_field.rs if not already fixed
echo "7️⃣ Ensuring result variable exists in consciousness_field.rs..."
grep -q "let result =" think-ai-consciousness/src/consciousness_field.rs || \
    sed -i '/let mut combined_state = self.state.clone();/a\        let result = combined_state.clone();' think-ai-consciousness/src/consciousness_field.rs

# 8. Test the build
echo ""
echo "8️⃣ Testing build..."
cd think-ai-consciousness && cargo check 2>&1 | grep -c "error:"

echo ""
echo "✅ Final fixes applied!"
echo "Checking detailed build status..."
cargo check