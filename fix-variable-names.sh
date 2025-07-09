#!/bin/bash
set -e

echo "Fixing variable name mismatches..."

# Fix think-ai-core/src/consciousness_engine.rs
echo "Fixing consciousness_engine.rs"
sed -i 's/core___/core/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___seed/seed/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/input___/input/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___start/start/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___content_hash/content_hash/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___thought_id/thought_id/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___awareness/awareness/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___thought/thought/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___result/result/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/action_hash___/action_hash/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___is_ethical/is_ethical/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/pattern_hash___/pattern_hash/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/thought_id2___/thought_id2/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___association_hash/association_hash/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___metrics/metrics/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___state/state/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/content___/content/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/content_hash___/content_hash/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/id2___/id2/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___min/min/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___max/max/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/cache_hit___/cache_hit/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___elapsed_ns/elapsed_ns/g' think-ai-core/src/consciousness_engine.rs
sed -i 's/___normalized/normalized/g' think-ai-core/src/consciousness_engine.rs

echo "All variable name mismatches fixed"