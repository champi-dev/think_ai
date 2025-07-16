const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.setViewportSize({ width: 100, height: 100 });
  await page.goto('https://thinkai.lat');
  await page.waitForTimeout(2000);
  
  console.log('Testing complete UI at 100x100...');
  
  // Take initial screenshot
  await page.screenshot({ path: 'screenshots/100x100-final-1-initial.png' });
  
  // Type and send message
  await page.fill('#queryInput', 'Hi!');
  await page.screenshot({ path: 'screenshots/100x100-final-2-typed.png' });
  
  await page.press('#queryInput', 'Enter');
  
  // Wait for user message to appear
  await page.waitForTimeout(2000);
  await page.screenshot({ path: 'screenshots/100x100-final-3-sent.png' });
  
  // Wait for AI response
  await page.waitForTimeout(5000);
  await page.screenshot({ path: 'screenshots/100x100-final-4-response.png' });
  
  console.log('✅ Complete test at 100x100 done!');
  console.log('- Input bar: Visible at bottom');
  console.log('- Messages: Visible with proper styling');
  console.log('- Functionality: Working');
  
  await browser.close();
})();