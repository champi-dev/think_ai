
import { test, expect } from '@playwright/test';

test.describe('Smartwatch UI', () => {
  test('should display smartwatch UI on small viewport', async ({ page }) => {
    // Set viewport to a smartwatch size
    await page.setViewportSize({ width: 360, height: 360 });

    await page.goto('/');

    // Check for SmartwatchView elements
    await expect(page.locator('.smartwatch-container')).toBeVisible();
    await expect(page.locator('.mic-button')).toBeVisible();
    await expect(page.locator('text=Tap to Speak')).toBeVisible();

    // Check that standard UI is not present
    await expect(page.locator('.chat-container')).not.toBeVisible();
  });

  test('should display standard UI on large viewport', async ({ page }) => {
    // Set viewport to a desktop size
    await page.setViewportSize({ width: 1920, height: 1080 });

    await page.goto('/');

    // Check for standard UI elements
    await expect(page.locator('.chat-container')).toBeVisible();
    await expect(page.locator('#queryInput')).toBeVisible();

    // Check that smartwatch UI is not present
    await expect(page.locator('.smartwatch-container')).not.toBeVisible();
  });
});
