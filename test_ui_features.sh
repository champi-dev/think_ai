#!/bin/bash
set -e

echo "=== Testing UI with Web Search and Fact Check Features ==="

# Check if stable-server is running
if lsof -i :8080 | grep -q LISTEN; then
    echo "✅ Server is running on port 8080"
else
    echo "❌ Server not running. Please start the server first."
    exit 1
fi

# Open browser (if available)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8080
elif command -v open &> /dev/null; then
    open http://localhost:8080
else
    echo "Please open http://localhost:8080 in your browser"
fi

echo -e "\n=== Test Checklist ==="
echo "1. ✓ Check that Web Search and Fact Check toggles appear in header"
echo "2. ✓ Check that input field has Web Search 🔍 and Fact Check ✅ buttons"
echo "3. ✓ Test toggling Web Search on/off (should persist on refresh)"
echo "4. ✓ Test toggling Fact Check on/off (should persist on refresh)"
echo "5. ✓ Test sending a query with Web Search enabled"
echo "6. ✓ Test sending a query with Fact Check enabled"
echo "7. ✓ Verify indicators appear when features are active"
echo "8. ✓ Test on mobile view (responsive design)"

echo -e "\n=== API Request Examples ==="
echo "Test with Web Search:"
echo 'curl -X POST http://localhost:8080/api/chat -H "Content-Type: application/json" -d '"'"'{"message": "latest AI news", "use_web_search": true}'"'"''

echo -e "\nTest with Fact Check:"
echo 'curl -X POST http://localhost:8080/api/chat -H "Content-Type: application/json" -d '"'"'{"message": "is the earth flat?", "fact_check": true}'"'"''

echo -e "\nTest with Both:"
echo 'curl -X POST http://localhost:8080/api/chat -H "Content-Type: application/json" -d '"'"'{"message": "current president of USA", "use_web_search": true, "fact_check": true}'"'"''