#!/bin/bash

echo "🚀 SIMPLE RELEASE BUILD"
echo "====================="

# Just try to build everything in release mode
echo "Building all modules in release mode..."
echo ""

# Run the release build and capture output
cargo build --release 2>&1 | tee full-release-build.log

# Check results
echo ""
echo "Build complete. Checking results..."
echo ""

if grep -q "Finished \`release\`" full-release-build.log; then
    echo "✅ SOME MODULES BUILT SUCCESSFULLY!"
    echo ""
    echo "Available release binaries:"
    ls -la target/release/ | grep -E "^-rwx" | grep -v "\.d$" | awk '{print $9}' | sort
    echo ""
    echo "Main binaries:"
    ls -la target/release/think-ai 2>/dev/null && echo "✓ CLI available"
    ls -la target/release/think-ai-server 2>/dev/null && echo "✓ Server available"
    ls -la target/release/process-manager 2>/dev/null && echo "✓ Process manager available"
else
    echo "❌ No modules built successfully"
    echo ""
    echo "Errors summary:"
    grep -E "error\[E[0-9]+\]:" full-release-build.log | sort | uniq -c | head -20
fi

echo ""
echo "For deployment:"
echo "1. Use only the successfully built binaries"
echo "2. Update Dockerfile to copy specific binaries"
echo "3. Deploy with: railway up"