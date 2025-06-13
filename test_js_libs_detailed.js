#!/usr/bin/env node
/**
 * Detailed testing of Think AI JavaScript/TypeScript libraries
 */

const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

class JSLibraryTester {
  constructor() {
    this.results = {
      timestamp: Date.now(),
      tests: {},
      summary: { total: 0, passed: 0, failed: 0 }
    };
  }

  log(name, passed, details = "") {
    this.results.tests[name] = { passed, details, timestamp: Date.now() };
    this.results.summary.total++;
    if (passed) {
      this.results.summary.passed++;
      console.log(`✅ ${name}: PASSED`);
    } else {
      this.results.summary.failed++;
      console.log(`❌ ${name}: FAILED - ${details}`);
    }
    if (details) console.log(`   Details: ${details}`);
  }

  async runCommand(command, args, cwd = process.cwd()) {
    return new Promise((resolve) => {
      const proc = spawn(command, args, { 
        cwd, 
        stdio: ['pipe', 'pipe', 'pipe'],
        shell: true 
      });
      
      let stdout = '';
      let stderr = '';
      
      proc.stdout.on('data', (data) => stdout += data.toString());
      proc.stderr.on('data', (data) => stderr += data.toString());
      
      proc.on('close', (code) => {
        resolve({ code, stdout, stderr });
      });
      
      // Timeout after 30 seconds
      setTimeout(() => {
        proc.kill();
        resolve({ code: -1, stdout, stderr: 'Timeout' });
      }, 30000);
    });
  }

  testO1VectorSearchExists() {
    const indexPath = path.join('o1-js', 'src', 'index.ts');
    const testPath = path.join('o1-js', 'src', 'index.test.ts');
    
    if (fs.existsSync(indexPath) && fs.existsSync(testPath)) {
      this.log("O1 Vector Search Files", true, "Source and test files exist");
    } else {
      this.log("O1 Vector Search Files", false, "Missing source or test files");
    }
  }

  testNpmPackageExists() {
    const indexPath = path.join('npm', 'src', 'index.ts');
    const testPath = path.join('npm', 'src', 'index.test.ts');
    const packagePath = path.join('npm', 'package.json');
    
    if (fs.existsSync(indexPath) && fs.existsSync(testPath) && fs.existsSync(packagePath)) {
      this.log("NPM Package Files", true, "All NPM package files exist");
    } else {
      this.log("NPM Package Files", false, "Missing NPM package files");
    }
  }

  async testTypeScriptCompilation() {
    // Test O1-JS compilation
    const o1Result = await this.runCommand('npx', ['tsc', '--noEmit'], path.join(process.cwd(), 'o1-js'));
    
    if (o1Result.code === 0) {
      this.log("O1-JS TypeScript Compilation", true, "TypeScript compiles without errors");
    } else {
      this.log("O1-JS TypeScript Compilation", false, `Compilation errors: ${o1Result.stderr}`);
    }

    // Test NPM package compilation  
    const npmResult = await this.runCommand('npx', ['tsc', '--noEmit'], path.join(process.cwd(), 'npm'));
    
    if (npmResult.code === 0) {
      this.log("NPM TypeScript Compilation", true, "TypeScript compiles without errors");
    } else {
      this.log("NPM TypeScript Compilation", false, `Compilation errors: ${npmResult.stderr}`);
    }
  }

  async testJestTests() {
    // Test Jest specifically for our test files
    const jestResult = await this.runCommand('npx', ['jest', '--testPathPattern=.*\\.test\\.ts'], process.cwd());
    
    if (jestResult.code === 0) {
      this.log("Jest Tests Execution", true, "All Jest tests passed");
    } else {
      this.log("Jest Tests Execution", false, `Jest failures: ${jestResult.stderr}`);
    }
  }

