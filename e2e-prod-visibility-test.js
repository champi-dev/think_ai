const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PROD_URL = 'http://localhost:8080'; // Local systemd service

async function testProductionVisibility() {
    console.log('Starting production visibility test...');
    const browser = await chromium.launch({ 
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 }
    });
    
    const page = await context.newPage();
    
    // Capture console logs
    page.on('console', msg => console.log('Browser console:', msg.type(), msg.text()));
    page.on('pageerror', error => console.log('Browser error:', error.message));
    
    try {
        // Navigate to production
        console.log(`Navigating to ${PROD_URL}...`);
        await page.goto(PROD_URL, { 
            waitUntil: 'networkidle',
            timeout: 30000 
        });
        
        // Wait a bit for everything to render
        await page.waitForTimeout(3000);
        
        // Create screenshots directory
        const screenshotDir = path.join(__dirname, 'screenshots', 'prod-visibility-test');
        if (!fs.existsSync(screenshotDir)) {
            fs.mkdirSync(screenshotDir, { recursive: true });
        }
        
        // Take initial screenshot
        await page.screenshot({ 
            path: path.join(screenshotDir, '1-initial-load.png'),
            fullPage: true 
        });
        console.log('✓ Captured initial load screenshot');
        
        // Check if header is visible
        const headerVisible = await page.isVisible('.header');
        console.log(`Header visible: ${headerVisible}`);
        
        // Check if chat interface is visible
        const interfaceVisible = await page.isVisible('.interface');
        console.log(`Interface visible: ${interfaceVisible}`);
        
        // Check if messages area is visible
        const messagesVisible = await page.isVisible('.messages');
        console.log(`Messages area visible: ${messagesVisible}`);
        
        // Check if input is visible
        const inputVisible = await page.isVisible('#queryInput');
        console.log(`Input field visible: ${inputVisible}`);
        
        // Check if send button is visible
        const sendBtnVisible = await page.isVisible('#sendBtn');
        console.log(`Send button visible: ${sendBtnVisible}`);
        
        // Check background color of body
        const bodyBgColor = await page.evaluate(() => {
            const body = document.body;
            return window.getComputedStyle(body).backgroundColor;
        });
        console.log(`Body background color: ${bodyBgColor}`);
        
        // Check if any text content is visible
        const textContent = await page.textContent('body');
        console.log(`Has text content: ${textContent.length > 0}`);
        
        // Try to interact with the input
        if (inputVisible) {
            await page.click('#queryInput');
            await page.type('#queryInput', 'Hello, can you see this?');
            await page.screenshot({ 
                path: path.join(screenshotDir, '2-typed-message.png'),
                fullPage: true 
            });
            console.log('✓ Typed test message');
        }
        
        // Get computed styles of key elements
        const styles = await page.evaluate(() => {
            const elements = {
                body: document.body,
                header: document.querySelector('.header'),
                interface: document.querySelector('.interface'),
                messages: document.querySelector('.messages'),
                input: document.querySelector('#queryInput')
            };
            
            const results = {};
            for (const [key, el] of Object.entries(elements)) {
                if (el) {
                    const style = window.getComputedStyle(el);
                    results[key] = {
                        display: style.display,
                        visibility: style.visibility,
                        opacity: style.opacity,
                        zIndex: style.zIndex,
                        position: style.position,
                        backgroundColor: style.backgroundColor,
                        color: style.color
                    };
                }
            }
            return results;
        });
        
        console.log('\nComputed styles:');
        console.log(JSON.stringify(styles, null, 2));
        
        // Take screenshot of different viewports
        const viewports = [
            { name: 'mobile', width: 375, height: 667 },
            { name: 'tablet', width: 768, height: 1024 },
            { name: 'desktop-large', width: 1920, height: 1080 }
        ];
        
        for (const viewport of viewports) {
            await page.setViewportSize(viewport);
            await page.waitForTimeout(1000);
            await page.screenshot({ 
                path: path.join(screenshotDir, `3-${viewport.name}.png`),
                fullPage: true 
            });
            console.log(`✓ Captured ${viewport.name} screenshot`);
        }
        
        // Generate test report
        const report = {
            timestamp: new Date().toISOString(),
            url: PROD_URL,
            results: {
                headerVisible,
                interfaceVisible,
                messagesVisible,
                inputVisible,
                sendBtnVisible,
                hasTextContent: textContent.length > 0,
                bodyBackgroundColor: bodyBgColor,
                computedStyles: styles
            },
            status: headerVisible && interfaceVisible && messagesVisible && inputVisible ? 'PASS' : 'FAIL'
        };
        
        fs.writeFileSync(
            path.join(screenshotDir, 'test-report.json'),
            JSON.stringify(report, null, 2)
        );
        
        console.log(`\nTest Status: ${report.status}`);
        console.log(`Screenshots saved to: ${screenshotDir}`);
        
        return report.status === 'PASS';
        
    } catch (error) {
        console.error('Test failed:', error);
        await page.screenshot({ 
            path: path.join(__dirname, 'screenshots', 'prod-visibility-test', 'error-state.png'),
            fullPage: true 
        });
        return false;
    } finally {
        await browser.close();
    }
}

// Run the test
testProductionVisibility().then(success => {
    process.exit(success ? 0 : 1);
});