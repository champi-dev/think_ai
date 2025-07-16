#!/bin/bash

echo "🧪 Think AI Production E2E Test - 100% Verification"
echo "=================================================="
echo "🌐 Target: https://thinkai.lat"
echo "📅 Time: $(date)"
echo ""

PROD_URL="https://thinkai.lat"
PASSED=0
FAILED=0

# Enhanced test function with detailed output
test_feature() {
    local feature="$1"
    local test_cmd="$2"
    local expected="$3"
    
    echo -n "Testing $feature... "
    
    result=$(eval "$test_cmd" 2>&1)
    if echo "$result" | grep -q "$expected"; then
        echo "✅ PASSED"
        ((PASSED++))
        echo "  └─ Evidence: $(echo "$result" | grep "$expected" | head -1)"
    else
        echo "❌ FAILED"
        ((FAILED++))
        echo "  └─ Got: $(echo "$result" | head -1)"
        echo "  └─ Expected: $expected"
    fi
    echo ""
}

echo "1️⃣ PWA Core Files"
echo "=================="
test_feature "Manifest.json" \
    "curl -s $PROD_URL/manifest.json | jq -r .name" \
    "Think AI - O(1) Quantum Consciousness"

test_feature "Service Worker" \
    "curl -s $PROD_URL/sw.js | head -1" \
    "// Minimal Service Worker - No Caching"

test_feature "Icon 192x192" \
    "curl -sI $PROD_URL/icon-192.png | grep -i content-type" \
    "image/png"

test_feature "Icon 512x512" \
    "curl -sI $PROD_URL/icon-512.png | grep -i content-type" \
    "image/png"

echo "2️⃣ PWA HTML Integration"
echo "======================="
HTML=$(curl -s $PROD_URL)

test_feature "Manifest Link" \
    "echo '$HTML' | grep -o 'manifest.json'" \
    "manifest.json"

test_feature "Theme Color" \
    "echo '$HTML' | grep -o 'theme-color.*#[0-9a-f]*'" \
    "theme-color"

test_feature "Mobile Web App Capable" \
    "echo '$HTML' | grep -o 'mobile-web-app-capable'" \
    "mobile-web-app-capable"

test_feature "Install Button" \
    "echo '$HTML' | grep -o 'pwaInstallButton'" \
    "pwaInstallButton"

test_feature "Service Worker Registration" \
    "echo '$HTML' | grep -o 'serviceWorker.register'" \
    "serviceWorker.register"

echo "3️⃣ Language Detection"
echo "===================="
test_feature "Language Detector Script" \
    "curl -s $PROD_URL/js/language-detector.js | grep -o 'LanguageDetector'" \
    "LanguageDetector"

test_feature "Language Script Loading" \
    "echo '$HTML' | grep -o 'language-detector.js'" \
    "language-detector.js"

test_feature "Translation Attributes" \
    "echo '$HTML' | grep -o 'data-translate' | head -1" \
    "data-translate"

echo "4️⃣ API Functionality"
echo "==================="
test_feature "Health Check" \
    "curl -s $PROD_URL/health | jq -r .status" \
    "healthy"

test_feature "Chat API" \
    "curl -s -X POST $PROD_URL/api/chat -H 'Content-Type: application/json' -d '{\"query\":\"test\"}' | jq -r .response | wc -c" \
    "[1-9][0-9]*"

echo "5️⃣ Lighthouse PWA Score (Manual Check)"
echo "===================================="
echo "To verify PWA score:"
echo "1. Open Chrome DevTools on $PROD_URL"
echo "2. Go to Lighthouse tab"
echo "3. Run audit with 'Progressive Web App' checked"
echo "4. Expected: Green scores for PWA criteria"
echo ""

echo "6️⃣ Browser Install Test (Manual)"
echo "==============================="
echo "✓ Chrome: Address bar should show install icon"
echo "✓ Edge: Three dots menu > Apps > Install"
echo "✓ Mobile: Browser menu > Add to Home Screen"
echo "✓ Install button should be visible and pulsing"
echo ""

echo "📊 Final Score"
echo "============="
TOTAL=$((PASSED + FAILED))
PERCENTAGE=$((PASSED * 100 / TOTAL))

echo "✅ Passed: $PASSED"
echo "❌ Failed: $FAILED"
echo "📈 Success Rate: $PERCENTAGE%"
echo ""

if [ $PERCENTAGE -eq 100 ]; then
    echo "🎉 Perfect Score! All tests passed!"
    echo "✨ Think AI PWA is 100% production ready!"
else
    echo "⚠️  Some tests failed. Please fix the issues above."
fi

# Create detailed report
REPORT="e2e-report-$(date +%Y%m%d-%H%M%S).json"
cat > $REPORT << EOF
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "url": "$PROD_URL",
  "passed": $PASSED,
  "failed": $FAILED,
  "percentage": $PERCENTAGE,
  "pwa_ready": $([ $PERCENTAGE -eq 100 ] && echo "true" || echo "false")
}
EOF

echo ""
echo "📄 Report saved to: $REPORT"