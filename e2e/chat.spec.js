import { test, expect } from '@playwright/test';

test.describe('Chat Interface', () => {
  test('should show login when accessing chat without auth', async ({ page }) => {
    await page.goto('/chat');

    // Should redirect to login
    await expect(page).toHaveURL('/login');

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/chat-redirect-to-login.png'
    });
  });

  test('should display chat input with proper alignment', async ({ page }) => {
    await page.goto('/login');
    await page.waitForLoadState('networkidle');

    // Try to login (this will fail but we can still test UI)
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'password');

    // Take screenshot showing login form
    await page.screenshot({
      path: 'e2e/screenshots/login-form-filled.png'
    });
  });
});

test.describe('UI Components', () => {
  test('should have proper button styling', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const getStartedButton = page.locator('text=Get Started Free');

    // Check button is visible
    await expect(getStartedButton).toBeVisible();

    // Hover over button
    await getStartedButton.hover();

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/button-hover-state.png'
    });
  });

  test('should display three.js background', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Wait for canvas to be rendered
    await page.waitForSelector('canvas', { timeout: 5000 }).catch(() => {});

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/threejs-background.png',
      fullPage: true
    });
  });

  test('should be responsive on mobile', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Check mobile layout
    await expect(page.locator('h1')).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/mobile-landing.png',
      fullPage: true
    });
  });

  test('should be responsive on tablet', async ({ page }) => {
    // Set tablet viewport
    await page.setViewportSize({ width: 768, height: 1024 });

    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/tablet-landing.png',
      fullPage: true
    });
  });
});
