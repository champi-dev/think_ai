const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const LOCAL_URL = 'http://localhost:8000/?testMode=true';

async function testSmartwatchUI() {
  const screenshotsDir = path.join(process.cwd(), 'screenshots', 'smartwatch-ui');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 300, height: 300 }
  });
  const page = await context.newPage();

  console.log('🔍 Testing Smartwatch UI locally...\n');

  try {
    await page.goto(LOCAL_URL, { waitUntil: 'networkidle' });
    console.log('✓ Navigated to Smartwatch UI');

    await page.screenshot({
      path: path.join(screenshotsDir, '1-initial-load.png'),
      fullPage: true
    });

    const startButton = await page.$('#start-button');
    if (startButton) {
      console.log('✓ Found "Start Listening" button');
      await startButton.click();
      console.log('✓ Clicked "Start Listening" button');

      await page.waitForTimeout(1000); // Wait for potential animation

      await page.screenshot({
        path: path.join(screenshotsDir, '2-after-click.png'),
        fullPage: true
      });

      const buttonText = await page.textContent('#start-button');
      if (buttonText === 'Listening...') {
        console.log('✓ Button text changed to "Listening..."');
      } else {
        console.error('✗ Button text did not change to "Listening..."');
      }

      const listeningIndicator = await page.$('.listening-indicator.listening');
      if (listeningIndicator) {
        console.log('✓ Listening indicator has "listening" class');
      } else {
        console.error('✗ Listening indicator does not have "listening" class');
      }

    } else {
      console.error('✗ Could not find "Start Listening" button');
    }

  } catch (error) {
    console.error(`❌ Error: ${error.message}`);
  } finally {
    await browser.close();
    console.log('\n✅ E2E test complete!');
    console.log(`📁 Screenshots saved to: ${screenshotsDir}`);
  }
}

testSmartwatchUI().catch(console.error);