  testPackageJsonStructure() {
    try {
      const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
      
      const hasDevDeps = packageJson.devDependencies && Object.keys(packageJson.devDependencies).length > 0;
      const hasDeps = packageJson.dependencies && Object.keys(packageJson.dependencies).length > 0;
      const hasScripts = packageJson.scripts && Object.keys(packageJson.scripts).length > 0;
      
      if (hasDevDeps && hasDeps && hasScripts) {
        this.log("Package.json Structure", true, "Complete package.json with deps and scripts");
      } else {
        this.log("Package.json Structure", false, "Incomplete package.json structure");
      }
    } catch (e) {
      this.log("Package.json Structure", false, `Error reading package.json: ${e.message}`);
    }
  }

  testConfigFiles() {
    const configs = [
      '.eslintrc.js',
      'jest.config.js', 
      'tsconfig.json'
    ];

    let allPresent = true;
    let missing = [];

    for (const config of configs) {
      if (!fs.existsSync(config)) {
        allPresent = false;
        missing.push(config);
      }
    }

    if (allPresent) {
      this.log("Configuration Files", true, "All config files present");
    } else {
      this.log("Configuration Files", false, `Missing: ${missing.join(', ')}`);
    }
  }

  async testO1VectorSearchFunctionality() {
    // Create a simple test to verify O1VectorSearch works
    const testCode = `
      const { O1VectorSearch } = require('./o1-js/dist/index.js');
      
      try {
        const index = new O1VectorSearch(3);
        index.add([1, 0, 0], { id: 'test1' });
        index.add([0, 1, 0], { id: 'test2' });
        
        const results = index.search([0.9, 0.1, 0], 1);
        
        if (results.length > 0 && results[0].metadata.id === 'test1') {
          console.log('SUCCESS');
        } else {
          console.log('FAILURE');
        }
      } catch (e) {
        console.log('ERROR: ' + e.message);
      }
    `;

    // First build the o1-js package
    const buildResult = await this.runCommand('npx', ['tsc'], path.join(process.cwd(), 'o1-js'));
    
    if (buildResult.code === 0) {
      this.log("O1-JS Build", true, "Successfully built O1-JS package");
      
      // Write and run the test
      fs.writeFileSync('temp_o1_test.js', testCode);
      const testResult = await this.runCommand('node', ['temp_o1_test.js']);
      
      if (testResult.stdout.includes('SUCCESS')) {
        this.log("O1 Vector Search Functionality", true, "O1VectorSearch works correctly");
      } else {
        this.log("O1 Vector Search Functionality", false, `Test failed: ${testResult.stdout}`);
      }
      
      // Cleanup
      if (fs.existsSync('temp_o1_test.js')) {
        fs.unlinkSync('temp_o1_test.js');
      }
    } else {
      this.log("O1-JS Build", false, `Build failed: ${buildResult.stderr}`);
    }
  }

  async runAllTests() {
    console.log("🧪 Think AI JavaScript/TypeScript Library Testing");
    console.log("=" * 60);

    this.testO1VectorSearchExists();
    this.testNpmPackageExists(); 
    this.testPackageJsonStructure();
    this.testConfigFiles();
    
    await this.testTypeScriptCompilation();
    await this.testJestTests();
    await this.testO1VectorSearchFunctionality();

    // Summary
    console.log("\n" + "=" * 60);
    console.log("📊 JAVASCRIPT LIBRARY TEST SUMMARY");
    console.log("=" * 60);
    
    const { total, passed, failed } = this.results.summary;
    console.log(`Total Tests: ${total}`);
    console.log(`Passed: ✅ ${passed}`);
    console.log(`Failed: ❌ ${failed}`);
    console.log(`Success Rate: ${(passed/total*100).toFixed(1)}%`);

    // Save results
    fs.writeFileSync('js_library_test_results.json', JSON.stringify(this.results, null, 2));
    console.log(`\n📝 Results saved to: js_library_test_results.json`);

    return passed === total;
  }
}

// Run if called directly
if (require.main === module) {
  const tester = new JSLibraryTester();
  tester.runAllTests().then(success => {
    if (success) {
      console.log("\n🎉 ALL JAVASCRIPT TESTS PASSED!");
      process.exit(0);
    } else {
      console.log("\n⚠️ Some JavaScript tests failed.");
      process.exit(1);
    }
  }).catch(error => {
    console.error("❌ Test runner error:", error);
    process.exit(1);
  });
}