#!/bin/bash
set -e

echo "🔐 Removing API Keys from Tracked Files"
echo "====================================="
echo ""

# Remove API keys from files
echo "Cleaning files with API keys..."

# List of files to clean
FILES=(
    "test_huggingface_api.sh"
    "think-ai-qwen/benches/benchmark.rs"
    "QWEN_INTEGRATION_SUMMARY.md"
    "setup-huggingface-token.sh"
    "test-working-models.py"
    "think-ai-llm/src/model.rs"
    "think-ai-knowledge/src/bin/think-ai-train-with-qwen.rs"
    "find-working-model.py"
    "docs/QWEN_INTEGRATION.md"
    "config/fast_test.yaml"
    "config/full_system.yaml"
    "configs/docker-compose.cache.yml"
)

# Replace all hf_ tokens with placeholder
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "Cleaning $file..."
        sed -i 's/hf_[A-Za-z0-9]\{32,\}/YOUR_HUGGINGFACE_TOKEN_HERE/g' "$file"
    fi
done

# Also clean the weird {} file if it exists
if [ -f "{}" ]; then
    echo "Cleaning {} file..."
    sed -i 's/hf_[A-Za-z0-9]\{32,\}/YOUR_HUGGINGFACE_TOKEN_HERE/g' "{}"
fi

echo ""
echo "✅ API keys replaced with placeholders"
echo ""

# Create .env.example if not exists
if [ ! -f ".env.example" ]; then
    echo "Creating .env.example..."
    cat > .env.example << 'EOF'
# Hugging Face API Configuration
HUGGINGFACE_TOKEN=your_token_here

# Model Configuration
MODEL_ID=Qwen/Qwen2.5-1.5B-Instruct

# API Keys (if needed)
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
EOF
fi

# Update .gitignore
echo "Updating .gitignore..."
if ! grep -q "HUGGINGFACE_TOKEN" .gitignore 2>/dev/null; then
    cat >> .gitignore << 'EOF'

# API Keys and Secrets
.env
.env.local
.env.*.local
**/secrets.json
**/api_keys.json
test_huggingface_api.sh
setup-huggingface-token.sh

# Files with potential secrets
*_with_token.sh
*_api_key*
EOF
fi

echo ""
echo "📝 Next Steps:"
echo "1. Review changes: git diff"
echo "2. Stage clean files: git add -u"
echo "3. Commit: git commit -m 'Remove API keys from tracked files'"
echo "4. Force push if needed: git push --force-with-lease"
echo ""
echo "⚠️  Important: Never commit API keys!"
echo "   Use environment variables instead: export HUGGINGFACE_TOKEN='your_token'"
echo ""