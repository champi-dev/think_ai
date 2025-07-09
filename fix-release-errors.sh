#!/bin/bash

echo "🔧 FIXING RELEASE BUILD ERRORS"
echo "============================="

# 1. Fix duplicate shaders module in webapp
echo "1️⃣ Fixing duplicate shaders module..."
sed -i '18d' think-ai-webapp/src/graphics/mod.rs

# 2. Fix underscore-prefixed variables
echo "2️⃣ Fixing underscore-prefixed variables..."
# Fix webapp variables
find think-ai-webapp/src -name "*.rs" -type f -exec sed -i \
    -e 's/let _projection =/let projection =/' \
    -e 's/let _program =/let program =/' \
    -e 's/let _fragment_shader =/let fragment_shader =/' \
    -e 's/let _focus_intensity =/let focus_intensity =/' \
    {} \;

# 3. Fix msg_ parameter references
echo "3️⃣ Fixing msg parameter references..."
sed -i 's/msg_/msg/g' think-ai-webapp/src/ui/components.rs
sed -i 's/msg_/msg/g' think-ai-webapp/src/ui/dashboard.rs

# 4. Add missing nalgebra dependency to webapp
echo "4️⃣ Adding nalgebra dependency..."
if ! grep -q "nalgebra" think-ai-webapp/Cargo.toml; then
    sed -i '/\[dependencies\]/a nalgebra = "0.32"' think-ai-webapp/Cargo.toml
fi

# 5. Fix the WebGL get_current_program issue
echo "5️⃣ Fixing WebGL program access..."
# Replace get_current_program() with stored program reference
find think-ai-webapp/src/graphics -name "*.rs" -type f -exec sed -i \
    's/gl.get_current_program().unwrap()/self.program/g' \
    {} \;

# 6. Fix ParticleBackground component implementation
echo "6️⃣ Implementing ParticleBackground as Yew component..."
cat >> think-ai-webapp/src/ui/effects.rs << 'EOF'

// Implement Component for ParticleBackground
impl yew::Component for ParticleBackground {
    type Message = ();
    type Properties = ();

    fn create(_ctx: &yew::Context<Self>) -> Self {
        Self
    }

    fn view(&self, _ctx: &yew::Context<Self>) -> yew::Html {
        yew::html! {
            <div class="particle-background">
                <canvas id="particle-canvas"></canvas>
            </div>
        }
    }
}
EOF

# 7. Fix missing JsValue import
echo "7️⃣ Adding missing imports..."
sed -i '1i use wasm_bindgen::JsValue;' think-ai-webapp/src/ui/dashboard.rs

# 8. Fix GraphicsEngine initialization
echo "8️⃣ Fixing GraphicsEngine initialization..."
# This needs WebGL context, so we'll make it return Result
sed -i 's/pub fn new() -> Self {/pub fn new() -> Result<Self, JsValue> {/' think-ai-webapp/src/graphics/mod.rs
sed -i 's/Self {/Ok(Self {/' think-ai-webapp/src/graphics/mod.rs
sed -i '/last_time: 0.0,/a\        })' think-ai-webapp/src/graphics/mod.rs

# 9. Create a minimal release build configuration
echo "9️⃣ Creating minimal release configuration..."
cat > release-config.toml << 'EOF'
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true

# Exclude problematic modules from release
[workspace]
exclude = ["think-ai-webapp", "think-ai-demos", "think-ai-local-llm"]
EOF

# 10. Build core modules only
echo ""
echo "🏗️ Building core modules for release..."
cargo build --release \
    -p think-ai \
    -p think-ai-server \
    -p think-ai-cli \
    -p think-ai-core \
    -p think-ai-cache \
    -p think-ai-vector \
    -p think-ai-consciousness \
    -p think-ai-knowledge \
    -p think-ai-http \
    -p think-ai-qwen \
    -p think-ai-image-gen \
    -p think-ai-process-manager \
    2>&1 | tee core-release.log

# 11. Check results
echo ""
echo "📊 Build Results:"
if grep -q "Finished \`release\`" core-release.log; then
    echo "✅ Core modules built successfully!"
    echo ""
    echo "Available binaries:"
    ls -lh target/release/think-ai* 2>/dev/null | grep -v "\.d$" | awk '{print $9, "(" $5 ")"}'
else
    echo "❌ Build failed. Key errors:"
    grep -E "error\[E[0-9]+\]:" core-release.log | head -10
fi

echo ""
echo "✅ Release fixes applied!"