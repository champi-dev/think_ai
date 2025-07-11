#!/bin/bash

echo "Testing markdown rendering improvements..."

# Kill any process using port 3456
echo "Killing any process on port 3456..."
lsof -ti:3456 | xargs kill -9 2>/dev/null || true

# Start a simple HTTP server for testing
echo "Starting test server on port 3456..."
cd /home/administrator/think_ai
python3 -m http.server 3456 > /dev/null 2>&1 &
SERVER_PID=$!

# Wait for server to start
sleep 2

echo ""
echo "✅ Test server started!"
echo ""
echo "To test the markdown rendering improvements:"
echo ""
echo "1. Open your browser and go to: http://localhost:3456/minimal_3d_markdown.html"
echo ""
echo "2. Click on 'Send' to see the welcome message with markdown"
echo ""
echo "3. Test the following markdown features:"
echo "   - Headers (# H1, ## H2, etc)"
echo "   - Code blocks with syntax highlighting"
echo "   - Copy buttons on code blocks (hover to see, click to copy)"
echo "   - Tables with proper formatting"
echo "   - Lists (ordered and unordered)"
echo "   - Links and emphasis"
echo ""
echo "4. Try sending a message with code:"
echo '   ```python'
echo '   def hello_world():'
echo '       print("Hello, World!")'
echo '   ```'
echo ""
echo "5. The copy button should appear when you hover over code blocks"
echo ""
echo "Press Ctrl+C to stop the test server"
echo ""

# Wait for user to stop
trap "kill $SERVER_PID 2>/dev/null; echo 'Test server stopped.'; exit" INT
wait