#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// ANSI colors
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m'
};

// Coverage directories
const COVERAGE_DIR = path.join(__dirname, '..', 'coverage');
const BACKEND_COVERAGE = path.join(COVERAGE_DIR, 'backend');
const FRONTEND_COVERAGE = path.join(COVERAGE_DIR, 'frontend');
const COMBINED_COVERAGE = path.join(COVERAGE_DIR, 'combined');

// Ensure coverage directories exist
[COVERAGE_DIR, BACKEND_COVERAGE, FRONTEND_COVERAGE, COMBINED_COVERAGE].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

// Parse coverage percentage from string
function parseCoveragePercentage(str) {
  const match = str.match(/(\d+\.?\d*)%/);
  return match ? parseFloat(match[1]) : 0;
}

// Get color for coverage percentage
function getCoverageColor(percentage) {
  if (percentage >= 90) return colors.green;
  if (percentage >= 70) return colors.yellow;
  return colors.red;
}

// Generate backend coverage
async function generateBackendCoverage() {
  console.log(`${colors.cyan}📊 Generating backend coverage...${colors.reset}`);
  
  try {
    // Check if cargo-tarpaulin is installed
    try {
      execSync('cargo tarpaulin --version', { stdio: 'ignore' });
    } catch {
      console.log(`${colors.yellow}⚠️  Installing cargo-tarpaulin...${colors.reset}`);
      execSync('cargo install cargo-tarpaulin', { stdio: 'inherit' });
    }
    
    // Run tarpaulin
    const output = execSync(
      'cargo tarpaulin --out Html --out Json --output-dir ../coverage/backend --exclude-files "*/tests/*" --exclude-files "*/examples/*"',
      { cwd: path.join(__dirname, '..', 'full-system'), encoding: 'utf8' }
    );
    
    // Parse coverage from output
    const coverageMatch = output.match(/Coverage\s+(\d+\.?\d*)%/);
    const coverage = coverageMatch ? parseFloat(coverageMatch[1]) : 0;
    
    console.log(`${colors.green}✅ Backend coverage generated: ${coverage}%${colors.reset}`);
    
    return {
      type: 'backend',
      coverage,
      report: path.join(BACKEND_COVERAGE, 'tarpaulin-report.html'),
      json: path.join(BACKEND_COVERAGE, 'tarpaulin-report.json')
    };
  } catch (error) {
    console.error(`${colors.red}❌ Failed to generate backend coverage: ${error.message}${colors.reset}`);
    return { type: 'backend', coverage: 0, error: error.message };
  }
}

// Generate frontend coverage
async function generateFrontendCoverage() {
  console.log(`${colors.cyan}📊 Generating frontend coverage...${colors.reset}`);
  
  try {
    // Run vitest coverage
    const output = execSync(
      'npm run test:coverage',
      { cwd: path.join(__dirname, '..', 'frontend'), encoding: 'utf8' }
    );
    
    // Parse coverage from output
    let coverage = {
      statements: 0,
      branches: 0,
      functions: 0,
      lines: 0
    };
    
    // Try to read coverage summary
    const summaryPath = path.join(FRONTEND_COVERAGE, 'coverage-summary.json');
    if (fs.existsSync(summaryPath)) {
      const summary = JSON.parse(fs.readFileSync(summaryPath, 'utf8'));
      coverage = {
        statements: summary.total.statements.pct,
        branches: summary.total.branches.pct,
        functions: summary.total.functions.pct,
        lines: summary.total.lines.pct
      };
    } else {
      // Parse from console output as fallback
      const stmtMatch = output.match(/Statements\s*:\s*(\d+\.?\d*)%/);
      const branchMatch = output.match(/Branches\s*:\s*(\d+\.?\d*)%/);
      const funcMatch = output.match(/Functions\s*:\s*(\d+\.?\d*)%/);
      const lineMatch = output.match(/Lines\s*:\s*(\d+\.?\d*)%/);
      
      coverage = {
        statements: stmtMatch ? parseFloat(stmtMatch[1]) : 0,
        branches: branchMatch ? parseFloat(branchMatch[1]) : 0,
        functions: funcMatch ? parseFloat(funcMatch[1]) : 0,
        lines: lineMatch ? parseFloat(lineMatch[1]) : 0
      };
    }
    
    const avgCoverage = (coverage.statements + coverage.branches + coverage.functions + coverage.lines) / 4;
    
    console.log(`${colors.green}✅ Frontend coverage generated:${colors.reset}`);
    console.log(`   Statements: ${getCoverageColor(coverage.statements)}${coverage.statements}%${colors.reset}`);
    console.log(`   Branches:   ${getCoverageColor(coverage.branches)}${coverage.branches}%${colors.reset}`);
    console.log(`   Functions:  ${getCoverageColor(coverage.functions)}${coverage.functions}%${colors.reset}`);
    console.log(`   Lines:      ${getCoverageColor(coverage.lines)}${coverage.lines}%${colors.reset}`);
    
    return {
      type: 'frontend',
      coverage: avgCoverage,
      detailed: coverage,
      report: path.join(FRONTEND_COVERAGE, 'index.html')
    };
  } catch (error) {
    console.error(`${colors.red}❌ Failed to generate frontend coverage: ${error.message}${colors.reset}`);
    return { type: 'frontend', coverage: 0, error: error.message };
  }
}

