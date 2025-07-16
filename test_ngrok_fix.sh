#!/bin/bash

# Unit tests for ngrok fix

echo "=== Testing ngrok wrapper fix ==="

# Test 1: Check if wrapper has correct shebang
echo -n "Test 1 - Checking shebang line... "
if head -n1 /home/administrator/think_ai/ngrok-wrapper.sh | grep -q "^#!/bin/bash$"; then
    echo "PASS"
else
    echo "FAIL"
    exit 1
fi

# Test 2: Check if wrapper is executable
echo -n "Test 2 - Checking executable permissions... "
if [ -x /home/administrator/think_ai/ngrok-wrapper.sh ]; then
    echo "PASS"
else
    echo "FAIL"
    exit 1
fi

# Test 3: Check if ngrok service is running
echo -n "Test 3 - Checking ngrok service status... "
if systemctl is-active --quiet ngrok-thinkai.service; then
    echo "PASS"
else
    echo "FAIL"
    exit 1
fi

# Test 4: Check if ngrok process is running
echo -n "Test 4 - Checking ngrok process... "
if pgrep -f "ngrok http 8080" > /dev/null; then
    echo "PASS"
else
    echo "FAIL"
    exit 1
fi

# Test 5: Check if conflicting services are stopped
echo -n "Test 5 - Checking conflicting services are stopped... "
if ! systemctl is-active --quiet think-ai.service && ! systemctl is-active --quiet think-ai-http.service; then
    echo "PASS"
else
    echo "FAIL"
    exit 1
fi

# Test 6: Check if think-ai-full service is running
echo -n "Test 6 - Checking think-ai-full service... "
if systemctl is-active --quiet think-ai-full.service; then
    echo "PASS"
else
    echo "FAIL"
    exit 1
fi

# Test 7: Check if port 8080 is listening
echo -n "Test 7 - Checking port 8080 is listening... "
if sudo lsof -i :8080 | grep -q LISTEN; then
    echo "PASS"
else
    echo "FAIL"
    exit 1
fi

# Test 8: Check if domain responds with 200 OK
echo -n "Test 8 - Checking domain response... "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://thinkai.lat)
if [ "$HTTP_CODE" = "200" ]; then
    echo "PASS"
else
    echo "FAIL (HTTP $HTTP_CODE)"
    exit 1
fi

echo "=== All unit tests passed! ==="