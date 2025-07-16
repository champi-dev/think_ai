const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PROD_URL = 'https://thinkai.lat';

async function testMessageVisibility() {
  const screenshotsDir = path.join(process.cwd(), 'screenshots', 'prod-message-debug');
  if (!fs.existsSync(screenshotsDir)) {
    fs.mkdirSync(screenshotsDir, { recursive: true });
  }

  const browser = await chromium.launch({ headless: true });

  console.log('🔍 Testing message visibility at production (thinkai.lat)...\n');

  const resolutions = [
    { width: 100, height: 100, name: 'minimum' },
    { width: 150, height: 150, name: 'extreme-micro' },
    { width: 200, height: 300, name: 'micro' },
    { width: 300, height: 400, name: 'tiny' }
  ];

  for (const { width, height, name } of resolutions) {
    console.log(`\n=== Testing ${width}x${height} (${name}) ===`);
    
    const context = await browser.newContext({
      viewport: { width, height },
      deviceScaleFactor: 2
    });

    const page = await context.newPage();
    
    try {
      await page.goto(PROD_URL, { waitUntil: 'networkidle' });
      await page.waitForTimeout(2000);

      // 1. Capture initial state
      await page.screenshot({
        path: path.join(screenshotsDir, `${name}-1-initial.png`),
        fullPage: false
      });

      // 2. Check messages container
      const messagesInfo = await page.evaluate(() => {
        const messagesEl = document.querySelector('.messages');
        if (!messagesEl) return { exists: false };
        
        const rect = messagesEl.getBoundingClientRect();
        const styles = window.getComputedStyle(messagesEl);
        
        return {
          exists: true,
          visible: rect.width > 0 && rect.height > 0,
          dimensions: { width: rect.width, height: rect.height, top: rect.top, left: rect.left },
          styles: {
            display: styles.display,
            visibility: styles.visibility,
            overflow: styles.overflow,
            background: styles.backgroundColor,
            opacity: styles.opacity,
            height: styles.height,
            padding: styles.padding
          },
          childCount: messagesEl.children.length
        };
      });
      
      console.log('Messages container:', messagesInfo);

      // 3. Type and send a message
      const input = await page.$('#queryInput');
      if (input) {
        await input.fill(`Test ${width}x${height}`);
        console.log('✓ Typed message');
        
        await page.screenshot({
          path: path.join(screenshotsDir, `${name}-2-typed.png`),
          fullPage: false
        });

        const sendBtn = await page.$('#sendBtn');
        if (sendBtn) {
          await sendBtn.click();
          console.log('✓ Clicked send');
          
          // 4. Wait for user message to appear
          try {
            await page.waitForSelector('.message.user', { timeout: 5000 });
            console.log('✓ User message appeared');
            
            await page.waitForTimeout(500);
            
            await page.screenshot({
              path: path.join(screenshotsDir, `${name}-3-user-message.png`),
              fullPage: false
            });

            // 5. Analyze user message
            const userMessageInfo = await page.evaluate(() => {
              const msg = document.querySelector('.message.user');
              const msgContent = document.querySelector('.message.user .message-content');
              
              if (!msg || !msgContent) return { exists: false };
              
              const msgRect = msg.getBoundingClientRect();
              const contentRect = msgContent.getBoundingClientRect();
              const msgStyles = window.getComputedStyle(msg);
              const contentStyles = window.getComputedStyle(msgContent);
              
              // Check if message is within viewport
              const inViewport = (
                contentRect.top >= 0 &&
                contentRect.left >= 0 &&
                contentRect.bottom <= window.innerHeight &&
                contentRect.right <= window.innerWidth
              );
              
              return {
                exists: true,
                text: msgContent.textContent,
                message: {
                  dimensions: { width: msgRect.width, height: msgRect.height, top: msgRect.top },
                  styles: {
                    display: msgStyles.display,
                    marginBottom: msgStyles.marginBottom
                  }
                },
                content: {
                  dimensions: { width: contentRect.width, height: contentRect.height, top: contentRect.top },
                  styles: {
                    fontSize: contentStyles.fontSize,
                    color: contentStyles.color,
                    background: contentStyles.backgroundColor,
                    padding: contentStyles.padding,
                    display: contentStyles.display
                  }
                },
                inViewport
              };
            });
            
            console.log('User message info:', userMessageInfo);

            // 6. Wait for AI response
            try {
              await page.waitForSelector('.message.ai', { timeout: 10000 });
              console.log('✓ AI response appeared');
              
              await page.waitForTimeout(500);
              
              await page.screenshot({
                path: path.join(screenshotsDir, `${name}-4-ai-response.png`),
                fullPage: false
              });

              // 7. Check if both messages are visible
              const allMessagesInfo = await page.evaluate(() => {
                const messages = document.querySelectorAll('.message');
                const messagesContainer = document.querySelector('.messages');
                
                return {
                  messageCount: messages.length,
                  containerScrollHeight: messagesContainer?.scrollHeight,
                  containerClientHeight: messagesContainer?.clientHeight,
                  messages: Array.from(messages).map((msg, i) => {
                    const content = msg.querySelector('.message-content');
                    const rect = content?.getBoundingClientRect();
                    return {
                      index: i,
                      type: msg.classList.contains('user') ? 'user' : 'ai',
                      text: content?.textContent?.substring(0, 20) + '...',
                      visible: rect && rect.width > 0 && rect.height > 0,
                      top: rect?.top
                    };
                  })
                };
              });
              
              console.log('All messages info:', allMessagesInfo);

            } catch (e) {
              console.log('✗ No AI response within timeout');
            }

          } catch (e) {
            console.log('✗ User message did not appear');
            
            // Debug why message didn't appear
            const debugInfo = await page.evaluate(() => {
              return {
                inputValue: document.querySelector('#queryInput')?.value,
                sendBtnExists: !!document.querySelector('#sendBtn'),
                messagesExists: !!document.querySelector('.messages'),
                bodyClasses: document.body.className,
                errors: Array.from(document.querySelectorAll('.error')).map(e => e.textContent)
              };
            });
            
            console.log('Debug info:', debugInfo);
          }
        }
      }

    } catch (error) {
      console.error(`❌ Error: ${error.message}`);
    } finally {
      await context.close();
    }
  }

  await browser.close();
  
  console.log('\n✅ E2E test complete!');
  console.log(`📁 Screenshots saved to: ${screenshotsDir}`);
}

testMessageVisibility().catch(console.error);