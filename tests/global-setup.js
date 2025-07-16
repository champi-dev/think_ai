// Global setup for e2e tests
const { chromium } = require('@playwright/test');

async function globalSetup(config) {
  console.log('🚀 Starting global e2e test setup...');
  
  // You can perform any setup needed before all tests
  // For example, seed database, setup test accounts, etc.
  
  // Create a browser instance to check if the app is ready
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    // Wait for the app to be ready
    const maxRetries = 30;
    let retries = 0;
    let appReady = false;
    
    while (retries < maxRetries && !appReady) {
      try {
        await page.goto(config.projects[0].use.baseURL || 'http://localhost:8080', {
          timeout: 5000
        });
        const title = await page.title();
        if (title.includes('Think AI')) {
          appReady = true;
          console.log('✅ App is ready for testing');
        }
      } catch (e) {
        retries++;
        console.log(`⏳ Waiting for app to be ready... (attempt ${retries}/${maxRetries})`);
        await new Promise(resolve => setTimeout(resolve, 2000));
      }
    }
    
    if (!appReady) {
      throw new Error('App failed to start in time');
    }
    
  } finally {
    await browser.close();
  }
  
  // Store any global state if needed
  return {
    startTime: Date.now()
  };
}

module.exports = globalSetup;