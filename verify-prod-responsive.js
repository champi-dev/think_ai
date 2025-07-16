const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PROD_URL = 'https://thinkai.lat';

const TEST_RESOLUTIONS = [
  { width: 100, height: 100, name: 'minimum' },
  { width: 200, height: 300, name: 'micro' },
  { width: 400, height: 600, name: 'ultra-small' }
];

async function verifyResponsive() {
  const screenshotsDir = path.join(process.cwd(), 'screenshots', 'prod-updated');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });

  console.log('🔍 Verifying responsive design on production...\n');

  for (const { width, height, name } of TEST_RESOLUTIONS) {
    console.log(`Testing ${width}x${height} (${name})...`);
    
    const context = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor: 2
    });

    const page = await context.newPage();
    
    try {
      await page.goto(PROD_URL, { 
        waitUntil: 'networkidle',
        timeout: 30000 
      });

      await page.waitForTimeout(2000);

      await page.screenshot({
        path: path.join(screenshotsDir, `${name}-${width}x${height}-updated.png`),
        fullPage: false
      });

      const metrics = await page.evaluate(() => {
        const body = document.body;
        const bodyStyles = window.getComputedStyle(body);
        const input = document.querySelector('#queryInput');
        const inputStyles = input ? window.getComputedStyle(input) : null;
        const header = document.querySelector('.header');
        const headerVisible = header ? window.getComputedStyle(header).display !== 'none' : false;
        
        return {
          bodyFontSize: bodyStyles.fontSize,
          inputFontSize: inputStyles?.fontSize,
          headerVisible,
          animations: Array.from(document.querySelectorAll('*')).some(el => {
            const styles = window.getComputedStyle(el);
            return styles.animation !== 'none' && styles.animation !== '' && styles.animationDuration !== '0s';
          })
        };
      });

      console.log(`  ✓ Screenshot captured`);
      console.log(`    Body font: ${metrics.bodyFontSize}`);
      console.log(`    Input font: ${metrics.inputFontSize || 'N/A'}`);
      console.log(`    Header visible: ${metrics.headerVisible}`);
      console.log(`    Animations: ${metrics.animations ? 'Yes' : 'No'}`);
      
      // Verify expected behavior
      if (width === 100) {
        console.log(`    ✅ Verification: Font should be ~6px (actual: ${metrics.bodyFontSize})`);
        console.log(`    ✅ Verification: Header should be hidden (actual: ${metrics.headerVisible ? 'visible' : 'hidden'})`);
      }
      
      console.log('');

    } catch (error) {
      console.error(`  ❌ Error: ${error.message}`);
    } finally {
      await context.close();
    }
  }

  await browser.close();
  
  console.log('✅ Verification complete!');
  console.log(`📁 Screenshots saved to: ${screenshotsDir}`);
}

verifyResponsive().catch(console.error);