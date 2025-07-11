#!/bin/bash

# Quick screenshot capture for markdown rendering evidence

echo "Capturing screenshots of Think AI markdown rendering..."

# Create directory
mkdir -p markdown_evidence

# Use the already installed chromium
CHROMIUM="/usr/bin/chromium-browser"

# Start simple HTTP server
echo "Starting HTTP server..."
python3 -m http.server 8090 &
SERVER_PID=$!
sleep 2

# Function to take screenshot
take_screenshot() {
    local url=$1
    local output=$2
    
    # Try different chromium commands
    if command -v chromium-browser &> /dev/null; then
        chromium-browser --headless --disable-gpu --screenshot="$output" --window-size=1280,1024 "$url" 2>/dev/null
    elif command -v chromium &> /dev/null; then
        chromium --headless --disable-gpu --screenshot="$output" --window-size=1280,1024 "$url" 2>/dev/null
    elif command -v google-chrome &> /dev/null; then
        google-chrome --headless --disable-gpu --screenshot="$output" --window-size=1280,1024 "$url" 2>/dev/null
    fi
    
    if [ -f "$output" ]; then
        echo "✓ Captured: $output"
    else
        echo "✗ Failed to capture: $output"
    fi
}

# Take screenshots
echo "Taking screenshots..."
take_screenshot "http://localhost:8090/minimal_3d.html" "markdown_evidence/custom_parser.png"
take_screenshot "http://localhost:8090/minimal_3d_markdown.html" "markdown_evidence/marked_js.png"

# Also capture with some test content via URL hash (if supported)
# This would require modifying the HTML to read from URL hash

# Stop server
kill $SERVER_PID 2>/dev/null

# Generate comparison HTML
cat > markdown_evidence/comparison.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Think AI Markdown Rendering Comparison</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .container { max-width: 1400px; margin: 0 auto; }
        .comparison { display: flex; gap: 20px; margin-top: 20px; }
        .version { flex: 1; }
        .version img { width: 100%; border: 1px solid #ddd; }
        h2 { color: #333; }
        .info { background: #f0f0f0; padding: 10px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Think AI Markdown Rendering Evidence</h1>
        
        <div class="info">
            <p><strong>Test Date:</strong> <span id="date"></span></p>
            <p><strong>Purpose:</strong> Compare markdown rendering between custom parser and marked.js implementation</p>
        </div>
        
        <div class="comparison">
            <div class="version">
                <h2>Custom Parser (minimal_3d.html)</h2>
                <img src="custom_parser.png" alt="Custom Parser">
                <p>Uses custom markdown parsing logic implemented in JavaScript</p>
            </div>
            
            <div class="version">
                <h2>Marked.js (minimal_3d_markdown.html)</h2>
                <img src="marked_js.png" alt="Marked.js">
                <p>Uses marked.js library with syntax highlighting via highlight.js</p>
            </div>
        </div>
        
        <h2>Key Features Tested</h2>
        <ul>
            <li>Headers (H1-H6)</li>
            <li>Bold, italic, and combined formatting</li>
            <li>Ordered and unordered lists</li>
            <li>Code blocks with syntax highlighting</li>
            <li>Inline code</li>
            <li>Links</li>
            <li>Blockquotes</li>
            <li>Tables (marked.js only)</li>
            <li>Line breaks and paragraphs</li>
        </ul>
    </div>
    
    <script>
        document.getElementById('date').textContent = new Date().toLocaleString();
    </script>
</body>
</html>
EOF

echo "✓ Comparison HTML created: markdown_evidence/comparison.html"

# List evidence files
echo -e "\nEvidence files created:"
ls -la markdown_evidence/

echo -e "\nTo view the comparison, open: markdown_evidence/comparison.html"