// Generate combined coverage report
function generateCombinedReport(backendResult, frontendResult) {
  console.log(`\n${colors.cyan}📊 Generating combined coverage report...${colors.reset}`);
  
  const timestamp = new Date().toISOString();
  const totalCoverage = (backendResult.coverage + frontendResult.coverage) / 2;
  
  const report = {
    timestamp,
    totalCoverage: totalCoverage.toFixed(2),
    backend: {
      coverage: backendResult.coverage.toFixed(2),
      reportPath: backendResult.report,
      error: backendResult.error
    },
    frontend: {
      coverage: frontendResult.coverage.toFixed(2),
      detailed: frontendResult.detailed,
      reportPath: frontendResult.report,
      error: frontendResult.error
    }
  };
  
  // Write JSON report
  const jsonPath = path.join(COMBINED_COVERAGE, 'coverage-report.json');
  fs.writeFileSync(jsonPath, JSON.stringify(report, null, 2));
  
  // Generate HTML report
  const htmlReport = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Think AI Coverage Report</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .timestamp {
            color: #666;
            font-size: 14px;
            margin-bottom: 30px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }
        .card h2 {
            margin: 0 0 15px 0;
            color: #495057;
            font-size: 18px;
        }
        .coverage-bar {
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        .coverage-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }
        .coverage-fill.warning {
            background: linear-gradient(90deg, #ffc107, #fd7e14);
        }
        .coverage-fill.danger {
            background: linear-gradient(90deg, #dc3545, #e91e63);
        }
        .coverage-value {
            font-size: 24px;
            font-weight: bold;
            margin: 10px 0;
        }
        .coverage-value.good { color: #28a745; }
        .coverage-value.warning { color: #ffc107; }
        .coverage-value.danger { color: #dc3545; }
        .details {
            margin-top: 10px;
            font-size: 14px;
            color: #6c757d;
        }
        .details div {
            margin: 5px 0;
            display: flex;
            justify-content: space-between;
        }
        .link {
            display: inline-block;
            margin-top: 10px;
            color: #007bff;
            text-decoration: none;
        }
        .link:hover {
            text-decoration: underline;
        }
        .total-coverage {
            text-align: center;
            padding: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .total-coverage h2 {
            margin: 0 0 10px 0;
            font-size: 24px;
        }
        .total-coverage .value {
            font-size: 48px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🧠 Think AI Coverage Report</h1>
        <div class="timestamp">Generated: ${new Date(timestamp).toLocaleString()}</div>
        
        <div class="total-coverage">
            <h2>Total Coverage</h2>
            <div class="value">${totalCoverage.toFixed(1)}%</div>
        </div>
        
        <div class="summary">
            <div class="card">
                <h2>Backend Coverage (Rust)</h2>
                <div class="coverage-value ${backendResult.coverage >= 90 ? 'good' : backendResult.coverage >= 70 ? 'warning' : 'danger'}">
                    ${backendResult.coverage.toFixed(1)}%
                </div>
                <div class="coverage-bar">
                    <div class="coverage-fill ${backendResult.coverage >= 90 ? '' : backendResult.coverage >= 70 ? 'warning' : 'danger'}" 
                         style="width: ${backendResult.coverage}%"></div>
                </div>
                ${backendResult.report ? `<a href="${path.relative(COMBINED_COVERAGE, backendResult.report)}" class="link">View Detailed Report →</a>` : ''}
                ${backendResult.error ? `<div class="details" style="color: #dc3545;">Error: ${backendResult.error}</div>` : ''}
            </div>
            
            <div class="card">
                <h2>Frontend Coverage (React)</h2>
                <div class="coverage-value ${frontendResult.coverage >= 90 ? 'good' : frontendResult.coverage >= 70 ? 'warning' : 'danger'}">
                    ${frontendResult.coverage.toFixed(1)}%
                </div>
                <div class="coverage-bar">
                    <div class="coverage-fill ${frontendResult.coverage >= 90 ? '' : frontendResult.coverage >= 70 ? 'warning' : 'danger'}" 
                         style="width: ${frontendResult.coverage}%"></div>
                </div>
                ${frontendResult.detailed ? `
                <div class="details">
                    <div><span>Statements:</span> <span>${frontendResult.detailed.statements.toFixed(1)}%</span></div>
                    <div><span>Branches:</span> <span>${frontendResult.detailed.branches.toFixed(1)}%</span></div>
                    <div><span>Functions:</span> <span>${frontendResult.detailed.functions.toFixed(1)}%</span></div>
                    <div><span>Lines:</span> <span>${frontendResult.detailed.lines.toFixed(1)}%</span></div>
                </div>
                ` : ''}
                ${frontendResult.report ? `<a href="${path.relative(COMBINED_COVERAGE, frontendResult.report)}" class="link">View Detailed Report →</a>` : ''}
                ${frontendResult.error ? `<div class="details" style="color: #dc3545;">Error: ${frontendResult.error}</div>` : ''}
            </div>
        </div>
    </div>
</body>
</html>
  `.trim();
  
  const htmlPath = path.join(COMBINED_COVERAGE, 'index.html');
  fs.writeFileSync(htmlPath, htmlReport);
  
  console.log(`\n${colors.green}✅ Combined coverage report generated!${colors.reset}`);
  console.log(`${colors.blue}📄 HTML Report: ${htmlPath}${colors.reset}`);
  console.log(`${colors.blue}📄 JSON Report: ${jsonPath}${colors.reset}`);
  
  // Print summary
  console.log(`\n${colors.cyan}📊 Coverage Summary:${colors.reset}`);
  console.log('━'.repeat(50));
  console.log(`Total Coverage: ${getCoverageColor(totalCoverage)}${totalCoverage.toFixed(1)}%${colors.reset}`);
  console.log(`Backend:        ${getCoverageColor(backendResult.coverage)}${backendResult.coverage.toFixed(1)}%${colors.reset}`);
  console.log(`Frontend:       ${getCoverageColor(frontendResult.coverage)}${frontendResult.coverage.toFixed(1)}%${colors.reset}`);
  console.log('━'.repeat(50));
  
  return totalCoverage;
}

// Main function
async function main() {
  console.log(`${colors.cyan}🚀 Think AI Coverage Report Generator${colors.reset}`);
  console.log('━'.repeat(50));
  
  const startTime = Date.now();
  
  // Generate coverage for both backend and frontend
  const [backendResult, frontendResult] = await Promise.all([
    generateBackendCoverage(),
    generateFrontendCoverage()
  ]);
  
  // Generate combined report
  const totalCoverage = generateCombinedReport(backendResult, frontendResult);
  
  const duration = Date.now() - startTime;
  console.log(`\n⏱️  Total time: ${(duration / 1000).toFixed(2)}s`);
  
  // Exit with appropriate code based on coverage
  if (totalCoverage >= 90) {
    console.log(`\n${colors.green}🎉 Excellent coverage!${colors.reset}`);
    process.exit(0);
  } else if (totalCoverage >= 70) {
    console.log(`\n${colors.yellow}⚠️  Good coverage, but there's room for improvement.${colors.reset}`);
    process.exit(0);
  } else {
    console.log(`\n${colors.red}❌ Coverage is below 70%. Please add more tests!${colors.reset}`);
    process.exit(1);
  }
}

// Run the script
if (require.main === module) {
  main().catch(error => {
    console.error(`${colors.red}💥 Fatal error: ${error.message}${colors.reset}`);
    process.exit(1);
  });
}

module.exports = { generateBackendCoverage, generateFrontendCoverage, generateCombinedReport };