#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

// ANSI colors
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

// Tasks to run before commit
const tasks = [
  {
    name: 'Rust Format Check',
    command: 'cargo',
    args: ['fmt', '--all', '--check'],
    cwd: path.join(__dirname, '..', 'full-system')
  },
  {
    name: 'Rust Lint (Clippy)',
    command: 'cargo',
    args: ['clippy', '--', '-D', 'warnings'],
    cwd: path.join(__dirname, '..', 'full-system')
  },
  {
    name: 'Frontend Lint',
    command: 'npm',
    args: ['run', 'lint'],
    cwd: path.join(__dirname, '..', 'frontend')
  },
  {
    name: 'Frontend Type Check',
    command: 'npm',
    args: ['run', 'typecheck'],
    cwd: path.join(__dirname, '..', 'frontend')
  },
  {
    name: 'Backend Unit Tests',
    command: 'cargo',
    args: ['test', '--lib', '--', '--test-threads=1'],
    cwd: path.join(__dirname, '..', 'full-system')
  },
  {
    name: 'Frontend Unit Tests',
    command: 'npm',
    args: ['test', '--', '--run'],
    cwd: path.join(__dirname, '..', 'frontend')
  }
];

// Run a single task
function runTask(task) {
  return new Promise((resolve, reject) => {
    console.log(`${colors.blue}🔧 Running ${task.name}...${colors.reset}`);
    
    const startTime = Date.now();
    const proc = spawn(task.command, task.args, {
      cwd: task.cwd,
      stdio: 'pipe'
    });
    
    let output = '';
    let errorOutput = '';
    
    proc.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    proc.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });
    
    proc.on('close', (code) => {
      const duration = Date.now() - startTime;
      
      if (code === 0) {
        console.log(`${colors.green}✅ ${task.name} passed (${(duration / 1000).toFixed(2)}s)${colors.reset}`);
        resolve();
      } else {
        console.log(`${colors.red}❌ ${task.name} failed (exit code: ${code})${colors.reset}`);
        if (output) {
          console.log(`${colors.yellow}Output:${colors.reset}`);
          console.log(output);
        }
        if (errorOutput) {
          console.log(`${colors.red}Errors:${colors.reset}`);
          console.log(errorOutput);
        }
        reject(new Error(`${task.name} failed`));
      }
    });
    
    proc.on('error', (err) => {
      console.log(`${colors.red}❌ Failed to run ${task.name}: ${err.message}${colors.reset}`);
      reject(err);
    });
  });
}

// Main function
async function main() {
  console.log(`${colors.cyan}🚀 Think AI Pre-commit Checks${colors.reset}`);
  console.log('━'.repeat(50));
  
  const startTime = Date.now();
  let allPassed = true;
  
  // Run tasks sequentially
  for (const task of tasks) {
    try {
      await runTask(task);
    } catch (error) {
      allPassed = false;
      console.log(`${colors.red}⛔ Pre-commit check failed: ${error.message}${colors.reset}`);
      break;
    }
  }
  
  const totalDuration = Date.now() - startTime;
  console.log('━'.repeat(50));
  
  if (allPassed) {
    console.log(`${colors.green}✨ All pre-commit checks passed! (${(totalDuration / 1000).toFixed(2)}s)${colors.reset}`);
    console.log(`${colors.green}👍 Your commit is ready to go!${colors.reset}`);
    process.exit(0);
  } else {
    console.log(`${colors.red}💔 Pre-commit checks failed!${colors.reset}`);
    console.log(`${colors.yellow}📝 Please fix the issues before committing.${colors.reset}`);
    process.exit(1);
  }
}

// Check if we're running in a git hook context
if (process.env.GIT_PARAMS || process.env.HUSKY_GIT_PARAMS) {
  main().catch((error) => {
    console.error(`${colors.red}💥 Fatal error: ${error.message}${colors.reset}`);
    process.exit(1);
  });
} else {
  // Allow manual running
  console.log(`${colors.magenta}ℹ️  Running pre-commit checks manually...${colors.reset}\n`);
  main().catch((error) => {
    console.error(`${colors.red}💥 Fatal error: ${error.message}${colors.reset}`);
    process.exit(1);
  });
}