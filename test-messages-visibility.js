const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PROD_URL = 'https://thinkai.lat';

async function testMessageVisibility() {
  const screenshotsDir = path.join(process.cwd(), 'screenshots', 'message-test');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });

  console.log('🔍 Testing message visibility at tiny resolutions...\n');

  const resolutions = [
    { width: 100, height: 100, name: 'minimum' },
    { width: 200, height: 300, name: 'micro' }
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

      // Type and send a message
      const input = await page.$('#queryInput');
      if (input) {
        await input.fill(`Test ${width}x${height}`);
        await page.screenshot({
          path: path.join(screenshotsDir, `${name}-1-typed.png`),
          fullPage: false
        });

        const sendBtn = await page.$('#sendBtn');
        if (sendBtn) {
          await sendBtn.click();
          
          // Wait for user message
          await page.waitForSelector('.message.user', { timeout: 5000 });
          await page.waitForTimeout(1000);
          
          await page.screenshot({
            path: path.join(screenshotsDir, `${name}-2-sent.png`),
            fullPage: false
          });

          // Check message visibility
          const messageVisible = await page.evaluate(() => {
            const userMsg = document.querySelector('.message.user .message-content');
            if (!userMsg) return { visible: false };
            
            const rect = userMsg.getBoundingClientRect();
            const styles = window.getComputedStyle(userMsg);
            
            return {
              visible: rect.width > 0 && rect.height > 0,
              text: userMsg.textContent,
              fontSize: styles.fontSize,
              color: styles.color,
              background: styles.backgroundColor,
              position: { x: rect.x, y: rect.y, width: rect.width, height: rect.height }
            };
          });

          console.log(`  Message visibility:`, messageVisible);

          // Wait for AI response
          try {
            await page.waitForSelector('.message.ai', { timeout: 10000 });
            await page.waitForTimeout(1000);
            
            await page.screenshot({
              path: path.join(screenshotsDir, `${name}-3-response.png`),
              fullPage: false
            });

            const aiMessageVisible = await page.evaluate(() => {
              const aiMsg = document.querySelector('.message.ai .message-content');
              if (!aiMsg) return { visible: false };
              
              const rect = aiMsg.getBoundingClientRect();
              const styles = window.getComputedStyle(aiMsg);
              
              return {
                visible: rect.width > 0 && rect.height > 0,
                fontSize: styles.fontSize,
                color: styles.color,
                background: styles.backgroundColor
              };
            });

            console.log(`  AI message visibility:`, aiMessageVisible);
          } catch (e) {
            console.log(`  No AI response received`);
          }
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
  
  console.log('✅ Message visibility test complete!');
  console.log(`📁 Screenshots saved to: ${screenshotsDir}`);
}

testMessageVisibility().catch(console.error);