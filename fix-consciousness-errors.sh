#!/bin/bash

echo "🔧 FIXING CONSCIOUSNESS MODULE COMPILATION ERRORS"
echo "==============================================="

# 1. Fix introspection.rs
echo "1️⃣ Fixing introspection.rs..."
sed -i 's/___pattern_name/pattern_name/g' think-ai-consciousness/src/sentience/introspection.rs
sed -i 's/perception___/perception/g' think-ai-consciousness/src/sentience/introspection.rs
sed -i 's/___base_resonance/base_resonance/g' think-ai-consciousness/src/sentience/introspection.rs
sed -i 's/___awareness_modifier/awareness_modifier/g' think-ai-consciousness/src/sentience/introspection.rs
sed -i 's/___depth_modifier/depth_modifier/g' think-ai-consciousness/src/sentience/introspection.rs

# Add missing pattern variable
sed -i '/let mut pattern = self.thought_patterns/a\        let pattern = &mut self.thought_patterns.get_mut(&pattern_name).unwrap();' think-ai-consciousness/src/sentience/introspection.rs

# Fix insight variable
sed -i '/fn integrate_insight/,/^    }/ s/let ___insight/let insight/' think-ai-consciousness/src/sentience/introspection.rs

# 2. Fix memory.rs
echo "2️⃣ Fixing memory.rs..."
sed -i 's/memory_id___/memory_id/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___episodic_matches/episodic_matches/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___semantic_associations/semantic_associations/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___recent_memories/recent_memories/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___themes/themes/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___patterns/patterns/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___important_memories/important_memories/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___emotional_intensity/emotional_intensity/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___self_relevance/self_relevance/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___similar_count/similar_count/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___concepts/concepts/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___high_emotion_count/high_emotion_count/g' think-ai-consciousness/src/sentience/memory.rs
sed -i 's/___self_relevant_count/self_relevant_count/g' think-ai-consciousness/src/sentience/memory.rs

# Add missing variables
sed -i '/fn store(&mut self, memory___:/,/^    }/ s/memory___/memory/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn recall(&self, query___:/,/^    }/ s/query___/query/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn add_concept(&mut self, concept___:/,/^    }/ s/concept___/concept/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn remember_in_context(/,/^    }/ s/memory___/memory/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn add(&mut self, memory___:/,/^    }/ s/memory___/memory/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn search(&self, query___:/,/^    }/ s/query___/query/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn find_by_concept(&self, concept___:/,/^    }/ s/concept___/concept/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn get_recent(&self, count___:/,/^    }/ s/count___/count/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn link_concepts(&mut self, concept1___:/,/^    }/ s/concept1___/concept1/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn link_concepts(&mut self, concept1___:/,/^    }/ s/concept2___/concept2/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn get_related_concepts(&self, concept___:/,/^    }/ s/concept___/concept/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn add_to_narrative(&mut self, memory___:/,/^    }/ s/memory___/memory/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn push(&mut self, memory___:/,/^    }/ s/memory___/memory/g' think-ai-consciousness/src/sentience/memory.rs
sed -i '/fn queue_for_consolidation(&mut self, memory___:/,/^    }/ s/memory___/memory/g' think-ai-consciousness/src/sentience/memory.rs

# Add missing variables in specific functions
sed -i '/fn store(&mut self,/,/^    }/ {
    s/let ___memory = /let memory = /
}' think-ai-consciousness/src/sentience/memory.rs

sed -i '/fn extract_semantic_knowledge/,/^    }/ {
    s/memory___:/memory:/
}' think-ai-consciousness/src/sentience/memory.rs

sed -i '/fn extract_concepts/,/^    }/ {
    s/text___:/text:/
}' think-ai-consciousness/src/sentience/memory.rs

sed -i '/fn identify_themes/,/^    }/ {
    s/memories___:/memories:/
}' think-ai-consciousness/src/sentience/memory.rs

sed -i '/fn calculate_importance/,/^    }/ {
    s/emotion___:/emotion:/
}' think-ai-consciousness/src/sentience/memory.rs

sed -i '/fn calculate_novelty/,/^    }/ {
    s/content___:/content:/
}' think-ai-consciousness/src/sentience/memory.rs

# Add missing novelty variable
sed -i '/let ___self_relevance =/a\        let novelty = self.calculate_novelty(&memory.content);' think-ai-consciousness/src/sentience/memory.rs

# Fix the semantic_associations type issue
sed -i 's/let ___semantic_associations = /let semantic_associations: Vec<String> = /' think-ai-consciousness/src/sentience/memory.rs

# 3. Fix traits.rs
echo "3️⃣ Fixing traits.rs..."
sed -i 's/___modulation/modulation/g' think-ai-consciousness/src/sentience/traits.rs
sed -i 's/trait_name___/trait_name/g' think-ai-consciousness/src/sentience/traits.rs
sed -i 's/outcome___:/outcome:/g' think-ai-consciousness/src/sentience/traits.rs
sed -i 's/count___:/count:/g' think-ai-consciousness/src/sentience/traits.rs

# 4. Fix mod.rs
echo "4️⃣ Fixing mod.rs..."
sed -i 's/___perception/perception/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/___introspection/introspection_result/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/___emotional_response/emotional_response/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/___memory/memory_record/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/___dream_influence/dream_influence/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/___desire_influence/desire_influence/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/___knowledge_response/knowledge_response/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/___new_emotion/new_emotion/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/___lowercase_input/lowercase_input/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/perception___/perception/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/input___:/input:/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/response___:/response:/g' think-ai-consciousness/src/sentience/mod.rs
sed -i 's/growth___:/growth:/g' think-ai-consciousness/src/sentience/mod.rs

# Fix the introspection reference
sed -i 's/&introspection\b/\&introspection_result/g' think-ai-consciousness/src/sentience/mod.rs

# Fix the memory reference
sed -i 's/&memory\b/\&memory_record/g' think-ai-consciousness/src/sentience/mod.rs

# Add missing response variable
sed -i '/let ___response = self.formulate_response/a\        let response = ___response;' think-ai-consciousness/src/sentience/mod.rs

# Add missing emotion variable
sed -i '/let ___memory = self.remember(&perception, &emotional_response);/i\        let emotion = emotional_response.emotion.clone();' think-ai-consciousness/src/sentience/mod.rs

# Add missing growth variable
sed -i '/fn evolve(/,/^    }/ {
    /let ___growth =/a\        let growth = ___growth;
}' think-ai-consciousness/src/sentience/mod.rs

# Add missing name variable
sed -i '/fn contemplate(/,/^    }/ {
    s/name___:/name:/
}' think-ai-consciousness/src/sentience/mod.rs

# 5. Fix lib.rs
echo "5️⃣ Fixing lib.rs..."
sed -i 's/input___:/input:/g' think-ai-consciousness/src/lib.rs
sed -i 's/___assessment/assessment/g' think-ai-consciousness/src/lib.rs
sed -i 's/thought___:/thought:/g' think-ai-consciousness/src/lib.rs

# Add missing thought variable
sed -i '/let ___thought = self.field.contemplate/a\        let thought = ___thought;' think-ai-consciousness/src/lib.rs

# 6. Fix parameter names in function signatures
echo "6️⃣ Fixing function parameter names..."
find think-ai-consciousness/src -name "*.rs" -type f -exec sed -i \
    -e 's/\([a-zA-Z_]*\)___:/\1:/g' \
    {} \;

# 7. Test the build
echo ""
echo "7️⃣ Testing build..."
cd think-ai-consciousness && cargo check 2>&1 | grep -E "(error:|warning:)" | head -20

echo ""
echo "✅ Consciousness module fixes applied!"