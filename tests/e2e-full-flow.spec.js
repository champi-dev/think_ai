const { test, expect } = require('@playwright/test');

test.describe('Think AI - Full E2E Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:8080');
    // Wait for app to load
    await page.waitForSelector('.header h1:has-text("🧠 Think AI")');
  });

  test('complete user journey with all features', async ({ page }) => {
    // Verify initial state
    await expect(page.locator('.header h1')).toContainText('🧠 Think AI');
    await expect(page.locator('input[placeholder="Type your message here..."]')).toBeVisible();
    
    // Start conversation
    await page.fill('input[placeholder="Type your message here..."]', 'Hello, Think AI!');
    await page.click('button:has-text("Send")');
    
    // Wait for response
    await expect(page.locator('.message.user').first()).toContainText('Hello, Think AI!');
    await expect(page.locator('.message.assistant').first()).toBeVisible();
    
    // Test code mode
    await page.click('.toggle-switch input[type="checkbox"]');
    await expect(page.locator('.mode-label')).toContainText('💻 Code');
    
    await page.fill('input[placeholder="Type your message here..."]', 'Write a fibonacci function in Python');
    await page.click('button:has-text("Send")');
    
    // Wait for code response
    await expect(page.locator('.message.assistant').last()).toBeVisible();
    await expect(page.locator('.message.assistant').last()).toContainText(/def|fibonacci|return/);
    
    // Test web search
    await page.click('.feature-toggle:has-text("🔍")');
    await expect(page.locator('.feature-toggle:has-text("🔍")')).toHaveClass(/active/);
    
    await page.fill('input[placeholder="Type your message here..."]', 'What are the latest AI developments?');
    await page.click('button:has-text("Send")');
    
    await expect(page.locator('.message.assistant').last()).toBeVisible();
    
    // Test fact checking
    await page.click('.feature-toggle:has-text("✅")');
    await expect(page.locator('.feature-toggle:has-text("✅")')).toHaveClass(/active/);
    
    await page.fill('input[placeholder="Type your message here..."]', 'The Earth is round, correct?');
    await page.click('button:has-text("Send")');
    
    await expect(page.locator('.message.assistant').last()).toBeVisible();
    
    // Test copy functionality
    const copyButton = page.locator('.copy-button').first();
    await copyButton.click();
    await expect(copyButton).toContainText('Copied!');
    await page.waitForTimeout(2000);
    await expect(copyButton).toContainText('Copy');
    
    // Verify session persistence
    const sessionId = await page.evaluate(() => localStorage.getItem('think-ai-session'));
    expect(sessionId).toBeTruthy();
    
    // Reload page and verify session
    await page.reload();
    await page.waitForSelector('.header h1:has-text("🧠 Think AI")');
    
    const newSessionId = await page.evaluate(() => localStorage.getItem('think-ai-session'));
    expect(newSessionId).toBe(sessionId);
  });

  test('handles errors gracefully', async ({ page }) => {
    // Intercept API calls to simulate error
    await page.route('**/api/chat', route => {
      route.fulfill({
        status: 500,
        body: JSON.stringify({ error: 'Internal server error' })
      });
    });
    
    await page.fill('input[placeholder="Type your message here..."]', 'Test error handling');
    await page.click('button:has-text("Send")');
    
    // Should show error message
    await expect(page.locator('.message.assistant').last()).toContainText('Sorry, I encountered an error');
    
    // App should still be functional
    await page.unroute('**/api/chat');
    await page.fill('input[placeholder="Type your message here..."]', 'Test recovery');
    await page.click('button:has-text("Send")');
    
    await expect(page.locator('.message.user').last()).toContainText('Test recovery');
  });

  test('responsive design on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await expect(page.locator('.header h1')).toBeVisible();
    await expect(page.locator('input[placeholder="Type your message here..."]')).toBeVisible();
    
    // Test interaction on mobile
    await page.fill('input[placeholder="Type your message here..."]', 'Mobile test');
    await page.click('button:has-text("Send")');
    
    await expect(page.locator('.message.user').last()).toContainText('Mobile test');
    await expect(page.locator('.message.assistant').last()).toBeVisible();
  });

  test('keyboard navigation and accessibility', async ({ page }) => {
    // Tab through elements
    await page.keyboard.press('Tab'); // Mode toggle
    await expect(page.locator('.toggle-switch input[type="checkbox"]')).toBeFocused();
    
    await page.keyboard.press('Tab'); // Input field
    await expect(page.locator('input[placeholder="Type your message here..."]')).toBeFocused();
    
    // Type and send with Enter
    await page.keyboard.type('Keyboard test');
    await page.keyboard.press('Enter');
    
    await expect(page.locator('.message.user').last()).toContainText('Keyboard test');
    
    // Check ARIA labels
    const input = page.locator('input[placeholder="Type your message here..."]');
    await expect(input).toHaveAttribute('aria-label', 'Message input');
  });

  test('performance - handles rapid messages', async ({ page }) => {
    const messages = ['Message 1', 'Message 2', 'Message 3', 'Message 4', 'Message 5'];
    
    for (const msg of messages) {
      await page.fill('input[placeholder="Type your message here..."]', msg);
      await page.click('button:has-text("Send")');
      // Don't wait for response, send next immediately
    }
    
    // All messages should be queued and processed
    for (const msg of messages) {
      await expect(page.locator(`.message.user:has-text("${msg}")`)).toBeVisible();
    }
    
    // Wait for all responses
    await page.waitForTimeout(3000);
    const assistantMessages = await page.locator('.message.assistant').count();
    expect(assistantMessages).toBeGreaterThanOrEqual(messages.length);
  });

  test('PWA functionality', async ({ page }) => {
    // Check manifest
    const manifestResponse = await page.request.get('/manifest.json');
    expect(manifestResponse.ok()).toBeTruthy();
    const manifest = await manifestResponse.json();
    expect(manifest.name).toBe('Think AI');
    expect(manifest.icons[0].src).toContain('🧠');
    
    // Check service worker registration (if implemented)
    const hasServiceWorker = await page.evaluate(() => 'serviceWorker' in navigator);
    expect(hasServiceWorker).toBeTruthy();
  });

  test('memory and performance with long conversation', async ({ page }) => {
    // Send many messages to test memory handling
    for (let i = 0; i < 20; i++) {
      await page.fill('input[placeholder="Type your message here..."]', `Test message ${i}`);
      await page.click('button:has-text("Send")');
      
      // Wait for response before sending next
      await page.waitForSelector(`.message.assistant:nth-child(${(i + 1) * 2})`);
    }
    
    // Check scrolling behavior
    const messagesContainer = page.locator('.messages-container');
    const isScrolledToBottom = await messagesContainer.evaluate(el => {
      return Math.abs(el.scrollHeight - el.scrollTop - el.clientHeight) < 10;
    });
    expect(isScrolledToBottom).toBeTruthy();
    
    // App should still be responsive
    const startTime = Date.now();
    await page.fill('input[placeholder="Type your message here..."]', 'Final performance test');
    await page.click('button:has-text("Send")');
    await page.waitForSelector('.message.assistant:last-child');
    const endTime = Date.now();
    
    // Response time should be reasonable
    expect(endTime - startTime).toBeLessThan(5000);
  });

  test('dark mode toggle (if implemented)', async ({ page }) => {
    // Check if dark mode exists
    const darkModeToggle = page.locator('[aria-label="Toggle dark mode"]');
    const hasDarkMode = await darkModeToggle.count() > 0;
    
    if (hasDarkMode) {
      await darkModeToggle.click();
      await expect(page.locator('body')).toHaveClass(/dark/);
      
      // Toggle back
      await darkModeToggle.click();
      await expect(page.locator('body')).not.toHaveClass(/dark/);
    }
  });

  test('API health check', async ({ page }) => {
    const response = await page.request.get('/api/health');
    expect(response.ok()).toBeTruthy();
    const health = await response.json();
    expect(health.status).toBe('healthy');
    expect(health.service).toBe('think-ai-full');
  });

  test('handles network delays gracefully', async ({ page }) => {
    // Simulate slow network
    await page.route('**/api/chat', async route => {
      await new Promise(resolve => setTimeout(resolve, 3000));
      route.continue();
    });
    
    await page.fill('input[placeholder="Type your message here..."]', 'Slow network test');
    await page.click('button:has-text("Send")');
    
    // Should show loading state
    await expect(page.locator('.loading-indicator')).toContainText('AI is thinking...');
    await expect(page.locator('button:has-text("Send")')).toBeDisabled();
    await expect(page.locator('input[placeholder="Type your message here..."]')).toBeDisabled();
    
    // Wait for response
    await page.waitForSelector('.message.assistant:last-child', { timeout: 10000 });
    
    // Should recover from loading state
    await expect(page.locator('button:has-text("Send")')).toBeEnabled();
    await expect(page.locator('input[placeholder="Type your message here..."]')).toBeEnabled();
  });
});