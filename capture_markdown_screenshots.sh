#\!/bin/bash

# Script to capture screenshots of markdown rendering
# Uses the web interface to show actual rendering

set -e

echo "📸 Markdown Screenshot Capture Script"
echo "===================================="

# Create directory for screenshots
SCREENSHOT_DIR="markdown_rendering_proof"
mkdir -p "$SCREENSHOT_DIR"

# Check if server is running
if \! curl -s http://localhost:7777/health > /dev/null; then
    echo "❌ Server not running on port 7777"
    echo "Please run: python3 serve_webapp_7777_final.py"
    exit 1
fi

echo "✅ Server is running"

# Test the markdown directly via console
echo "🧪 Testing markdown rendering via browser console..."

# Create a test script
cat > "$SCREENSHOT_DIR/test_markdown.js" << 'JSEOF'
// Test markdown rendering in browser console
console.log("Testing markdown parser...");

const testCases = [
    {
        name: "Headers",
        input: "# H1\\n## H2\\n### H3",
        expected: ["<h1>", "<h2>", "<h3>"]
    },
    {
        name: "Bold/Italic", 
        input: "**bold** and *italic*",
        expected: ["<strong>", "<em>"]
    },
    {
        name: "Lists",
        input: "- Item 1\\n- Item 2\\n\\n1. First\\n2. Second",
        expected: ["<ul>", "<ol>", "<li>"]
    },
    {
        name: "Code",
        input: "Inline `code` and\\n```python\\nprint('hello')\\n```",
        expected: ["<code>", "<pre>"]
    }
];

// Run tests
testCases.forEach(test => {
    console.log(`\\nTesting: ${test.name}`);
    console.log(`Input: ${test.input}`);
    
    // Call the parseMarkdown function from the webapp
    if (typeof parseMarkdown === 'function') {
        const result = parseMarkdown(test.input);
        console.log(`Output HTML: ${result}`);
        
        const passed = test.expected.every(tag => result.includes(tag));
        console.log(`Result: ${passed ? '✅ PASS' : '❌ FAIL'}`);
    } else {
        console.log("❌ parseMarkdown function not found\!");
    }
});
JSEOF

echo "✅ Test script created"
echo ""
echo "📋 To run the tests:"
echo "1. Open http://localhost:7777 in your browser"
echo "2. Open Developer Console (F12)"
echo "3. Copy and paste the contents of $SCREENSHOT_DIR/test_markdown.js"
echo "4. Take screenshots of the results"
echo ""
echo "🔍 To verify binary usage:"
echo "   ps aux  < /dev/null |  grep stable-server-streaming"
echo "   lsof -i:7778"
echo ""
echo "📸 Take screenshots showing:"
echo "   - The webapp with markdown messages"
echo "   - The console showing test results"
echo "   - The network tab showing API calls"
