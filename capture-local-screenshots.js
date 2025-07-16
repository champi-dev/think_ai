const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LOCAL_URL = 'http://localhost:5173';

const RESOLUTIONS = [
  { width: 400, height: 600, name: 'ultra-small' },
  { width: 320, height: 480, name: 'iphone-se' },
  { width: 300, height: 400, name: 'tiny' },
  { width: 200, height: 300, name: 'micro' },
  { width: 150, height: 150, name: 'extreme-micro' },
  { width: 100, height: 100, name: 'minimum' }
];

async function captureScreenshots() {
  // Create screenshots directory
  const screenshotsDir = path.join(process.cwd(), 'screenshots', 'local');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  const browser = await chromium.launch({
    headless: true
  });

  console.log('📸 Capturing screenshots from local development...\n');

  for (const { width, height, name } of RESOLUTIONS) {
    console.log(`Testing ${width}x${height} (${name})...`);
    
    const context = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor: 2, // High quality screenshots
      isMobile: width <= 480
    });

    const page = await context.newPage();
    
    try {
      // Navigate to local site
      await page.goto(LOCAL_URL, { 
        waitUntil: 'networkidle',
        timeout: 30000 
      });

      // Wait a bit for any animations to complete
      await page.waitForTimeout(1000);

      // Capture initial state
      await page.screenshot({
        path: path.join(screenshotsDir, `${name}-${width}x${height}-initial.png`),
        fullPage: false
      });

      // Capture some metrics
      const metrics = await page.evaluate(() => {
        const body = document.body;
        const bodyStyles = window.getComputedStyle(body);
        const input = document.querySelector('#queryInput');
        const inputStyles = input ? window.getComputedStyle(input) : null;
        const header = document.querySelector('.header');
        const headerVisible = header ? window.getComputedStyle(header).display !== 'none' : false;
        
        // Check for our custom CSS at small resolutions
        const hasCustomCSS = window.innerWidth <= 400 && bodyStyles.animation === 'none';
        
        return {
          bodyFontSize: bodyStyles.fontSize,
          inputFontSize: inputStyles?.fontSize,
          headerVisible,
          inputHeight: input ? input.offsetHeight : 0,
          hasCustomCSS,
          animations: Array.from(document.querySelectorAll('*')).some(el => {
            const styles = window.getComputedStyle(el);
            return styles.animation !== 'none' && styles.animation !== '';
          })
        };
      });

      console.log(`  ✓ Captured screenshot`);
      console.log(`    Body font: ${metrics.bodyFontSize}`);
      console.log(`    Input font: ${metrics.inputFontSize || 'N/A'}`);
      console.log(`    Header visible: ${metrics.headerVisible}`);
      console.log(`    Input height: ${metrics.inputHeight}px`);
      console.log(`    Custom CSS applied: ${metrics.hasCustomCSS}`);
      console.log(`    Animations: ${metrics.animations ? 'Yes' : 'No'}`);
      console.log('');

    } catch (error) {
      console.error(`  ❌ Error at ${width}x${height}: ${error.message}`);
    } finally {
      await context.close();
    }
  }

  await browser.close();
  
  console.log('✅ Screenshot capture complete!');
  console.log(`📁 Screenshots saved to: ${screenshotsDir}`);
}

// Run the screenshot capture
captureScreenshots().catch(console.error);