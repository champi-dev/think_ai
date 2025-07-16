// @ts-check
const { defineConfig, devices } = require('@playwright/test');

/**
 * Read environment variables from file.
 * https://github.com/motdotla/dotenv
 */
// require('dotenv').config();

/**
 * @see https://playwright.dev/docs/test-configuration
 */
module.exports = defineConfig({
  testDir: './tests',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI,
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0,
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined,
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: [
    ['html', { outputFolder: 'test-results/e2e-report' }],
    ['json', { outputFile: 'test-results/e2e-results.json' }],
    ['junit', { outputFile: 'test-results/e2e-junit.xml' }],
    ['list']
  ],
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: process.env.BASE_URL || 'http://localhost:8080',

    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',

    /* Screenshot on failure */
    screenshot: 'only-on-failure',

    /* Video on failure */
    video: 'retain-on-failure',

    /* Maximum time each action can take */
    actionTimeout: 10000,

    /* Viewport */
    viewport: { width: 1280, height: 720 },
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },

    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },

    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },

    /* Test against mobile viewports. */
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },

    /* Test against branded browsers. */
    {
      name: 'Microsoft Edge',
      use: { ...devices['Desktop Edge'], channel: 'msedge' },
    },
    {
      name: 'Google Chrome',
      use: { ...devices['Desktop Chrome'], channel: 'chrome' },
    },
  ],

  /* Run your local dev server before starting the tests */
  webServer: [
    {
      command: 'cd full-system && cargo run --bin think-ai-full-fixed',
      port: 8080,
      timeout: 120 * 1000,
      reuseExistingServer: !process.env.CI,
      stdout: 'pipe',
      stderr: 'pipe',
    }
  ],

  /* Global setup */
  globalSetup: require.resolve('./tests/global-setup.js'),
  
  /* Global teardown */
  globalTeardown: require.resolve('./tests/global-teardown.js'),

  /* Maximum time one test can run for */
  timeout: 30 * 1000,

  /* Maximum time the whole test suite can run */
  globalTimeout: 30 * 60 * 1000, // 30 minutes
});