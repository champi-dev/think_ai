#!/bin/bash
# Test deployment script - verifies everything works without publishing

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "🧪 Testing Deployment Pipeline"
echo "============================="

# Test 1: Check scripts exist and are executable
echo "1️⃣ Checking scripts..."
[ -x "$SCRIPT_DIR/ultra-fast-precommit.sh" ] && echo "✅ ultra-fast-precommit.sh is executable" || echo "❌ ultra-fast-precommit.sh missing or not executable"
[ -x "$SCRIPT_DIR/deploy-all-libs.sh" ] && echo "✅ deploy-all-libs.sh is executable" || echo "❌ deploy-all-libs.sh missing or not executable"

# Test 2: Check pre-commit configuration
echo -e "\n2️⃣ Checking pre-commit configuration..."
if [ -f "$PROJECT_ROOT/.pre-commit-config.yaml" ]; then
    echo "✅ .pre-commit-config.yaml exists"
    grep -q "deploy-libs" "$PROJECT_ROOT/.pre-commit-config.yaml" && echo "✅ deploy-libs hook configured" || echo "❌ deploy-libs hook not found"
else
    echo "❌ .pre-commit-config.yaml not found"
fi

# Test 3: Check environment setup
echo -e "\n3️⃣ Checking environment setup..."
[ -f "$PROJECT_ROOT/.env.example" ] && echo "✅ .env.example exists" || echo "❌ .env.example missing"
[ -f "$PROJECT_ROOT/.env" ] && echo "✅ .env exists (tokens configured)" || echo "⚠️  .env missing (create from .env.example)"

# Test 4: Check npm package structure
echo -e "\n4️⃣ Checking npm package..."
if [ -d "$PROJECT_ROOT/think-ai-js" ]; then
    echo "✅ think-ai-js directory exists"
    [ -f "$PROJECT_ROOT/think-ai-js/package.json" ] && echo "✅ package.json exists" || echo "❌ package.json missing"
    [ -f "$PROJECT_ROOT/think-ai-js/README.md" ] && echo "✅ README.md exists" || echo "❌ README.md missing"
else
    echo "❌ think-ai-js directory not found"
fi

# Test 5: Check PyPI package structure
echo -e "\n5️⃣ Checking PyPI package..."
if [ -d "$PROJECT_ROOT/think-ai-py" ]; then
    echo "✅ think-ai-py directory exists"
    [ -f "$PROJECT_ROOT/think-ai-py/pyproject.toml" ] && echo "✅ pyproject.toml exists" || echo "❌ pyproject.toml missing"
    [ -f "$PROJECT_ROOT/think-ai-py/README.md" ] && echo "✅ README.md exists" || echo "❌ README.md missing"
else
    echo "❌ think-ai-py directory not found"
fi

# Test 6: Check Rust build
echo -e "\n6️⃣ Checking Rust build..."
cd "$PROJECT_ROOT"
if cargo check --all 2>/dev/null; then
    echo "✅ Rust code compiles successfully"
else
    echo "❌ Rust compilation failed"
fi

# Test 7: Run pre-commit hook
echo -e "\n7️⃣ Testing pre-commit hook..."
if command -v pre-commit >/dev/null 2>&1; then
    echo "Running pre-commit hooks..."
    pre-commit run --all-files || echo "⚠️  Pre-commit hooks failed (this might be expected)"
else
    echo "⚠️  pre-commit not installed. Install with: pip install pre-commit"
fi

echo -e "\n📊 Test Summary"
echo "=============="
echo "To deploy libraries:"
echo "1. Create .env from .env.example and add your tokens"
echo "2. Run: ./scripts/deploy-all-libs.sh"
echo "3. Or commit changes to trigger pre-commit hooks"