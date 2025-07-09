#!/bin/bash

echo "Final syntax error fixes for think-ai-knowledge module..."
echo "======================================================"

cd ../think-ai-knowledge

# Run a comprehensive check to find all remaining files with syntax errors
echo "Current syntax errors:"
cargo check --message-format=short 2>&1 | grep -E "error:|error\[" | head -20

echo ""
echo "Creating test script to verify all fixes..."

# Create a verification script
cat > verify-syntax.sh << 'VERIFY_EOF'
#!/bin/bash
echo "Verifying syntax fixes..."
cargo check 2>&1 | grep -E "error:|error\[" | wc -l
VERIFY_EOF

chmod +x verify-syntax.sh

echo ""
echo "Running syntax verification..."
ERROR_COUNT=$(./verify-syntax.sh)
echo "Remaining syntax errors: $ERROR_COUNT"

if [ "$ERROR_COUNT" -eq "0" ]; then
    echo "✅ All syntax errors fixed!"
else
    echo "❌ Still have syntax errors to fix"
fi