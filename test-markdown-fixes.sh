#!/bin/bash

echo "=== Testing Markdown Rendering Improvements ==="
echo

# Kill any existing processes on port 8888
echo "Cleaning up port 8888..."
lsof -ti:8888 | xargs kill -9 2>/dev/null || true
sleep 1

# Create a simple comparison page
cat > markdown_comparison.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Markdown Rendering Comparison</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        .panel {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        h2 {
            color: #666;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        iframe {
            width: 100%;
            height: 600px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .test-content {
            background: #f9f9f9;
            padding: 15px;
            border-radius: 4px;
            margin-top: 20px;
            white-space: pre-wrap;
            font-family: monospace;
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h1>Markdown Rendering Improvements Test</h1>
    
    <div class="container">
        <div class="panel">
            <h2>Original minimal_3d.html</h2>
            <iframe src="http://localhost:8888/original"></iframe>
        </div>
        <div class="panel">
            <h2>Fixed minimal_3d_fixed.html</h2>
            <iframe src="http://localhost:8888/fixed"></iframe>
        </div>
    </div>
    
    <div class="test-content">
<h3>Test Content Being Rendered:</h3>
# Long Words Test
supercalifragilisticexpialidocious https://example.com/very/long/path/that/should/wrap/properly

## Code Wrapping
\`const veryLongVariableNameThatShouldWrapProperly = 'This is a very long string';\`

## List Items
1. This is a numbered list item with a very long line of text that should wrap properly without breaking
2. Another item with **bold** and *italic* text

## Paragraphs
This is a paragraph with multiple sentences. Each sentence should flow naturally.

Here's a paragraph with manual line breaks:
First line
Second line  
Third line with hard break
    </div>
</body>
</html>
EOF

# Start the test server
echo "Starting test server on http://localhost:8888"
python3 << 'EOF'
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class TestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/original':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('minimal_3d.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/fixed':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('minimal_3d_fixed.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('markdown_comparison.html', 'rb') as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()

print("Test server running on http://localhost:8888")
print("Open your browser to see the comparison")
print("Press Ctrl+C to stop")

httpd = HTTPServer(('localhost', 8888), TestHandler)
httpd.serve_forever()
EOF