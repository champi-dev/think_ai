#!/bin/bash

echo "🧪 Think AI PWA E2E Tests (Production - thinkai.lat)"
echo "==================================================="
echo ""

PROD_URL="https://thinkai.lat"
PASSED=0
FAILED=0

# Function to test and report
test_e2e() {
    local test_name="$1"
    local command="$2"
    
    echo -n "Testing: $test_name... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo "✅ PASSED"
        ((PASSED++))
    else
        echo "❌ FAILED"
        ((FAILED++))
    fi
}

# Test 1: Check if manifest.json is accessible
test_e2e "Manifest.json is accessible" \
    "curl -s -o /dev/null -w '%{http_code}' $PROD_URL/manifest.json | grep -q 200"

# Test 2: Check if service worker is accessible
test_e2e "Service worker (sw.js) is accessible" \
    "curl -s -o /dev/null -w '%{http_code}' $PROD_URL/sw.js | grep -q 200"

# Test 3: Verify manifest.json content
echo ""
echo "📋 Checking manifest.json content..."
MANIFEST_CONTENT=$(curl -s $PROD_URL/manifest.json)

test_e2e "Manifest has correct name" \
    "echo '$MANIFEST_CONTENT' | grep -q 'Think AI'"

test_e2e "Manifest has start_url" \
    "echo '$MANIFEST_CONTENT' | grep -q 'start_url'"

test_e2e "Manifest has display mode" \
    "echo '$MANIFEST_CONTENT' | grep -q 'standalone'"

test_e2e "Manifest has icons array" \
    "echo '$MANIFEST_CONTENT' | grep -q 'icons'"

# Test 4: Check service worker content
echo ""
echo "⚙️  Checking service worker content..."
SW_CONTENT=$(curl -s $PROD_URL/sw.js)

test_e2e "Service worker has install event" \
    "echo '$SW_CONTENT' | grep -q 'install'"

test_e2e "Service worker has activate event" \
    "echo '$SW_CONTENT' | grep -q 'activate'"

test_e2e "Service worker has fetch event" \
    "echo '$SW_CONTENT' | grep -q 'fetch'"

test_e2e "Service worker has NO caching (as requested)" \
    "! echo '$SW_CONTENT' | grep -q 'caches.open'"

# Test 5: Check HTML for PWA tags
echo ""
echo "🌐 Checking HTML for PWA integration..."
HTML_CONTENT=$(curl -s $PROD_URL)

test_e2e "HTML links to manifest.json" \
    "echo '$HTML_CONTENT' | grep -q 'manifest.json'"

test_e2e "HTML has theme-color meta tag" \
    "echo '$HTML_CONTENT' | grep -q 'theme-color'"

test_e2e "HTML has apple-mobile-web-app meta tags" \
    "echo '$HTML_CONTENT' | grep -q 'apple-mobile-web-app'"

test_e2e "HTML has install button" \
    "echo '$HTML_CONTENT' | grep -q 'pwaInstallButton'"

test_e2e "HTML has service worker registration" \
    "echo '$HTML_CONTENT' | grep -q 'serviceWorker.register'"

# Test 6: Check icon availability
echo ""
echo "🎨 Checking PWA icons..."
test_e2e "Icon 192x192 is accessible" \
    "curl -s -o /dev/null -w '%{http_code}' $PROD_URL/icon-192.png | grep -q 200"

test_e2e "Icon 512x512 is accessible" \
    "curl -s -o /dev/null -w '%{http_code}' $PROD_URL/icon-512.png | grep -q 200"

# Test 7: Check HTTPS (required for PWA)
echo ""
echo "🔒 Checking HTTPS requirements..."
test_e2e "Site is served over HTTPS" \
    "curl -s -o /dev/null -w '%{url_effective}' $PROD_URL | grep -q 'https://'"

# Test 8: Headers check
echo ""
echo "📡 Checking response headers..."
HEADERS=$(curl -s -I $PROD_URL)

test_e2e "Has proper Content-Type for HTML" \
    "echo '$HEADERS' | grep -i 'content-type' | grep -q 'text/html'"

# Summary
echo ""
echo "📊 E2E Test Summary"
echo "=================="
echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo "📈 Success Rate: $(( PASSED * 100 / (PASSED + FAILED) ))%"

echo ""
if [ $FAILED -eq 0 ]; then
    echo "🎉 All PWA E2E tests passed in production!"
    echo ""
    echo "📱 The PWA is ready for installation at $PROD_URL"
    echo "   - Desktop: Look for install icon in address bar"
    echo "   - Mobile: Use browser menu > 'Add to Home Screen'"
    exit 0
else
    echo "⚠️  Some E2E tests failed. Please check the production deployment."
    exit 1
fi