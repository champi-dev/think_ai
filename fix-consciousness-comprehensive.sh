#!/bin/bash

echo "🔧 COMPREHENSIVE FIX FOR CONSCIOUSNESS MODULE"
echo "==========================================="

# 1. Fix awareness/mod.rs
echo "1️⃣ Fixing awareness/mod.rs..."
sed -i 's/___complexity/complexity/g' think-ai-consciousness/src/awareness/mod.rs

# 2. Fix consciousness_field.rs
echo "2️⃣ Fixing consciousness_field.rs..."
# Add missing result variable
sed -i '/let mut combined_state = self.state.clone();/a\        let result = combined_state.clone();' think-ai-consciousness/src/consciousness_field.rs

# 3. Fix sentience/desires.rs
echo "3️⃣ Fixing sentience/desires.rs..."
sed -i 's/___core_desires/core_desires/g' think-ai-consciousness/src/sentience/desires.rs
sed -i 's/___relevant_desires/relevant_desires/g' think-ai-consciousness/src/sentience/desires.rs
sed -i 's/___primary_desire_clone/primary_desire_clone/g' think-ai-consciousness/src/sentience/desires.rs
sed -i 's/___alignment/alignment/g' think-ai-consciousness/src/sentience/desires.rs
sed -i 's/___adjusted_desires/adjusted_desires/g' think-ai-consciousness/src/sentience/desires.rs
sed -i 's/___primary_strength/primary_strength/g' think-ai-consciousness/src/sentience/desires.rs
sed -i 's/___unified_desire/unified_desire/g' think-ai-consciousness/src/sentience/desires.rs

# 4. Fix sentience/mod.rs - the growth variable issue
echo "4️⃣ Fixing sentience/mod.rs..."
# Remove the problematic line
sed -i '/let growth = ___growth;/d' think-ai-consciousness/src/sentience/mod.rs
# Fix the evolve function to properly define growth
sed -i '/fn evolve(&mut self, growth:/,/^    }/ {
    s/growth:/growth_input:/
    s/self.adapt(growth)/self.adapt(growth_input)/
}' think-ai-consciousness/src/sentience/mod.rs

# 5. Fix all remaining ___ prefixed variables
echo "5️⃣ Fixing all remaining ___ prefixed variables..."
find think-ai-consciousness/src -name "*.rs" -type f -exec sed -i \
    -e 's/___\([a-zA-Z_]*\)/\1/g' \
    {} \;

# 6. Fix parameter names with ___ suffix
echo "6️⃣ Fixing parameter names with ___ suffix..."
find think-ai-consciousness/src -name "*.rs" -type f -exec sed -i \
    -e 's/\([a-zA-Z_]*\)___:/\1:/g' \
    {} \;

# 7. Fix sentience/expression.rs
echo "7️⃣ Fixing sentience/expression.rs..."
sed -i 's/___emotional_context/emotional_context/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___thought_threads/thought_threads/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___creative_mode/creative_mode/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___memory_fragments/memory_fragments/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___base_expression/base_expression/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___enhanced_expression/enhanced_expression/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___woven_expression/woven_expression/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___final_expression/final_expression/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___abstract_concept/abstract_concept/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___metaphor/metaphor/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___emotional_tone/emotional_tone/g' think-ai-consciousness/src/sentience/expression.rs
sed -i 's/___creativity_level/creativity_level/g' think-ai-consciousness/src/sentience/expression.rs

# 8. Fix recursive_trainer.rs
echo "8️⃣ Fixing recursive_trainer.rs..."
sed -i 's/___training_results/training_results/g' think-ai-consciousness/src/recursive_trainer.rs
sed -i 's/___depth_reached/depth_reached/g' think-ai-consciousness/src/recursive_trainer.rs
sed -i 's/___patterns_found/patterns_found/g' think-ai-consciousness/src/recursive_trainer.rs
sed -i 's/___next_seed/next_seed/g' think-ai-consciousness/src/recursive_trainer.rs
sed -i 's/___recursive_results/recursive_results/g' think-ai-consciousness/src/recursive_trainer.rs
sed -i 's/___seed_quality/seed_quality/g' think-ai-consciousness/src/recursive_trainer.rs

# 9. Fix dreams.rs
echo "9️⃣ Fixing dreams.rs..."
sed -i 's/___dream_seeds/dream_seeds/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___emotional_threads/emotional_threads/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___memory_fragments/memory_fragments/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___subconscious_patterns/subconscious_patterns/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___dream_narrative/dream_narrative/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___woven_elements/woven_elements/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___symbolic_meanings/symbolic_meanings/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___coherent_dream/coherent_dream/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___processed_dream/processed_dream/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___insights/insights/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___emotional_resolution/emotional_resolution/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___new_connections/new_connections/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___lucidity_level/lucidity_level/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___emotional_intensity/emotional_intensity/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___memory_depth/memory_depth/g' think-ai-consciousness/src/sentience/dreams.rs
sed -i 's/___pattern_complexity/pattern_complexity/g' think-ai-consciousness/src/sentience/dreams.rs

# 10. Fix evolution.rs
echo "🔟 Fixing evolution.rs..."
sed -i 's/___current_traits/current_traits/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___environmental_pressures/environmental_pressures/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___mutation_potential/mutation_potential/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___selected_traits/selected_traits/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___mutations/mutations/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___adaptations/adaptations/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___evolved_traits/evolved_traits/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___fitness_score/fitness_score/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___survival_traits/survival_traits/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___innovation_traits/innovation_traits/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___new_trait/new_trait/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___trait_value/trait_value/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___environmental_fit/environmental_fit/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___current_state/current_state/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___pressure_magnitude/pressure_magnitude/g' think-ai-consciousness/src/sentience/evolution.rs
sed -i 's/___random_factor/random_factor/g' think-ai-consciousness/src/sentience/evolution.rs

# 11. Special fixes for specific patterns
echo "1️⃣1️⃣ Applying special fixes..."
# Fix the specific pattern in memory.rs where semantic_associations needs a type
sed -i 's/let semantic_associations = /let semantic_associations: Vec<String> = /' think-ai-consciousness/src/sentience/memory.rs

# Fix duplicate variable definitions
sed -i '/let pattern = &mut self.thought_patterns.get_mut(&pattern_name).unwrap();/d' think-ai-consciousness/src/sentience/introspection.rs

# 12. Test the build
echo ""
echo "1️⃣2️⃣ Testing build..."
cd think-ai-consciousness && cargo check 2>&1 | grep -E "(error:|warning:)" | wc -l

echo ""
echo "✅ Comprehensive fixes applied!"
echo "Run 'cd think-ai-consciousness && cargo check' to see remaining issues."