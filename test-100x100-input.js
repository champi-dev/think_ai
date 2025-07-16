const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.setViewportSize({ width: 100, height: 100 });
  await page.goto('https://thinkai.lat');
  await page.waitForTimeout(3000);
  
  // Take initial screenshot
  await page.screenshot({ path: 'screenshots/100x100-input-test-1.png' });
  
  // Check input visibility
  const input = await page.$('#queryInput');
  if (input) {
    const box = await input.boundingBox();
    console.log('Input box:', box);
    
    // Try to type
    await input.fill('Test');
    await page.screenshot({ path: 'screenshots/100x100-input-test-2.png' });
    
    // Check send button
    const sendBtn = await page.$('#sendBtn');
    if (sendBtn) {
      const btnBox = await sendBtn.boundingBox();
      console.log('Send button box:', btnBox);
    }
  } else {
    console.log('Input not found!');
  }
  
  // Check input container
  const container = await page.$('.input-container');
  if (container) {
    const containerBox = await container.boundingBox();
    console.log('Input container box:', containerBox);
  }
  
  await browser.close();
})();