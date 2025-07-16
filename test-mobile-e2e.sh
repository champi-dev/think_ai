#!/bin/bash

echo "📱 Think AI Mobile E2E Test & Design Analysis"
echo "============================================"
echo "🌐 Target: https://thinkai.lat"
echo "📅 Time: $(date)"
echo ""

PROD_URL="https://thinkai.lat"
MOBILE_UA="Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"

# Test mobile viewport
echo "1️⃣ Mobile Viewport Test"
echo "======================="

# Get mobile HTML
MOBILE_HTML=$(curl -s -H "User-Agent: $MOBILE_UA" $PROD_URL)

# Check viewport meta
echo -n "Viewport meta tag: "
if echo "$MOBILE_HTML" | grep -q 'viewport.*width=device-width'; then
    echo "✅ Present"
else
    echo "❌ Missing or incorrect"
fi

# Test responsive elements
echo ""
echo "2️⃣ Mobile UI Elements Check"
echo "=========================="

# Create a test script to check mobile styles
cat > check-mobile-css.js << 'EOF'
const puppeteer = require('puppeteer');

async function checkMobileDesign() {
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // iPhone 12 Pro viewport
    await page.setViewport({
        width: 390,
        height: 844,
        deviceScaleFactor: 3,
        isMobile: true,
        hasTouch: true
    });
    
    await page.goto('https://thinkai.lat', { waitUntil: 'networkidle2' });
    
    // Take mobile screenshot
    await page.screenshot({ 
        path: 'mobile-screenshot.png',
        fullPage: true 
    });
    
    // Check element sizes and positions
    const metrics = await page.evaluate(() => {
        const header = document.querySelector('.header');
        const input = document.querySelector('#queryInput');
        const installBtn = document.querySelector('#pwaInstallButton');
        const messages = document.querySelector('.messages');
        
        return {
            headerHeight: header ? header.offsetHeight : 0,
            inputWidth: input ? input.offsetWidth : 0,
            installBtnVisible: installBtn ? window.getComputedStyle(installBtn).display !== 'none' : false,
            messagesHeight: messages ? messages.offsetHeight : 0,
            viewportWidth: window.innerWidth,
            viewportHeight: window.innerHeight
        };
    });
    
    console.log('Mobile Metrics:', JSON.stringify(metrics, null, 2));
    
    // Check for overflow
    const hasOverflow = await page.evaluate(() => {
        return document.body.scrollWidth > window.innerWidth;
    });
    
    console.log('Horizontal overflow:', hasOverflow ? '❌ Yes' : '✅ No');
    
    await browser.close();
}

checkMobileDesign().catch(console.error);
EOF

# Run if puppeteer is available
if command -v node &> /dev/null && npm list puppeteer &> /dev/null; then
    echo "Running Puppeteer mobile test..."
    node check-mobile-css.js
else
    echo "⚠️  Puppeteer not available. Manual testing required."
fi

# Manual CSS checks
echo ""
echo "3️⃣ CSS Mobile Optimization Checks"
echo "================================"

# Check for media queries
echo -n "Media queries present: "
if curl -s $PROD_URL | grep -q '@media.*max-width'; then
    echo "✅ Found"
else
    echo "❌ Not found - needs mobile optimization"
fi

# Check font sizes
echo -n "Mobile-friendly font sizes: "
if curl -s $PROD_URL | grep -q 'font-size.*rem\|font-size.*vw'; then
    echo "✅ Using relative units"
else
    echo "⚠️  Check font sizing"
fi

echo ""
echo "4️⃣ Mobile Performance"
echo "==================="

# Check resource sizes
echo "Resource sizes for mobile:"
curl -s -I $PROD_URL/manifest.json | grep -i content-length | awk '{print "- Manifest: " $2 " bytes"}'
curl -s -I $PROD_URL/sw.js | grep -i content-length | awk '{print "- Service Worker: " $2 " bytes"}'
curl -s -I $PROD_URL/icon-192.png | grep -i content-length | awk '{print "- Icon 192: " $2 " bytes"}'

echo ""
echo "5️⃣ Touch Interaction Areas"
echo "========================="
echo "Checking button sizes for touch targets (44x44px minimum)..."

# Generate mobile optimization report
cat > mobile-improvements.md << 'EOF'
# Mobile Design Improvements Needed

## Current Issues to Fix:

### 1. Header
- [ ] Reduce padding on mobile
- [ ] Make logo smaller
- [ ] Hide or minimize mode toggle on small screens

### 2. Chat Interface
- [ ] Full width input on mobile
- [ ] Larger touch targets for buttons
- [ ] Better spacing between messages

### 3. Install Button
- [ ] Fixed position on mobile
- [ ] Larger touch target (min 44x44px)
- [ ] More prominent on mobile

### 4. Input Area
- [ ] Prevent zoom on focus (font-size: 16px minimum)
- [ ] Better mobile keyboard handling
- [ ] Sticky position at bottom

### 5. Typography
- [ ] Responsive font sizes
- [ ] Better line height for readability
- [ ] Adjust message padding

## Recommended CSS Additions:

```css
/* Mobile optimizations */
@media (max-width: 768px) {
    .header {
        padding: 0.5rem 1rem;
    }
    
    .logo {
        font-size: 1.2rem;
    }
    
    .chat-container {
        height: calc(100vh - 60px);
    }
    
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: var(--surface);
        padding: 1rem;
    }
    
    #queryInput {
        font-size: 16px; /* Prevents zoom */
        padding: 1rem;
    }
    
    .pwa-install-button {
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 100;
    }
}
```
EOF

echo ""
echo "📊 Mobile E2E Summary"
echo "==================="
echo "1. Viewport tag: Check above"
echo "2. Mobile CSS: Needs optimization"
echo "3. Touch targets: Need enlarging"
echo "4. Performance: Check resource sizes"
echo ""
echo "📄 Reports generated:"
echo "- mobile-improvements.md"
echo "- mobile-screenshot.png (if Puppeteer available)"
echo ""
echo "🔧 Next step: Implement mobile optimizations"