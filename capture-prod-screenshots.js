const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PROD_URL = 'https://thinkai.lat';

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
  const screenshotsDir = path.join(process.cwd(), 'screenshots', 'production');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  const browser = await chromium.launch({
    headless: true
  });

  console.log('📸 Capturing screenshots from production site...\n');

  for (const { width, height, name } of RESOLUTIONS) {
    console.log(`Testing ${width}x${height} (${name})...`);
    
    const context = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor: 2, // High quality screenshots
      isMobile: width <= 480
    });

    const page = await context.newPage();
    
    try {
      // Navigate to production site
      await page.goto(PROD_URL, { 
        waitUntil: 'networkidle',
        timeout: 30000 
      });

      // Wait a bit for any animations to complete
      await page.waitForTimeout(2000);

      // Capture initial state
      await page.screenshot({
        path: path.join(screenshotsDir, `${name}-${width}x${height}-initial.png`),
        fullPage: false
      });

      // Try to interact with the chat
      const input = await page.$('#queryInput');
      if (input) {
        // Type a test message
        await input.fill(`Test at ${width}x${height}`);
        
        await page.screenshot({
          path: path.join(screenshotsDir, `${name}-${width}x${height}-typed.png`),
          fullPage: false
        });

        // Find and click send button
        const sendBtn = await page.$('#sendBtn');
        if (sendBtn) {
          await sendBtn.click();
          
          // Wait for user message to appear
          try {
            await page.waitForSelector('.message.user', { timeout: 5000 });
            await page.waitForTimeout(1000);
            
            await page.screenshot({
              path: path.join(screenshotsDir, `${name}-${width}x${height}-sent.png`),
              fullPage: false
            });

            // Wait for AI response
            try {
              await page.waitForSelector('.message.ai', { timeout: 10000 });
              await page.waitForTimeout(1000);
              
              await page.screenshot({
                path: path.join(screenshotsDir, `${name}-${width}x${height}-response.png`),
                fullPage: false
              });
            } catch (e) {
              console.log(`  ⚠️  No AI response received at ${width}x${height}`);
            }
          } catch (e) {
            console.log(`  ⚠️  Message not sent properly at ${width}x${height}`);
          }
        }
      }

      // Capture some metrics
      const metrics = await page.evaluate(() => {
        const body = document.body;
        const bodyStyles = window.getComputedStyle(body);
        const input = document.querySelector('#queryInput');
        const inputStyles = input ? window.getComputedStyle(input) : null;
        const messageContent = document.querySelector('.message-content');
        const messageStyles = messageContent ? window.getComputedStyle(messageContent) : null;
        
        return {
          bodyFontSize: bodyStyles.fontSize,
          inputFontSize: inputStyles?.fontSize,
          messageFontSize: messageStyles?.fontSize,
          headerVisible: !!document.querySelector('.header')?.offsetParent,
          inputVisible: !!input?.offsetParent,
          animations: Array.from(document.querySelectorAll('*')).some(el => {
            const styles = window.getComputedStyle(el);
            return styles.animation !== 'none' && styles.animation !== '';
          })
        };
      });

      console.log(`  ✓ Captured screenshots`);
      console.log(`    Body font: ${metrics.bodyFontSize}`);
      console.log(`    Input font: ${metrics.inputFontSize || 'N/A'}`);
      console.log(`    Message font: ${metrics.messageFontSize || 'N/A'}`);
      console.log(`    Header visible: ${metrics.headerVisible}`);
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