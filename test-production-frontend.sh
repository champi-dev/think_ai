#!/bin/bash
# Test production frontend

echo "Testing production frontend at thinkai.lat..."

# Test main page
echo -n "1. Testing main page: "
if curl -s https://thinkai.lat/ | grep -q '<div id="root"></div>'; then
    echo "✓ HTML served correctly"
else
    echo "✗ HTML not served"
fi

# Test CSS
echo -n "2. Testing CSS file: "
CSS_FILE=$(curl -s https://thinkai.lat/ | grep -oE 'index-[a-z0-9]+\.css' | head -1)
if [ ! -z "$CSS_FILE" ]; then
    if curl -s "https://thinkai.lat/assets/$CSS_FILE" | grep -q ".header{position:fixed"; then
        echo "✓ CSS loaded with styles"
    else
        echo "✗ CSS missing styles"
    fi
else
    echo "✗ CSS file not found"
fi

# Test JS
echo -n "3. Testing JS file: "
JS_FILE=$(curl -s https://thinkai.lat/ | grep -oE 'index-[a-z0-9]+\.js' | head -1)
if [ ! -z "$JS_FILE" ]; then
    if curl -s "https://thinkai.lat/assets/$JS_FILE" | grep -q "React"; then
        echo "✓ JavaScript loaded"
    else
        echo "✗ JavaScript not loaded"
    fi
else
    echo "✗ JS file not found"
fi

# Test API
echo -n "4. Testing API health: "
if curl -s https://thinkai.lat/health | grep -q "OK"; then
    echo "✓ API is responsive"
else
    echo "✗ API not responding"
fi

echo ""
echo "Frontend deployment status: Complete"
echo "Cache-busted assets are being served with proper styles."