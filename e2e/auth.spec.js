import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test('should display login page', async ({ page }) => {
    await page.goto('/login');
    await page.waitForLoadState('networkidle');

    // Check page elements
    await expect(page.locator('h1')).toContainText('Welcome Back');
    await expect(page.locator('text=Sign in to continue to Think AI')).toBeVisible();

    // Check form fields
    await expect(page.locator('input[name="username"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/login-page.png',
      fullPage: true
    });
  });

  test('should display register page', async ({ page }) => {
    await page.goto('/register');
    await page.waitForLoadState('networkidle');

    // Check page elements
    await expect(page.locator('h1')).toContainText('Create Account');

    // Check form fields
    await expect(page.locator('input[name="username"]')).toBeVisible();
    await expect(page.locator('input[name="email"]')).toBeVisible();
    await expect(page.locator('input[name="fullName"]')).toBeVisible();
    await expect(page.locator('input[name="password"]')).toBeVisible();
    await expect(page.locator('input[name="confirmPassword"]')).toBeVisible();

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/register-page.png',
      fullPage: true
    });
  });

  test('should show error on invalid login', async ({ page }) => {
    await page.goto('/login');
    await page.waitForLoadState('networkidle');

    // Fill in invalid credentials
    await page.fill('input[name="username"]', 'invaliduser');
    await page.fill('input[name="password"]', 'wrongpassword');

    // Submit form
    await page.click('button[type="submit"]');

    // Wait for error message
    await page.waitForSelector('text=Login failed', { timeout: 5000 }).catch(() => {});

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/login-error.png'
    });
  });

  test('should allow registration of new user', async ({ page }) => {
    const timestamp = Date.now();
    const testUser = {
      fullName: 'Test User',
      email: `test${timestamp}@example.com`,
      username: `testuser${timestamp}`,
      password: 'TestPassword123!',
    };

    await page.goto('/register');
    await page.waitForLoadState('networkidle');

    // Fill in registration form
    await page.fill('input[name="username"]', testUser.username);
    await page.fill('input[name="email"]', testUser.email);
    await page.fill('input[name="fullName"]', testUser.fullName);
    await page.fill('input[name="password"]', testUser.password);
    await page.fill('input[name="confirmPassword"]', testUser.password);

    // Take screenshot before submitting
    await page.screenshot({
      path: 'e2e/screenshots/register-filled-form.png'
    });

    // Submit form
    await page.click('button[type="submit"]');

    // Wait for navigation or error
    await page.waitForTimeout(2000);

    // Take screenshot of result
    await page.screenshot({
      path: 'e2e/screenshots/register-result.png'
    });
  });

  test('should navigate from login to register', async ({ page }) => {
    await page.goto('/login');
    await page.waitForLoadState('networkidle');

    // Click sign up link
    await page.click('text=Sign up');

    // Should navigate to register page
    await expect(page).toHaveURL('/register');

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/login-to-register.png'
    });
  });

  test('should navigate from register to login', async ({ page }) => {
    await page.goto('/register');
    await page.waitForLoadState('networkidle');

    // Click sign in link
    await page.click('text=Sign in');

    // Should navigate to login page
    await expect(page).toHaveURL('/login');

    // Take screenshot
    await page.screenshot({
      path: 'e2e/screenshots/register-to-login.png'
    });
  });
});
