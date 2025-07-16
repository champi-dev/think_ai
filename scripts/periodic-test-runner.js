#!/usr/bin/env node

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// Configuration
const TEST_INTERVAL = process.env.TEST_INTERVAL || 30 * 60 * 1000; // 30 minutes default
const LOG_DIR = path.join(__dirname, '..', 'test-results', 'periodic');
const NOTIFY_ON_FAILURE = process.env.NOTIFY_ON_FAILURE === 'true';

// Ensure log directory exists
if (!fs.existsSync(LOG_DIR)) {
  fs.mkdirSync(LOG_DIR, { recursive: true });
}

// Test suites to run
const testSuites = [
  {
    name: 'Backend Tests',
    command: 'npm',
    args: ['run', 'test:backend'],
    cwd: path.join(__dirname, '..')
  },
  {
    name: 'Frontend Tests',
    command: 'npm',
    args: ['run', 'test:frontend'],
    cwd: path.join(__dirname, '..')
  },
  {
    name: 'E2E Tests',
    command: 'npm',
    args: ['run', 'test:e2e'],
    cwd: path.join(__dirname, '..')
  }
];

// Run a single test suite
function runTestSuite(suite) {
  return new Promise((resolve) => {
    const startTime = Date.now();
    const logFile = path.join(LOG_DIR, `${suite.name.replace(/\s+/g, '-').toLowerCase()}-${new Date().toISOString().replace(/[:.]/g, '-')}.log`);
    const logStream = fs.createWriteStream(logFile);
    
    console.log(`🏃 Running ${suite.name}...`);
    
    const proc = spawn(suite.command, suite.args, {
      cwd: suite.cwd,
      env: { ...process.env, CI: 'true' }
    });
    
    let output = '';
    
    proc.stdout.on('data', (data) => {
      const str = data.toString();
      output += str;
      logStream.write(str);
    });
    
    proc.stderr.on('data', (data) => {
      const str = data.toString();
      output += str;
      logStream.write(str);
    });
    
    proc.on('close', (code) => {
      const duration = Date.now() - startTime;
      const success = code === 0;
      
      logStream.end();
      
      const result = {
        suite: suite.name,
        success,
        duration,
        exitCode: code,
        timestamp: new Date().toISOString(),
        logFile
      };
      
      if (success) {
        console.log(`✅ ${suite.name} passed in ${(duration / 1000).toFixed(2)}s`);
      } else {
        console.error(`❌ ${suite.name} failed with exit code ${code}`);
        if (NOTIFY_ON_FAILURE) {
          notifyFailure(suite.name, code, output);
        }
      }
      
      resolve(result);
    });
  });
}

// Run all test suites
async function runAllTests() {
  console.log(`🚀 Starting periodic test run at ${new Date().toISOString()}`);
  console.log('━'.repeat(50));
  
  const results = [];
  
  for (const suite of testSuites) {
    const result = await runTestSuite(suite);
    results.push(result);
  }
  
  // Write summary
  const summaryFile = path.join(LOG_DIR, `summary-${new Date().toISOString().replace(/[:.]/g, '-')}.json`);
  fs.writeFileSync(summaryFile, JSON.stringify({
    timestamp: new Date().toISOString(),
    results,
    allPassed: results.every(r => r.success),
    totalDuration: results.reduce((sum, r) => sum + r.duration, 0)
  }, null, 2));
  
  console.log('━'.repeat(50));
  console.log('📊 Test Summary:');
  results.forEach(r => {
    const icon = r.success ? '✅' : '❌';
    console.log(`  ${icon} ${r.suite}: ${r.success ? 'PASSED' : 'FAILED'} (${(r.duration / 1000).toFixed(2)}s)`);
  });
  
  const allPassed = results.every(r => r.success);
  if (allPassed) {
    console.log('\n🎉 All tests passed!');
  } else {
    console.log('\n⚠️  Some tests failed. Check logs for details.');
  }
  
  // Clean up old logs (keep last 7 days)
  cleanupOldLogs();
  
  return allPassed;
}

// Clean up old log files
function cleanupOldLogs() {
  const maxAge = 7 * 24 * 60 * 60 * 1000; // 7 days
  const now = Date.now();
  
  fs.readdirSync(LOG_DIR).forEach(file => {
    const filePath = path.join(LOG_DIR, file);
    const stats = fs.statSync(filePath);
    
    if (now - stats.mtime.getTime() > maxAge) {
      fs.unlinkSync(filePath);
      console.log(`🗑️  Deleted old log: ${file}`);
    }
  });
}

// Notify on failure (can be extended to send emails, Slack messages, etc.)
function notifyFailure(suiteName, exitCode, output) {
  console.error('\n🚨 TEST FAILURE NOTIFICATION 🚨');
  console.error(`Suite: ${suiteName}`);
  console.error(`Exit Code: ${exitCode}`);
  console.error('Last 50 lines of output:');
  console.error(output.split('\n').slice(-50).join('\n'));
  
  // TODO: Add email/Slack/webhook notification here
}

// Main execution
async function main() {
  console.log('🤖 Think AI Periodic Test Runner Started');
  console.log(`📅 Tests will run every ${TEST_INTERVAL / 1000 / 60} minutes`);
  console.log('Press Ctrl+C to stop\n');
  
  // Run tests immediately
  await runAllTests();
  
  // Schedule periodic runs
  const interval = setInterval(async () => {
    console.log('\n' + '='.repeat(60) + '\n');
    await runAllTests();
  }, TEST_INTERVAL);
  
  // Handle graceful shutdown
  process.on('SIGINT', () => {
    console.log('\n\n👋 Stopping periodic test runner...');
    clearInterval(interval);
    process.exit(0);
  });
  
  process.on('SIGTERM', () => {
    clearInterval(interval);
    process.exit(0);
  });
}

// Run as daemon if requested
if (process.argv.includes('--daemon')) {
  require('child_process').spawn(process.argv[0], [__filename], {
    detached: true,
    stdio: 'ignore'
  }).unref();
  
  console.log('🌙 Started in daemon mode. Check test-results/periodic/ for logs.');
  process.exit(0);
} else {
  main().catch(error => {
    console.error('💥 Fatal error:', error);
    process.exit(1);
  });
}