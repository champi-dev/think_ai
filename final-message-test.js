const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PROD_URL = 'https://thinkai.lat';

async function finalMessageTest() {
  const screenshotsDir = path.join(process.cwd(), 'screenshots', 'final-test');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });

  console.log('🎯 Final message visibility test at production...\n');

  const resolutions = [
    { width: 100, height: 100, name: 'minimum' },
    { width: 150, height: 150, name: 'extreme-micro' },
    { width: 200, height: 300, name: 'micro' },
    { width: 300, height: 400, name: 'tiny' },
    { width: 400, height: 600, name: 'ultra-small' }
  ];

  for (const { width, height, name } of resolutions) {
    console.log(`Testing ${width}x${height} (${name})...`);
    
    const context = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor: 2
    });

    const page = await context.newPage();
    
    try {
      await page.goto(PROD_URL, { waitUntil: 'networkidle' });
      await page.waitForTimeout(2000);

      // Initial screenshot
      await page.screenshot({
        path: path.join(screenshotsDir, `${name}-1-initial.png`),
        fullPage: false
      });

      // Type and send message
      const input = await page.$('#queryInput');
      if (input) {
        await input.fill(`Hi ${width}x${height}`);
        
        // For 100x100, we need to handle the send button differently
        if (width === 100) {
          // Press Enter instead of clicking button
          await input.press('Enter');
        } else {
          const sendBtn = await page.$('#sendBtn');
          if (sendBtn) {
            await sendBtn.click();
          }
        }

        // Wait for user message
        try {
          await page.waitForSelector('.message.user', { timeout: 5000 });
          await page.waitForTimeout(1000);
          
          await page.screenshot({
            path: path.join(screenshotsDir, `${name}-2-with-user-msg.png`),
            fullPage: false
          });

          // Get message styles
          const messageInfo = await page.evaluate(() => {
            const userMsg = document.querySelector('.message.user .message-content');
            if (!userMsg) return null;
            
            const styles = window.getComputedStyle(userMsg);
            const rect = userMsg.getBoundingClientRect();
            
            return {
              text: userMsg.textContent,
              fontSize: styles.fontSize,
              color: styles.color,
              background: styles.backgroundColor,
              visible: rect.width > 0 && rect.height > 0,
              position: { top: rect.top, left: rect.left }
            };
          });
          
          console.log(`  ✓ User message:`, messageInfo);

          // Wait for AI response
          try {
            await page.waitForSelector('.message.ai', { timeout: 10000 });
            await page.waitForTimeout(2000);
            
            await page.screenshot({
              path: path.join(screenshotsDir, `${name}-3-with-ai-response.png`),
              fullPage: false
            });
            
            console.log(`  ✓ AI response received`);
          } catch (e) {
            console.log(`  ⚠ No AI response`);
          }

        } catch (e) {
          console.log(`  ❌ Failed to send message`);
        }
      }

    } catch (error) {
      console.error(`  ❌ Error: ${error.message}`);
    } finally {
      await context.close();
    }
    
    console.log('');
  }

  await browser.close();
  
  console.log('✅ Final test complete!');
  console.log(`📁 Screenshots saved to: ${screenshotsDir}`);
}

finalMessageTest().catch(console.error);