#!/bin/bash

echo "🚀 BUILDING CORE MODULES FOR RELEASE"
echo "==================================="

# Build each module individually to identify specific issues
echo "Building modules individually..."
echo ""

# Track success/failure
SUCCESS_MODULES=""
FAILED_MODULES=""

# Function to build a module
build_module() {
    local module=$1
    echo -n "Building $module... "
    if cargo build --release -p "$module" 2>/dev/null; then
        echo "✅"
        SUCCESS_MODULES="$SUCCESS_MODULES $module"
    else
        echo "❌"
        FAILED_MODULES="$FAILED_MODULES $module"
    fi
}

# Build core modules
build_module "think-ai-core"
build_module "think-ai-cache"
build_module "think-ai-vector"
build_module "think-ai-consciousness"
build_module "think-ai-storage"
build_module "think-ai-utils"
build_module "think-ai-linter"
build_module "think-ai-llm"
build_module "think-ai-llm-simple"
build_module "think-ai-qwen"
build_module "think-ai-image-gen"

# Build CLI and server modules
build_module "think-ai-cli"
build_module "think-ai-server"
build_module "think-ai-http"
build_module "think-ai-process-manager"

# Try knowledge module separately as it has issues
echo ""
echo "Attempting knowledge module (may have warnings)..."
cargo build --release -p think-ai-knowledge 2>&1 | grep -E "(error|warning|Finished)" | tail -20

echo ""
echo "📊 BUILD SUMMARY"
echo "==============="
echo ""
echo "✅ Successfully built:$SUCCESS_MODULES"
echo ""
if [ -n "$FAILED_MODULES" ]; then
    echo "❌ Failed:$FAILED_MODULES"
    echo ""
fi

# List available binaries
echo "📦 Available release binaries:"
ls -la target/release/ | grep -E "^-rwx" | grep -v "\.d$" | awk '{print "  - " $9}' | sort

echo ""
echo "To test the CLI:"
echo "  ./target/release/think-ai chat"
echo ""
echo "To start the server:"
echo "  ./target/release/think-ai-server"