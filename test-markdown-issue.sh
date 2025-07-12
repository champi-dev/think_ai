#\!/bin/bash
set -e

echo "🧪 Testing Markdown Rendering Issue"
echo "==================================="

# Kill existing server
echo "Stopping existing server..."
kill -9 $(lsof -t -i:3456) 2>/dev/null || true

# Start test server on local port
echo "Starting test server on port 3456..."
PORT=3456 ./target/release/stable-server-streaming &
SERVER_PID=$\!
sleep 3

# Test 1: Direct API call
echo -e "\n📝 Test 1: Direct API Response"
echo "--------------------------------"
RESPONSE=$(curl -s http://localhost:3456/api/chat -X POST \
    -H "Content-Type: application/json" \
    -d '{"message":"What is love?","stream":false}'  < /dev/null |  jq -r '.response' 2>/dev/null || echo "API Error")

echo "Raw Response (first 200 chars):"
echo "$RESPONSE" | head -c 200
echo -e "\n..."

# Test 2: Check for broken spacing
echo -e "\n\n🔍 Test 2: Checking for broken spacing patterns"
echo "------------------------------------------------"
if echo "$RESPONSE" | grep -E "[a-z] [a-z] [a-z]" > /dev/null; then
    echo "❌ FOUND broken spacing pattern\!"
    echo "Examples:"
    echo "$RESPONSE" | grep -oE ".{0,20}[a-z] [a-z] [a-z].{0,20}" | head -3
else
    echo "✅ No broken spacing found"
fi

# Test 3: Browser screenshot
echo -e "\n\n📸 Test 3: Taking browser screenshot"
echo "------------------------------------"
# Create test HTML page
cat > test-page.html << 'HTML'
<\!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial; padding: 20px; }
        #response { border: 1px solid #ccc; padding: 10px; background: #f0f0f0; }
    </style>
</head>
<body>
    <h2>Think AI Response Test</h2>
    <div id="response">Loading...</div>
    <script>
        fetch('http://localhost:3456/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message: 'What is physics?', stream: false})
        })
        .then(r => r.json())
        .then(data => {
            document.getElementById('response').textContent = data.response;
        });
    </script>
</body>
</html>
HTML

# Use a simple Python HTTP server for the test page
python3 -m http.server 8888 > /dev/null 2>&1 &
PYTHON_PID=$\!
sleep 1

echo "Test page available at: http://localhost:8888/test-page.html"
echo "Please open in browser to see rendering"

# Clean up
echo -e "\n\n🧹 Press Enter to clean up..."
read
kill $SERVER_PID 2>/dev/null || true
kill $PYTHON_PID 2>/dev/null || true
rm test-page.html

echo "✅ Test complete\!"
