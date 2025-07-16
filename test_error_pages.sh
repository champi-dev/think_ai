#!/bin/bash
set -e

echo "=== Testing Error Pages Locally ==="

# Function to test page
test_page() {
    local page=$1
    local port=$2
    echo -e "\n📄 Testing $page on port $port..."
    
    # Start simple HTTP server
    cd /home/administrator/think_ai/static
    python3 -m http.server $port &
    SERVER_PID=$!
    
    # Wait for server to start
    sleep 2
    
    # Open browser if available
    if command -v xdg-open &> /dev/null; then
        xdg-open http://localhost:$port/$page
    elif command -v open &> /dev/null; then
        open http://localhost:$port/$page
    else
        echo "Please open http://localhost:$port/$page in your browser"
    fi
    
    echo "Press Enter to stop server and continue..."
    read
    
    # Kill server
    kill $SERVER_PID 2>/dev/null || true
    wait $SERVER_PID 2>/dev/null || true
}

# Test 404 page
test_page "404.html" 7777

# Test maintenance page
test_page "maintenance.html" 7778

echo -e "\n✅ Error pages tested successfully!"

echo -e "\n📋 Integration Instructions:"
echo "1. Copy nginx_error_pages.conf content to your nginx configuration"
echo "2. Reload nginx: sudo nginx -s reload"
echo "3. Test 404: curl -I http://thinkai.lat/nonexistent-page"
echo "4. Test maintenance: Stop the backend service and access the site"

echo -e "\n🚀 Production Deployment:"
echo "- 404.html will show when users access non-existent pages"
echo "- maintenance.html will show when backend is down (502/503/504 errors)"
echo "- Both pages have auto-refresh and quantum animations!"

echo -e "\n💡 Pro Tips:"
echo "- Maintenance page auto-refreshes every 30 seconds"
echo "- 404 page has interactive quantum particles"
echo "- Both pages maintain Think AI's visual identity"