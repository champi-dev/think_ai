// Global teardown for e2e tests

async function globalTeardown(config) {
  console.log('🧹 Running global e2e test teardown...');
  
  // Clean up any test data
  // For example: clean test database, remove test files, etc.
  
  // If you stored global state in setup, you can access it here
  if (global.__testStartTime) {
    const duration = Date.now() - global.__testStartTime;
    console.log(`✅ Tests completed in ${(duration / 1000).toFixed(2)} seconds`);
  }
  
  console.log('🏁 Global teardown complete');
}

module.exports = globalTeardown;