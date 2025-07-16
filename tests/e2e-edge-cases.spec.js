const { test, expect } = require('@playwright/test');

test.describe('Think AI - Edge Cases E2E', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8080');
    await page.waitForSelector('.header h1:has-text("🧠 Think AI")');
  });

  test('handles extremely long messages', async ({ page }) => {
    const longMessage = 'This is a very long message that tests the system limits. '.repeat(100);
    
    await page.fill('input[placeholder="Type your message here..."]', longMessage);
    await page.click('button:has-text("Send")');
    
    // Should handle long message
    await expect(page.locator('.message.user').last()).toBeVisible();
    await expect(page.locator('.message.assistant').last()).toBeVisible();
  });

  test('handles special characters and emojis', async ({ page }) => {
    const specialMessage = '🤖 Hello! Can you handle "quotes", <tags>, & symbols? 你好 مرحبا';
    
    await page.fill('input[placeholder="Type your message here..."]', specialMessage);
    await page.click('button:has-text("Send")');
    
    await expect(page.locator('.message.user').last()).toContainText(specialMessage);
    await expect(page.locator('.message.assistant').last()).toBeVisible();
  });

  test('handles rapid toggle switching', async ({ page }) => {
    const modeToggle = page.locator('.toggle-switch input[type="checkbox"]');
    const searchToggle = page.locator('.feature-toggle:has-text("🔍")');
    const factToggle = page.locator('.feature-toggle:has-text("✅")');
    
    // Rapidly toggle all features
    for (let i = 0; i < 10; i++) {
      await modeToggle.click();
      await searchToggle.click();
      await factToggle.click();
    }
    
    // App should still be functional
    await page.fill('input[placeholder="Type your message here..."]', 'Test after rapid toggling');
    await page.click('button:has-text("Send")');
    
    await expect(page.locator('.message.assistant').last()).toBeVisible();
  });

  test('handles browser back/forward navigation', async ({ page }) => {
    // Send a message
    await page.fill('input[placeholder="Type your message here..."]', 'First message');
    await page.click('button:has-text("Send")');
    await page.waitForSelector('.message.assistant');
    
    // Navigate away and back
    await page.goto('about:blank');
    await page.goBack();
    
    // Session should be preserved
    await page.waitForSelector('.header h1:has-text("🧠 Think AI")');
    const sessionId = await page.evaluate(() => localStorage.getItem('think-ai-session'));
    expect(sessionId).toBeTruthy();
  });

  test('handles multiple browser tabs', async ({ browser }) => {
    const context = await browser.newContext();
    const page1 = await context.newPage();
    const page2 = await context.newPage();
    
    // Load app in both tabs
    await page1.goto('http://localhost:8080');
    await page2.goto('http://localhost:8080');
    
    // Send message in first tab
    await page1.fill('input[placeholder="Type your message here..."]', 'Message from tab 1');
    await page1.click('button:has-text("Send")');
    await page1.waitForSelector('.message.assistant');
    
    // Send message in second tab
    await page2.fill('input[placeholder="Type your message here..."]', 'Message from tab 2');
    await page2.click('button:has-text("Send")');
    await page2.waitForSelector('.message.assistant');
    
    // Both tabs should work independently
    const session1 = await page1.evaluate(() => localStorage.getItem('think-ai-session'));
    const session2 = await page2.evaluate(() => localStorage.getItem('think-ai-session'));
    
    // Sessions might be the same if using localStorage
    expect(session1).toBeTruthy();
    expect(session2).toBeTruthy();
    
    await context.close();
  });

  test('handles offline/online transitions', async ({ page, context }) => {
    // Send initial message
    await page.fill('input[placeholder="Type your message here..."]', 'Online message');
    await page.click('button:has-text("Send")');
    await page.waitForSelector('.message.assistant');
    
    // Go offline
    await context.setOffline(true);
    
    // Try to send message while offline
    await page.fill('input[placeholder="Type your message here..."]', 'Offline message');
    await page.click('button:has-text("Send")');
    
    // Should show error
    await expect(page.locator('.message.assistant').last()).toContainText(/error|failed|try again/i);
    
    // Go back online
    await context.setOffline(false);
    
    // Should work again
    await page.fill('input[placeholder="Type your message here..."]', 'Back online');
    await page.click('button:has-text("Send")');
    await page.waitForSelector('.message.assistant:last-child:not(:has-text("error"))');
  });

  test('handles localStorage quota exceeded', async ({ page }) => {
    // Fill localStorage near quota
    await page.evaluate(() => {
      try {
        const bigData = 'x'.repeat(1024 * 1024); // 1MB string
        for (let i = 0; i < 5; i++) {
          localStorage.setItem(`test-data-${i}`, bigData);
        }
      } catch (e) {
        // Quota might be exceeded, which is what we're testing
      }
    });
    
    // App should still function
    await page.fill('input[placeholder="Type your message here..."]', 'Test with full storage');
    await page.click('button:has-text("Send")');
    
    await expect(page.locator('.message.assistant').last()).toBeVisible();
    
    // Clean up
    await page.evaluate(() => {
      for (let i = 0; i < 5; i++) {
        localStorage.removeItem(`test-data-${i}`);
      }
    });
  });

  test('handles XSS attempts', async ({ page }) => {
    const xssAttempts = [
      '<script>alert("XSS")</script>',
      '<img src=x onerror="alert(\'XSS\')">',
      'javascript:alert("XSS")',
      '<iframe src="javascript:alert(\'XSS\')"></iframe>'
    ];
    
    for (const xss of xssAttempts) {
      await page.fill('input[placeholder="Type your message here..."]', xss);
      await page.click('button:has-text("Send")');
      
      // Check that script is not executed
      const alertFired = await page.evaluate(() => {
        let alertCalled = false;
        const originalAlert = window.alert;
        window.alert = () => { alertCalled = true; };
        setTimeout(() => { window.alert = originalAlert; }, 100);
        return new Promise(resolve => setTimeout(() => resolve(alertCalled), 200));
      });
      
      expect(alertFired).toBe(false);
      
      // Message should be displayed as text, not executed
      await expect(page.locator('.message.user').last()).toContainText(xss);
    }
  });

  test('handles session timeout/expiry', async ({ page }) => {
    // Send message
    await page.fill('input[placeholder="Type your message here..."]', 'Initial message');
    await page.click('button:has-text("Send")');
    await page.waitForSelector('.message.assistant');
    
    // Simulate expired session by clearing it
    await page.evaluate(() => {
      localStorage.removeItem('think-ai-session');
    });
    
    // Send another message
    await page.fill('input[placeholder="Type your message here..."]', 'Message after session clear');
    await page.click('button:has-text("Send")');
    
    // Should create new session and work normally
    await expect(page.locator('.message.assistant').last()).toBeVisible();
    
    const newSession = await page.evaluate(() => localStorage.getItem('think-ai-session'));
    expect(newSession).toBeTruthy();
  });

  test('handles clipboard errors gracefully', async ({ page, context }) => {
    // Deny clipboard permissions
    await context.clearPermissions();
    
    // Send a message
    await page.fill('input[placeholder="Type your message here..."]', 'Test message');
    await page.click('button:has-text("Send")');
    await page.waitForSelector('.message.assistant');
    
    // Try to copy
    const copyButton = page.locator('.copy-button').first();
    await copyButton.click();
    
    // Should handle gracefully (might show error or fallback)
    await page.waitForTimeout(500);
    
    // App should still be functional
    await page.fill('input[placeholder="Type your message here..."]', 'Test after clipboard error');
    await page.click('button:has-text("Send")');
    await expect(page.locator('.message.assistant').last()).toBeVisible();
  });

  test('handles memory pressure', async ({ page }) => {
    // Send many messages with large content
    for (let i = 0; i < 50; i++) {
      const largeMessage = `Message ${i}: ${'x'.repeat(1000)}`;
      await page.fill('input[placeholder="Type your message here..."]', largeMessage);
      await page.click('button:has-text("Send")');
      
      // Don't wait for all responses to accumulate
      if (i % 10 === 0) {
        await page.waitForTimeout(100);
      }
    }
    
    // Check if app is still responsive
    await page.fill('input[placeholder="Type your message here..."]', 'Final test');
    await page.click('button:has-text("Send")');
    
    // Should eventually show response
    await expect(page.locator('.message.user:has-text("Final test")')).toBeVisible({ timeout: 10000 });
  });

  test('handles concurrent API failures', async ({ page }) => {
    let failureCount = 0;
    
    // Intercept to fail every other request
    await page.route('**/api/chat', route => {
      failureCount++;
      if (failureCount % 2 === 0) {
        route.fulfill({ status: 500, body: JSON.stringify({ error: 'Server error' }) });
      } else {
        route.continue();
      }
    });
    
    // Send multiple messages
    const messages = ['Test 1', 'Test 2', 'Test 3', 'Test 4'];
    for (const msg of messages) {
      await page.fill('input[placeholder="Type your message here..."]', msg);
      await page.click('button:has-text("Send")');
      await page.waitForTimeout(500);
    }
    
    // Some should succeed, some should fail
    const userMessages = await page.locator('.message.user').count();
    expect(userMessages).toBe(messages.length);
    
    const errorMessages = await page.locator('.message.assistant:has-text("error")').count();
    expect(errorMessages).toBeGreaterThan(0);
    expect(errorMessages).toBeLessThan(messages.length);
  });
});