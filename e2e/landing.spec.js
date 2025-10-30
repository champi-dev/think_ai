import { test, expect } from '@playwright/test';

test.describe('Landing Page', () => {
  test('should display landing page when not authenticated', async ({ page }) => {
    await page.goto('/');

    // Wait for page to load
    await page.waitForLoadState('networkidle');

    // Check page title
    await expect(page.locator('h1')).toContainText('Think AI');

    // Check subtitle
    await expect(page.locator('text=Your Personal AI Assistant')).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/landing-page.png',
      fullPage: true
    });
  });

  test('should have Get Started and Sign In buttons', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check buttons exist
    const getStartedButton = page.locator('text=Get Started Free');
    const signInButton = page.locator('text=Sign In').nth(0);

    await expect(getStartedButton).toBeVisible();
    await expect(signInButton).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/landing-buttons.png'
    });
  });

  test('should display feature cards', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check feature cards
    await expect(page.locator('text=Open-Source AI')).toBeVisible();
    await expect(page.locator('text=Lightning Fast')).toBeVisible();
    await expect(page.locator('text=Privacy First')).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/landing-features.png'
    });
  });

  test('should display benefits section', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Scroll to benefits
    await page.locator('text=What You Get').scrollIntoViewIfNeeded();

    // Check benefits
    await expect(page.locator('text=Multi-user support')).toBeVisible();
    await expect(page.locator('text=Beautiful, modern UI')).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/landing-benefits.png',
      fullPage: true
    });
  });

  test('should navigate to register page when clicking Get Started', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await page.locator('text=Get Started Free').click();

    // Should navigate to register page
    await expect(page).toHaveURL('/register');

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/navigate-to-register.png'
    });
  });

  test('should navigate to login page when clicking Sign In', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await page.locator('text=Sign In').nth(0).click();

    // Should navigate to login page
    await expect(page).toHaveURL('/login');

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/navigate-to-login.png'
    });
  });

  test('should have footer with tech stack info', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Scroll to footer
    await page.locator('text=Powered by open-source').scrollIntoViewIfNeeded();

    await expect(page.locator('text=Powered by Qwen3')).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/landing-footer.png'
    });
  });
});
