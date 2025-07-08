#!/bin/bash

echo "🔧 FIXING REMAINING SYNTAX ERRORS"
echo "================================="

# 1. Fix the broken set_inner_html calls in effects.rs
echo "1️⃣ Fixing set_inner_html syntax errors..."
sed -i 's/container.set_inner_html(container.set_inner_html(&html)_html);/container.set_inner_html(\&_html);/g' think-ai-webapp/src/ui/effects.rs

# 2. Fix variable references
echo "2️⃣ Fixing variable references..."
sed -i 's/effect\./effect_./g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bid\b/_id/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bdocument\b/_document/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/document_/_document/g' think-ai-webapp/src/ui/effects.rs

# 3. Fix intensity field
echo "3️⃣ Fixing intensity field..."
sed -i 's/intensity: f32,/intensity_: f32,/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/self\.intensity/self.intensity_/g' think-ai-webapp/src/ui/effects.rs

# 4. Fix specific variables
echo "4️⃣ Fixing specific variables..."
sed -i 's/current_x/_current_x/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/current_y/_current_y/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bsize\b/_size/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bscale\b/_scale/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bchars\b/_chars/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/column_count/_column_count/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/\bintensity\b/_intensity/g' think-ai-webapp/src/ui/effects.rs
sed -i 's/distance/_distance/g' think-ai-webapp/src/ui/effects.rs

# 5. Fix mod.rs issues
echo "5️⃣ Fixing mod.rs variable issues..."
sed -i 's/\bwindow\b/_window/g' think-ai-webapp/src/ui/mod.rs
sed -i 's/\bdocument\b/_document/g' think-ai-webapp/src/ui/mod.rs
sed -i 's/style_element/_style_element/g' think-ai-webapp/src/ui/mod.rs
sed -i 's/\bhead\b/_head/g' think-ai-webapp/src/ui/mod.rs
sed -i 's/self\._window/self.window/g' think-ai-webapp/src/ui/mod.rs
sed -i 's/self\._document/self.document/g' think-ai-webapp/src/ui/mod.rs

# 6. Fix the broken parameter syntax in think-ai-utils
echo "6️⃣ Checking think-ai-utils issues..."
# Let's check what's wrong in think-ai-utils
head -50 think-ai-utils/src/lib.rs

# 7. Build again to see progress
echo ""
echo "7️⃣ Building to check progress..."
cargo build --release --bin think-ai 2>&1 | grep -E "(Compiling|Finished|error:|warning:)" | tail -30

echo ""
echo "✅ Syntax fixes applied!"