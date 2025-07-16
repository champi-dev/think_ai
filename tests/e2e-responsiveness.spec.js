const { test, expect } = require('@playwright/test');

const resolutions = {
  'mobile': { width: 320, height: 480 },
};

test.describe('UI Responsiveness Tests', () => {
  for (const resolutionName in resolutions) {
    const resolution = resolutions[resolutionName];

    test(`should capture screenshot on ${resolutionName} (${resolution.width}x${resolution.height})`, async ({ page }) => {
      await page.setViewportSize(resolution);
      await page.goto('http://localhost:5173');
      await page.screenshot({ path: `tests/screenshots/${resolutionName}.png` });
    });
  }
});
