#!/bin/bash

echo "🧪 Testing Tooltip Removal"
echo "========================="
echo ""

# Function to check HTML files for tooltips
check_tooltips() {
    local file=$1
    local filename=$(basename "$file")
    
    echo "Checking $filename..."
    
    # Check for title attributes on search/fact check buttons
    if grep -q 'id="webSearchBtn".*title=' "$file" || grep -q 'id="factCheckBtn".*title=' "$file"; then
        echo "❌ Found title attributes on buttons"
        return 1
    fi
    
    # Check for feature-tooltip divs
    if grep -q '<div class="feature-tooltip">' "$file"; then
        echo "❌ Found feature-tooltip divs"
        return 1
    fi
    
    # Check for feature-tooltip CSS
    if grep -q '\.feature-tooltip' "$file"; then
        echo "❌ Found feature-tooltip CSS rules"
        return 1
    fi
    
    echo "✅ No tooltips found"
    return 0
}

# Test main index.html
echo "1. Testing main index.html"
check_tooltips "/home/administrator/think_ai/static/index.html"
result1=$?

echo ""
echo "2. Testing backup index_with_search_factcheck.html"
check_tooltips "/home/administrator/think_ai/static/index_with_search_factcheck.html"
result2=$?

echo ""
echo "3. Verifying button structure"
echo "Main index.html buttons:"
grep -A1 -B1 'id="webSearchBtn"\|id="factCheckBtn"' /home/administrator/think_ai/static/index.html | head -10

echo ""
echo "📊 Summary"
echo "=========="
if [ $result1 -eq 0 ] && [ $result2 -eq 0 ]; then
    echo "✅ All tooltips successfully removed!"
else
    echo "❌ Some tooltips still present"
    exit 1
fi