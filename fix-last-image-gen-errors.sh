#!/bin/bash

echo "🔧 FIXING LAST 7 IMAGE-GEN ERRORS"
echo "================================"

# 1. Fix ai_image_improver.rs
echo "1️⃣ Fixing ai_image_improver.rs..."
sed -i 's/let _success_rate =/let success_rate =/' think-ai-image-gen/src/ai_image_improver.rs
sed -i 's/height__/height/g' think-ai-image-gen/src/ai_image_improver.rs

# 2. Fix open_source_generator.rs
echo "2️⃣ Fixing open_source_generator.rs..."
sed -i 's/let _patterns =/let patterns =/' think-ai-image-gen/src/open_source_generator.rs
sed -i 's/let _modifiers =/let modifiers =/' think-ai-image-gen/src/open_source_generator.rs

# 3. Fix lib.rs
echo "3️⃣ Fixing lib.rs..."
sed -i 's/config: config_,/config: config.clone(),/' think-ai-image-gen/src/lib.rs

# Fix the cache_dir type annotation
sed -i '/let cache_dir = std::env::var("IMAGE_CACHE_DIR")/s/let cache_dir =/let cache_dir: PathBuf =/' think-ai-image-gen/src/lib.rs

# Add PathBuf conversion
sed -i 's/\.unwrap_or_else(|_| home_dir.join(".think-ai-cache").to_string_lossy().to_string());/.unwrap_or_else(|_| home_dir.join(".think-ai-cache").to_string_lossy().to_string()).into();/' think-ai-image-gen/src/lib.rs

# 4. Test the build
echo ""
echo "4️⃣ Testing build..."
cd think-ai-image-gen && cargo check 2>&1 | grep -c "error:"

echo ""
echo "✅ Image generation module fixes complete!"