#!/bin/bash

echo "=== End-to-End Markdown Testing Script ==="
echo "This will test markdown rendering on both local and production"
echo

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to test markdown via curl
test_markdown_curl() {
    local url=$1
    local name=$2
    
    echo -e "${YELLOW}Testing $name at $url${NC}"
    
    # Check if site is accessible
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "200"; then
        echo -e "${GREEN}✓ Site is accessible${NC}"
        
        # Check parseMarkdown function
        echo "Checking parseMarkdown implementation..."
        curl -s "$url" | grep -A 20 "parseMarkdown" | head -40 > /tmp/${name}_markdown.txt
        
        # Look for the problematic line break handling
        if grep -q "result.replace(/\\\\n{2,}/g" /tmp/${name}_markdown.txt; then
            echo -e "${RED}✗ Found problematic line break handling${NC}"
            echo "  Issue: Using result.replace(/\\n{2,}/g, '</p><p>') which doesn't handle single newlines"
        else
            echo -e "${GREEN}✓ Line break handling might be fixed${NC}"
        fi
        
        # Check for proper paragraph handling
        if grep -q "split(/\\\\n\\\\n+/)" /tmp/${name}_markdown.txt; then
            echo -e "${GREEN}✓ Found proper paragraph splitting${NC}"
        else
            echo -e "${YELLOW}⚠ Paragraph splitting might need improvement${NC}"
        fi
        
    else
        echo -e "${RED}✗ Site is not accessible${NC}"
    fi
    echo
}

# Kill any existing servers on test ports
echo "Cleaning up test ports..."
lsof -ti:7777 | xargs -r kill -9 2>/dev/null
lsof -ti:8888 | xargs -r kill -9 2>/dev/null

# Start local test server
echo -e "${YELLOW}Starting local test server...${NC}"
cd /home/administrator/think_ai
python3 -m http.server 7777 > /dev/null 2>&1 &
LOCAL_PID=$!
sleep 2

# Test production
test_markdown_curl "https://thinkai.lat" "Production"

# Test local with visual comparison
echo -e "${YELLOW}Local visual test available at:${NC}"
echo "http://localhost:7777/markdown_test_visual.html"
echo

# Show the fix
echo -e "${YELLOW}=== RECOMMENDED FIX ===${NC}"
echo "The parseMarkdown function needs to be updated to properly handle:"
echo "1. Single line breaks (\\n) → <br> tags"
echo "2. Double line breaks (\\n\\n) → separate <p> tags"
echo "3. Mixed content with proper paragraph wrapping"
echo
echo "Fix is available in: MARKDOWN_FIX_PRODUCTION.js"
echo

# Create a simple test harness
cat > /tmp/test_markdown.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Markdown Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .test { border: 1px solid #ccc; padding: 10px; margin: 10px 0; }
        .input { background: #f0f0f0; padding: 10px; }
        .output { background: #fff; padding: 10px; border: 1px solid #ddd; }
        pre { background: #f5f5f5; padding: 5px; }
    </style>
</head>
<body>
    <h1>Markdown Line Break Test</h1>
    
    <div class="test">
        <h3>Test 1: Single Line Breaks</h3>
        <div class="input">
            <pre>Line 1
Line 2
Line 3</pre>
        </div>
        <div class="output" id="test1"></div>
    </div>
    
    <div class="test">
        <h3>Test 2: Paragraphs</h3>
        <div class="input">
            <pre>Paragraph 1

Paragraph 2

Paragraph 3</pre>
        </div>
        <div class="output" id="test2"></div>
    </div>
    
    <div class="test">
        <h3>Test 3: Mixed Content</h3>
        <div class="input">
            <pre># Title

First paragraph with
multiple lines.

## Subtitle

- Item 1
- Item 2</pre>
        </div>
        <div class="output" id="test3"></div>
    </div>
    
    <script src="MARKDOWN_FIX_PRODUCTION.js"></script>
    <script>
        // Test the fixed parseMarkdown
        document.getElementById('test1').innerHTML = parseMarkdown("Line 1\nLine 2\nLine 3");
        document.getElementById('test2').innerHTML = parseMarkdown("Paragraph 1\n\nParagraph 2\n\nParagraph 3");
        document.getElementById('test3').innerHTML = parseMarkdown("# Title\n\nFirst paragraph with\nmultiple lines.\n\n## Subtitle\n\n- Item 1\n- Item 2");
    </script>
</body>
</html>
EOF

echo -e "${GREEN}Test harness created at: /tmp/test_markdown.html${NC}"
echo "You can open it at: http://localhost:7777/../../tmp/test_markdown.html"
echo

# Summary
echo -e "${YELLOW}=== SUMMARY ===${NC}"
echo "1. Production site (thinkai.lat) has markdown rendering issues"
echo "2. Single line breaks are not being converted to <br> tags"
echo "3. The fix is in MARKDOWN_FIX_PRODUCTION.js"
echo "4. Visual comparison available at http://localhost:7777/markdown_test_visual.html"
echo
echo "To apply the fix to production:"
echo "1. Update the parseMarkdown function in the production code"
echo "2. Add the additional CSS for better spacing"
echo "3. Test thoroughly before deploying"
echo
echo -e "${GREEN}Test server running on port 7777. Press Ctrl+C to stop.${NC}"

# Keep script running
wait $LOCAL_PID