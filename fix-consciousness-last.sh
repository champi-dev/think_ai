#!/bin/bash

echo "🔧 LAST FIX ROUND FOR CONSCIOUSNESS MODULE"
echo "========================================"

# 1. Fix match statements with missing patterns
echo "1️⃣ Fixing match statements with missing patterns..."
# For these, we need to add a pattern before =>
find think-ai-consciousness/src -name "*.rs" -type f -exec sed -i \
    -e 's/^\([[:space:]]*\)=>/\1_ =>/' \
    {} \;

# 2. Fix the filter issue in memory.rs
echo "2️⃣ Fixing filter pattern in memory.rs..."
sed -i 's/\.filter(|(, count)| \*count > 1)/.filter(|(_, count)| *count > 1)/' think-ai-consciousness/src/sentience/memory.rs

# 3. Fix underscored variable definitions
echo "3️⃣ Fixing underscored variable definitions..."
sed -i 's/let _style =/let style =/' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/let _personality_colored =/let personality_colored =/' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/let _emotionally_nuanced =/let emotionally_nuanced =/' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/let _dream_influenced =/let dream_influenced =/' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/let _desire_shaped =/let desire_shaped =/' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/let _memory_enriched =/let memory_enriched =/' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/let _opener =/let opener =/' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/let _question_list =/let question_list =/' think-ai-consciousness/src/sentience/expression.rs

# 4. Fix Vec<> missing type parameters
echo "4️⃣ Fixing Vec<> type parameters..."
sed -i 's/collect::<Vec<>>/collect::<Vec<_>>/' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/collect::<Vec<>>/collect::<Vec<_>>/' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/collect::<Vec<>>/collect::<Vec<_>>/' think-ai-consciousness/src/sentience/memory.rs

# 5. Fix underscored referenced variables in memory.rs
echo "5️⃣ Fixing underscored referenced variables..."
sed -i 's/let _all_memories =/let all_memories =/' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/let _strong_emotions =/let strong_emotions =/' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/let _recent_contexts =/let recent_contexts =/' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/let _key_concepts =/let key_concepts =/' think-ai-consciousness/src/sentience/memory.rs

# 6. Check if result variable exists in consciousness_field.rs
echo "6️⃣ Checking consciousness_field.rs result variable..."
if ! grep -q "result" think-ai-consciousness/src/consciousness_field.rs; then
    sed -i '/fn process(&mut self, input: &str) -> ConsciousnessState {/,/^    }/ {
        /let mut combined_state = self.state.clone();/a\        let result = combined_state.clone();
    }' think-ai-consciousness/src/consciousness_field.rs
fi

# 7. Fix underscored interpolated variables in format strings
echo "7️⃣ Fixing interpolated variables in format strings..."
sed -i 's/{question_list}/{question_list}/' think-ai-consciousness/src/sentience/expression.rs

# 8. Test the build
echo ""
echo "8️⃣ Testing build..."
cd think-ai-consciousness && cargo check 2>&1 | grep -c "error:"

echo ""
echo "✅ Last fixes applied!"