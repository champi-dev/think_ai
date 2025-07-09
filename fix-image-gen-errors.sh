#!/bin/bash

echo "🔧 FIXING IMAGE GENERATION MODULE COMPILATION ERRORS"
echo "=================================================="

# 1. Fix open_source_generator.rs
echo "1️⃣ Fixing open_source_generator.rs..."
sed -i 's/height_/height/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___cy/cy/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___cx/cx/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___dist/dist/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___max_dist/max_dist/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___factor/factor/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___r_base/r_base/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___g_base/g_base/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___b_base/b_base/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___wave/wave/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___noise/noise/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___idx/idx/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___pixel/pixel/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___text_height/text_height/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___total_generations/total_generations/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___avg_quality/avg_quality/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___excellent_count/excellent_count/g' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/___quality_scores/quality_scores/g' think-ai-image-gen/src/open_source_generator.rs

# Add missing variables
sed -i '/let ___cy = height as f32/i\        let height = height_;' think-ai-image-gen/src/open_source_generator.rs

# 2. Fix prompt_optimizer.rs
echo "2️⃣ Fixing prompt_optimizer.rs..."
sed -i 's/___style_modifiers/style_modifiers/g' think-ai-image-gen/src/prompt_optimizer.rs
sed -i 's/___quality_modifiers/quality_modifiers/g' think-ai-image-gen/src/prompt_optimizer.rs
sed -i 's/___prompt_lower/prompt_lower/g' think-ai-image-gen/src/prompt_optimizer.rs
sed -i 's/___quality_mods/quality_mods/g' think-ai-image-gen/src/prompt_optimizer.rs
sed -i 's/___style_mods/style_mods/g' think-ai-image-gen/src/prompt_optimizer.rs
sed -i 's/success_score___/success_score/g' think-ai-image-gen/src/prompt_optimizer.rs

# Add missing variables
sed -i '/let mut enhanced_prompt = prompt.to_string();/i\    pub async fn optimize(&self, prompt: &str) -> String {' think-ai-image-gen/src/prompt_optimizer.rs
sed -i '/let mut enhanced_prompt = prompt.to_string();/i\        let patterns = self.optimization_patterns.read().await;' think-ai-image-gen/src/prompt_optimizer.rs

# Fix missing style variable
sed -i '/match style {/i\        let style = self.detect_style(prompt_lower);' think-ai-image-gen/src/prompt_optimizer.rs

# 3. Fix lib.rs
echo "3️⃣ Fixing lib.rs..."
sed -i 's/___cache_dir/cache_dir/g' think-ai-image-gen/src/lib.rs
sed -i 's/___max_cache_gb/max_cache_gb/g' think-ai-image-gen/src/lib.rs
sed -i 's/___client/client/g' think-ai-image-gen/src/lib.rs
sed -i 's/___optimizer/optimizer/g' think-ai-image-gen/src/lib.rs
sed -i 's/___learner/learner/g' think-ai-image-gen/src/lib.rs
sed -i 's/___cache_key/cache_key/g' think-ai-image-gen/src/lib.rs
sed -i 's/___enhanced_prompt/enhanced_prompt/g' think-ai-image-gen/src/lib.rs
sed -i 's/___start_time/start_time/g' think-ai-image-gen/src/lib.rs
sed -i 's/___generation_time_ms/generation_time_ms/g' think-ai-image-gen/src/lib.rs
sed -i 's/___total_generations/total_generations/g' think-ai-image-gen/src/lib.rs
sed -i 's/___cache_stats/cache_stats/g' think-ai-image-gen/src/lib.rs

# Fix the _cache variable
sed -i 's/let _cache =/let cache =/' think-ai-image-gen/src/lib.rs

# Add missing request parameter
sed -i '/pub async fn generate(&self, request: ImageGenRequest)/,/^    }/ {
    s/let ___cache_key = self.generate_cache_key(&request);/let cache_key = self.generate_cache_key(\&request);/
}' think-ai-image-gen/src/lib.rs

# Add missing metadata variable
sed -i '/let ___generation_time_ms/a\        let metadata = ImageMetadata {' think-ai-image-gen/src/lib.rs

# Fix struct field initialization shorthand
sed -i '/^[[:space:]]*api_key,$/s/api_key,/api_key: api_key.to_string(),/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*api_url,$/s/api_url,/api_url: api_url.to_string(),/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*cache_dir,$/s/cache_dir,/cache_dir: cache_dir.clone(),/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*config,$/s/config,/config: config_,/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*client,$/s/client,/client: client.clone(),/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*cache,$/s/cache,/cache: cache.clone(),/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*optimizer,$/s/optimizer,/optimizer: optimizer.clone(),/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*learner,$/s/learner,/learner: learner.clone(),/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*metadata,$/s/metadata,/metadata: metadata.clone(),/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*generation_time_ms,$/s/generation_time_ms,/generation_time_ms: generation_time_ms,/' think-ai-image-gen/src/lib.rs
sed -i '/^[[:space:]]*total_generations,$/s/total_generations,/total_generations: total_generations,/' think-ai-image-gen/src/lib.rs

# 4. Fix all remaining ___ prefixed variables
echo "4️⃣ Fixing all remaining ___ prefixed variables..."
find think-ai-image-gen/src -name "*.rs" -type f -exec sed -i \
    -e 's/___\([a-zA-Z_]*\)/\1/g' \
    {} \;

# 5. Fix parameter names with ___ suffix
echo "5️⃣ Fixing parameter names with ___ suffix..."
find think-ai-image-gen/src -name "*.rs" -type f -exec sed -i \
    -e 's/\([a-zA-Z_]*\)___:/\1:/g' \
    {} \;

# 6. Test the build
echo ""
echo "6️⃣ Testing build..."
cd think-ai-image-gen && cargo check 2>&1 | grep -c "error:"

echo ""
echo "✅ Image generation module fixes applied!"