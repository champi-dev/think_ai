#!/bin/bash
set -e

echo "🚀 Think AI Isolated Sessions Demo"
echo "================================="
echo ""

# Check if we need to fix Rust version dependencies
if cargo build --release 2>&1 | grep -q "rustc 1.80.1 is not supported"; then
    echo "⚠️  Detected Rust version compatibility issue"
    echo "Running dependency fix..."
    ./fix-rust-version-deps.sh
    echo ""
fi

# Build the project
echo "🔨 Building Think AI with isolated sessions..."
cargo build --release --bin test-isolated-sessions

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    
    # Run the demo
    echo "🎯 Running isolated sessions demo..."
    echo "===================================="
    ./target/release/test-isolated-sessions
    
    echo ""
    echo "🎉 Demo completed successfully!"
    echo ""
    echo "📚 Next steps:"
    echo "  1. Review the architecture documentation: ISOLATED_SESSIONS_ARCHITECTURE.md"
    echo "  2. Check the example integration: examples/isolated_sessions_example.rs"
    echo "  3. Run tests: cargo test -p think-ai-knowledge"
    echo ""
    echo "💡 To integrate into your application:"
    echo "  - Use IsolatedSession for each user chat"
    echo "  - Start ParallelProcessor for background tasks"
    echo "  - All components share the same SharedKnowledge instance"
else
    echo "❌ Build failed. Please check the error messages above."
    echo ""
    echo "If you see Rust version errors, try:"
    echo "  1. Run: ./fix-rust-version-deps.sh"
    echo "  2. Or update Rust: rustup update"
    echo "  3. Or use a specific version: rustup default 1.81.0"
fi