import { test, expect } from '@playwright/test';

// Test various tiny resolutions
const TINY_RESOLUTIONS = [
  { width: 400, height: 600, name: 'ultra-small' },
  { width: 320, height: 480, name: 'iphone-se' },
  { width: 300, height: 400, name: 'tiny' },
  { width: 200, height: 300, name: 'micro' },
  { width: 150, height: 150, name: 'extreme-micro' },
  { width: 100, height: 100, name: 'minimum' }
];

test.describe('Tiny Resolution Responsive Design Tests', () => {
  // Test local development site
  const TEST_URL = 'http://localhost:5173';
  
  TINY_RESOLUTIONS.forEach(({ width, height, name }) => {
    test(`should render properly at ${width}x${height} (${name})`, async ({ browser }) => {
      // Create a new context with specific viewport
      const context = await browser.newContext({
        viewport: { width, height },
        deviceScaleFactor: 1,
        isMobile: width <= 480
      });
      
      const page = await context.newPage();
      
      // Navigate to production site
      await page.goto(TEST_URL, { waitUntil: 'networkidle' });
      
      // Take screenshot
      await page.screenshot({
        path: `screenshots/test-${name}-${width}x${height}.png`,
        fullPage: false
      });
      
      // Basic visibility checks based on resolution
      if (width > 200) {
        // Header should be visible for resolutions > 200px
        const header = await page.$('.header');
        expect(header).toBeTruthy();
      } else if (width <= 150) {
        // Header should be hidden for extreme small resolutions
        const header = await page.$('.header');
        const isVisible = header ? await header.isVisible() : false;
        expect(isVisible).toBeFalsy();
      }
      
      // Chat interface should always be visible
      const chatInterface = await page.$('.interface');
      expect(chatInterface).toBeTruthy();
      
      // Input area should be visible and functional
      const input = await page.$('#queryInput');
      expect(input).toBeTruthy();
      
      // Send button should be visible
      const sendBtn = await page.$('#sendBtn');
      expect(sendBtn).toBeTruthy();
      
      // Test basic interaction at each resolution
      if (input && sendBtn) {
        // Type a message
        await input.fill('Test at ' + width + 'x' + height);
        
        // Take screenshot with filled input
        await page.screenshot({
          path: `screenshots/test-${name}-${width}x${height}-typed.png`,
          fullPage: false
        });
        
        // Click send button
        await sendBtn.click();
        
        // Wait for response (with timeout for small resolutions)
        try {
          await page.waitForSelector('.message.user', { timeout: 5000 });
          
          // Take screenshot with message
          await page.screenshot({
            path: `screenshots/test-${name}-${width}x${height}-sent.png`,
            fullPage: false
          });
        } catch (e) {
          console.log(`Timeout waiting for message at ${width}x${height}`);
        }
      }
      
      // Check font sizes are appropriate
      const bodyStyles = await page.evaluate(() => {
        const body = document.body;
        return window.getComputedStyle(body).fontSize;
      });
      
      if (width <= 100) {
        expect(parseInt(bodyStyles)).toBeLessThanOrEqual(10);
      }
      
      // Check that animations are disabled for small resolutions
      if (width < 400) {
        const hasAnimations = await page.evaluate(() => {
          const elements = document.querySelectorAll('*');
          for (let el of elements) {
            const styles = window.getComputedStyle(el);
            if (styles.animation !== 'none' && styles.animation !== '') {
              return true;
            }
          }
          return false;
        });
        expect(hasAnimations).toBeFalsy();
      }
      
      await context.close();
    });
  });
  
  // Test specific UI elements at different breakpoints
  test('UI elements visibility at breakpoints', async ({ browser }) => {
    const breakpointTests = [
      {
        width: 400,
        height: 600,
        expectations: {
          logoText: false,
          modeToggle: true,
          featureToggles: true,
          header: true
        }
      },
      {
        width: 200,
        height: 300,
        expectations: {
          logoText: false,
          modeToggle: true,
          featureToggles: false,
          header: true
        }
      },
      {
        width: 100,
        height: 100,
        expectations: {
          logoText: false,
          modeToggle: false,
          featureToggles: false,
          header: false
        }
      }
    ];
    
    for (const test of breakpointTests) {
      const context = await browser.newContext({
        viewport: { width: test.width, height: test.height }
      });
      
      const page = await context.newPage();
      await page.goto(TEST_URL, { waitUntil: 'networkidle' });
      
      // Check logo text
      const logoText = await page.$('.logo span');
      const logoTextVisible = logoText ? await logoText.isVisible() : false;
      expect(logoTextVisible).toBe(test.expectations.logoText);
      
      // Check mode toggle
      const modeToggle = await page.$('.mode-toggle');
      const modeToggleVisible = modeToggle ? await modeToggle.isVisible() : false;
      expect(modeToggleVisible).toBe(test.expectations.modeToggle);
      
      // Check feature toggles
      const featureToggles = await page.$('.input-features');
      const featureTogglesVisible = featureToggles ? await featureToggles.isVisible() : false;
      expect(featureTogglesVisible).toBe(test.expectations.featureToggles);
      
      // Check header
      const header = await page.$('.header');
      const headerVisible = header ? await header.isVisible() : false;
      expect(headerVisible).toBe(test.expectations.header);
      
      await context.close();
    }
  });
  
  // Test text readability
  test('text remains readable at tiny resolutions', async ({ browser }) => {
    for (const { width, height, name } of TINY_RESOLUTIONS) {
      const context = await browser.newContext({
        viewport: { width, height }
      });
      
      const page = await context.newPage();
      await page.goto(TEST_URL, { waitUntil: 'networkidle' });
      
      // Get computed styles for message content
      const messageStyles = await page.evaluate(() => {
        // Create a temporary message element to test styles
        const tempMsg = document.createElement('div');
        tempMsg.className = 'message-content';
        document.body.appendChild(tempMsg);
        const styles = window.getComputedStyle(tempMsg);
        const fontSize = styles.fontSize;
        const lineHeight = styles.lineHeight;
        document.body.removeChild(tempMsg);
        return { fontSize, lineHeight };
      });
      
      const fontSizePx = parseInt(messageStyles.fontSize);
      
      // Ensure font sizes are appropriate for resolution
      if (width <= 100) {
        expect(fontSizePx).toBeLessThanOrEqual(6);
      } else if (width <= 200) {
        expect(fontSizePx).toBeLessThanOrEqual(10);
      } else if (width <= 300) {
        expect(fontSizePx).toBeLessThanOrEqual(12);
      }
      
      await context.close();
    }
  });
  
  // Test interaction at minimum resolution
  test('interaction works at 100x100 resolution', async ({ browser }) => {
    const context = await browser.newContext({
      viewport: { width: 100, height: 100 }
    });
    
    const page = await context.newPage();
    await page.goto(TEST_URL, { waitUntil: 'networkidle' });
    
    // Find input and send button
    const input = await page.$('#queryInput');
    const sendBtn = await page.$('#sendBtn');
    
    expect(input).toBeTruthy();
    expect(sendBtn).toBeTruthy();
    
    // Input should be typeable
    await input.fill('Hi');
    
    // Get input value
    const inputValue = await input.inputValue();
    expect(inputValue).toBe('Hi');
    
    // Button should be clickable
    const isClickable = await sendBtn.isEnabled();
    expect(isClickable).toBeTruthy();
    
    // Take final screenshot
    await page.screenshot({
      path: 'screenshots/test-100x100-interaction.png'
    });
    
    await context.close();
  });
});