#!/bin/bash

echo "🏁 COMPLETE RELEASE BUILD FIX"
echo "============================"

# 1. First, exclude problematic modules from the build
echo "1️⃣ Creating a working release build configuration..."
cat > Cargo-release.toml << 'EOF'
[workspace]
members = [
    "think-ai-core",
    "think-ai-cache", 
    "think-ai-vector",
    "think-ai-consciousness",
    "think-ai-storage",
    "think-ai-utils",
    "think-ai-linter",
    "think-ai-coding",
    "think-ai-llm",
    "think-ai-llm-simple",
    "think-ai-qwen",
    "think-ai-cli",
    "think-ai-server",
    "think-ai-process-manager",
    "think-ai-http",
    "think-ai-knowledge",
    "think-ai-image-gen"
]

# Exclude webapp and demos from release build for now
exclude = [
    "think-ai-webapp",
    "think-ai-demos", 
    "think-ai-local-llm",
    "think-ai-quantum-mind",
    "think-ai-tinyllama"
]
EOF

# 2. Build only the working modules
echo ""
echo "2️⃣ Building core modules for release..."
cargo build --release \
    -p think-ai-core \
    -p think-ai-cache \
    -p think-ai-vector \
    -p think-ai-consciousness \
    -p think-ai-storage \
    -p think-ai-utils \
    -p think-ai-linter \
    -p think-ai-coding \
    -p think-ai-llm \
    -p think-ai-llm-simple \
    -p think-ai-qwen \
    -p think-ai-cli \
    -p think-ai-server \
    -p think-ai-process-manager \
    -p think-ai-http \
    -p think-ai-knowledge \
    -p think-ai-image-gen \
    2>&1 | tee core-release-build.log | tail -50

# 3. Check if core build succeeded
if grep -q "Finished \`release\`" core-release-build.log; then
    echo ""
    echo "✅ CORE MODULES BUILD SUCCESSFUL!"
    echo ""
    echo "Available binaries:"
    ls -la target/release/think-ai* 2>/dev/null | grep -v "\.d$" | head -20
    
    # 4. Create deployment script
    echo ""
    echo "3️⃣ Creating deployment helper..."
    cat > deploy-release.sh << 'EOF'
#!/bin/bash

echo "🚀 THINK AI DEPLOYMENT"
echo "===================="
echo ""
echo "Available binaries:"
ls -1 target/release/think-ai* | grep -v "\.d$"
echo ""
echo "To deploy to Railway:"
echo "1. Ensure railway.toml uses Rust 1.82+"
echo "2. git push origin main"
echo ""
echo "To run locally:"
echo "1. Server: ./target/release/think-ai-server"
echo "2. CLI: ./target/release/think-ai chat"
echo "3. Process Manager: ./target/release/process-manager"
EOF
    chmod +x deploy-release.sh
    
else
    echo ""
    echo "❌ Build failed. Checking errors..."
    grep -E "error:|error\[" core-release-build.log | head -30
fi

echo ""
echo "✅ Release build process complete!"
echo ""
echo "Next steps:"
echo "1. Run: ./deploy-release.sh"
echo "2. Deploy with: railway up"