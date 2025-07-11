#!/bin/bash
# Local test script for Think AI markdown rendering

echo "======================================"
echo "Think AI Markdown Rendering Test"
echo "======================================"

# Check for chromium
if ! command -v chromium-browser &> /dev/null && ! command -v chromium &> /dev/null; then
    echo "⚠️  Chromium not found. Screenshots will be skipped."
    echo "   Install with: sudo apt-get install chromium-browser"
    SKIP_SCREENSHOTS=true
else
    SKIP_SCREENSHOTS=false
fi

# Create evidence directory
mkdir -p markdown_evidence

# Start HTTP server
echo "Starting local server on port 8090..."
python3 -m http.server 8090 &
SERVER_PID=$!
sleep 2

echo ""
echo "✅ Server running! You can now:"
echo ""
echo "1. View Custom Parser:"
echo "   http://localhost:8090/minimal_3d.html"
echo ""
echo "2. View Marked.js Version:"  
echo "   http://localhost:8090/minimal_3d_markdown.html"
echo ""
echo "3. View test markdown content:"
echo "   http://localhost:8090/markdown_test_content.md"
echo ""

if [ "$SKIP_SCREENSHOTS" = false ]; then
    echo "Taking screenshots..."
    
    # Take screenshots
    if command -v chromium-browser &> /dev/null; then
        CHROMIUM="chromium-browser"
    else
        CHROMIUM="chromium"
    fi
    
    $CHROMIUM --headless --disable-gpu --screenshot="markdown_evidence/test_custom.png" \
              --window-size=1280,1024 "http://localhost:8090/minimal_3d.html" 2>/dev/null
              
    $CHROMIUM --headless --disable-gpu --screenshot="markdown_evidence/test_marked.png" \
              --window-size=1280,1024 "http://localhost:8090/minimal_3d_markdown.html" 2>/dev/null
    
    echo "✅ Screenshots saved to markdown_evidence/"
fi

echo ""
echo "4. View comparison (if screenshots taken):"
echo "   http://localhost:8090/markdown_evidence/comparison_full.html"
echo ""
echo "Press Ctrl+C to stop the server..."
echo ""

# Wait for user to stop
trap "kill $SERVER_PID 2>/dev/null; echo 'Server stopped.'; exit" INT
wait $SERVER_PID