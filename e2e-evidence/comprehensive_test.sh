#\!/bin/bash

echo "🔍 E2E Testing Think AI Production (thinkai.lat)"
echo "=============================================="
echo ""

# Test 1: Check page structure
echo "📄 Test 1: Checking page structure..."
curl -s https://thinkai.lat > page_content.html

# Check if feature toggles are NOT in header
if grep -q 'class="header".*class="feature-toggles"' page_content.html; then
    echo "❌ FAIL: Feature toggles found in header"
else
    echo "✅ PASS: No feature toggles in header"
fi

# Check if web search and fact check are in input area
if grep -q 'id="webSearchBtn"' page_content.html && grep -q 'id="factCheckBtn"' page_content.html; then
    echo "✅ PASS: Web Search and Fact Check buttons found in input area"
else
    echo "❌ FAIL: Buttons not found in input area"
fi

echo ""
echo "🔧 Test 2: Finding JavaScript error source..."

# Look for the problematic line around 1500
sed -n '1490,1510p' page_content.html  < /dev/null |  grep -n "addEventListener" > error_context.txt

echo "JavaScript around line 1500:"
sed -n '1495,1505p' page_content.html

