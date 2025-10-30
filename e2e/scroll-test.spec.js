import { test, expect } from '@playwright/test';

test.describe('Landing Page Scroll Test', () => {
  test('should allow scrolling and show all elements', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Get page dimensions
    const viewportHeight = page.viewportSize().height;

    // Take screenshot at top
    await page.screenshot({
      path: 'e2e/screenshots/scroll-test-top.png',
      fullPage: false
    });

    // Check if page is scrollable
    const scrollHeight = await page.evaluate(() => document.documentElement.scrollHeight);
    const clientHeight = await page.evaluate(() => document.documentElement.clientHeight);

    console.log(`Viewport height: ${viewportHeight}`);
    console.log(`Scroll height: ${scrollHeight}`);
    console.log(`Client height: ${clientHeight}`);
    console.log(`Is scrollable: ${scrollHeight > clientHeight}`);

    // Take full page screenshot
    await page.screenshot({
      path: 'e2e/screenshots/scroll-test-fullpage.png',
      fullPage: true
    });

    // Scroll to features section
    await page.locator('text=AI-Powered Chat').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await page.screenshot({
      path: 'e2e/screenshots/scroll-test-features.png',
      fullPage: false
    });

    // Scroll to benefits section
    await page.locator('text=What You Get').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await page.screenshot({
      path: 'e2e/screenshots/scroll-test-benefits.png',
      fullPage: false
    });

    // Scroll to footer
    await page.locator('text=Powered by open-source').scrollIntoViewIfNeeded();
    await page.waitForTimeout(500);
    await page.screenshot({
      path: 'e2e/screenshots/scroll-test-footer.png',
      fullPage: false
    });

    // Check all elements are visible (after scrolling to them)
    await expect(page.locator('h1:has-text("Think AI")')).toBeVisible();
    await expect(page.locator('text=AI-Powered Chat')).toBeVisible();
    await expect(page.locator('text=Lightning Fast')).toBeVisible();
    await expect(page.locator('text=Privacy First')).toBeVisible();
    await expect(page.locator('text=What You Get')).toBeVisible();
    await expect(page.locator('text=Multi-user support')).toBeVisible();
    await expect(page.locator('text=Powered by open-source')).toBeVisible();
  });

  test('should measure actual page height', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const metrics = await page.evaluate(() => {
      const body = document.body;
      const html = document.documentElement;

      return {
        scrollHeight: Math.max(
          body.scrollHeight, body.offsetHeight,
          html.clientHeight, html.scrollHeight, html.offsetHeight
        ),
        clientHeight: html.clientHeight,
        viewportHeight: window.innerHeight,
        bodyHeight: body.scrollHeight,
        htmlHeight: html.scrollHeight,
        overflow: window.getComputedStyle(html).overflow,
        overflowY: window.getComputedStyle(html).overflowY,
        bodyOverflow: window.getComputedStyle(body).overflow,
      };
    });

    console.log('Page Metrics:', JSON.stringify(metrics, null, 2));

    // Take annotated screenshot
    await page.screenshot({
      path: 'e2e/screenshots/scroll-test-metrics.png',
      fullPage: true
    });
  });
});
