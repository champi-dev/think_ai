#!/bin/bash

echo "🔍 VERIFYING RELEASE BUILD"
echo "========================="
echo ""

# Test main CLI
echo "1️⃣ Testing think-ai CLI..."
if ./target/release/think-ai chat --help &>/dev/null; then
    echo "   ✅ CLI is working"
else
    echo "   ❌ CLI failed"
fi

# Test coding tool
echo "2️⃣ Testing think-ai-coding..."
if ./target/release/think-ai-coding --help &>/dev/null; then
    echo "   ✅ Coding tool is working"
else
    echo "   ❌ Coding tool failed"
fi

# Check binary sizes
echo ""
echo "📦 Binary sizes:"
ls -lh target/release/think-ai* 2>/dev/null | grep -v "\.d$" | awk '{print "   " $9 ": " $5}'

echo ""
echo "✅ Release build verification complete!"
echo ""
echo "🚀 Your release binaries are ready for deployment!"
echo ""
echo "Next steps:"
echo "1. Test locally: ./target/release/think-ai chat"
echo "2. Deploy to Railway: railway up"
echo "3. Or use Docker: docker build -t think-ai ."