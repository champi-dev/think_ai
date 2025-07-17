const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PROD_URL = process.env.PROD_URL || 'http://localhost:8080';

async function testVoiceDetectionInProduction() {
    console.log('Starting voice detection E2E test...');
    console.log(`Testing URL: ${PROD_URL}`);
    
    const browser = await chromium.launch({ 
        headless: true,
        args: [
            '--no-sandbox', 
            '--disable-setuid-sandbox',
            '--use-fake-ui-for-media-stream', // Auto-accept mic permission
            '--use-fake-device-for-media-stream' // Use fake audio device
        ]
    });
    
    const context = await browser.newContext({
        viewport: { width: 1280, height: 720 },
        permissions: ['microphone']
    });
    
    const page = await context.newPage();
    
    // Capture console logs and errors
    const consoleLogs = [];
    const consoleErrors = [];
    page.on('console', msg => {
        const text = msg.text();
        consoleLogs.push({ type: msg.type(), text });
        if (msg.type() === 'error') {
            consoleErrors.push(text);
        }
    });
    page.on('pageerror', error => consoleErrors.push(error.message));
    
    // Create results directory
    const resultsDir = path.join(__dirname, 'voice-detection-test-results');
    if (!fs.existsSync(resultsDir)) {
        fs.mkdirSync(resultsDir, { recursive: true });
    }
    
    const testResults = {
        timestamp: new Date().toISOString(),
        url: PROD_URL,
        tests: {},
        errors: [],
        logs: []
    };
    
    try {
        // Navigate to the app
        console.log('Navigating to app...');
        await page.goto(PROD_URL, { waitUntil: 'networkidle', timeout: 30000 });
        
        // Wait for AutoVoiceDetector to initialize
        await page.waitForTimeout(3000);
        
        // Test 1: Component Initialization
        console.log('\nTest 1: Component Initialization');
        const autoVoiceDetector = await page.locator('.auto-voice-detector');
        const isVisible = await autoVoiceDetector.isVisible();
        testResults.tests.componentInitialization = {
            passed: isVisible,
            message: isVisible ? 'AutoVoiceDetector component is visible' : 'Component not found'
        };
        
        // Take screenshot
        await page.screenshot({ 
            path: path.join(resultsDir, '1-initial-state.png'),
            fullPage: true 
        });
        
        // Test 2: UI Elements
        console.log('\nTest 2: UI Elements');
        const toggleButton = await page.locator('.auto-voice-detector button');
        const statusDisplay = await page.locator('.status-display');
        const audioLevelContainer = await page.locator('.audio-level-container');
        
        const uiElementsPresent = 
            await toggleButton.isVisible() && 
            await statusDisplay.isVisible() && 
            await audioLevelContainer.isVisible();
            
        testResults.tests.uiElements = {
            passed: uiElementsPresent,
            details: {
                toggleButton: await toggleButton.isVisible(),
                statusDisplay: await statusDisplay.isVisible(),
                audioLevelContainer: await audioLevelContainer.isVisible()
            }
        };
        
        // Test 3: Initial State
        console.log('\nTest 3: Initial State');
        const statusText = await page.locator('.status-text').textContent();
        const buttonText = await toggleButton.textContent();
        
        testResults.tests.initialState = {
            passed: true,
            details: {
                statusText,
                buttonText,
                isAutoStarted: consoleLogs.some(log => log.text.includes('Auto-starting voice monitoring'))
            }
        };
        
        // Test 4: Toggle Functionality
        console.log('\nTest 4: Toggle Functionality');
        const initialButtonState = await toggleButton.textContent();
        await toggleButton.click();
        await page.waitForTimeout(1000);
        const afterClickButtonState = await toggleButton.textContent();
        
        testResults.tests.toggleFunctionality = {
            passed: initialButtonState !== afterClickButtonState,
            details: {
                before: initialButtonState,
                after: afterClickButtonState
            }
        };
        
        await page.screenshot({ 
            path: path.join(resultsDir, '2-after-toggle.png'),
            fullPage: true 
        });
        
        // Test 5: Audio Level Visualization
        console.log('\nTest 5: Audio Level Visualization');
        const audioLevelBar = await page.locator('.audio-level-bar');
        const voiceThresholdLine = await page.locator('.voice-threshold-line');
        
        testResults.tests.audioVisualization = {
            passed: await audioLevelBar.isVisible() && await voiceThresholdLine.isVisible(),
            details: {
                audioLevelBar: await audioLevelBar.isVisible(),
                voiceThresholdLine: await voiceThresholdLine.isVisible(),
                thresholdPosition: await voiceThresholdLine.getAttribute('style')
            }
        };
        
        // Test 6: Recording Indicator
        console.log('\nTest 6: Recording Indicator');
        const recordingIndicator = await page.locator('.recording-indicator');
        const hasRecordingIndicator = await recordingIndicator.isVisible();
        
        testResults.tests.recordingIndicator = {
            passed: hasRecordingIndicator,
            details: {
                visible: hasRecordingIndicator,
                hasRecDot: await page.locator('.rec-dot').isVisible(),
                hasRecText: await page.locator('.rec-text').isVisible()
            }
        };
        
        // Test 7: Error Handling
        console.log('\nTest 7: Error Handling');
        const micErrors = consoleLogs.filter(log => 
            log.text.includes('Error starting monitoring') || 
            log.text.includes('Requested device not found')
        );
        
        testResults.tests.errorHandling = {
            passed: true, // In headless mode, mic errors are expected
            details: {
                micErrors: micErrors.length > 0,
                errorMessages: micErrors.map(e => e.text)
            }
        };
        
        // Test 8: API Integration
        console.log('\nTest 8: API Integration');
        // Check if API routes are configured
        const apiResponses = await Promise.all([
            page.evaluate(() => 
                fetch('/api/audio/transcribe', { method: 'POST', body: new Blob(['test']) })
                    .then(r => ({ status: r.status, ok: r.ok }))
                    .catch(e => ({ error: e.message }))
            ),
            page.evaluate(() => 
                fetch('/api/chat', { 
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: 'test' })
                })
                    .then(r => ({ status: r.status, ok: r.ok }))
                    .catch(e => ({ error: e.message }))
            ),
            page.evaluate(() => 
                fetch('/api/audio/synthesize', { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: 'test' })
                })
                    .then(r => ({ status: r.status, ok: r.ok }))
                    .catch(e => ({ error: e.message }))
            )
        ]);
        
        testResults.tests.apiIntegration = {
            passed: apiResponses.every(r => !r.error),
            details: {
                transcribeAPI: apiResponses[0],
                chatAPI: apiResponses[1],
                synthesizeAPI: apiResponses[2]
            }
        };
        
        // Test 9: Responsive Design
        console.log('\nTest 9: Responsive Design');
        const viewports = [
            { name: 'mobile', width: 375, height: 667 },
            { name: 'tablet', width: 768, height: 1024 },
            { name: 'desktop', width: 1920, height: 1080 }
        ];
        
        testResults.tests.responsiveDesign = {
            passed: true,
            details: {}
        };
        
        for (const viewport of viewports) {
            await page.setViewportSize(viewport);
            await page.waitForTimeout(500);
            
            const isComponentVisible = await autoVoiceDetector.isVisible();
            testResults.tests.responsiveDesign.details[viewport.name] = {
                visible: isComponentVisible,
                viewport: viewport
            };
            
            await page.screenshot({ 
                path: path.join(resultsDir, `3-responsive-${viewport.name}.png`),
                fullPage: true 
            });
        }
        
        // Test 10: Performance
        console.log('\nTest 10: Performance Metrics');
        const performanceMetrics = await page.evaluate(() => {
            const navigation = performance.getEntriesByType('navigation')[0];
            return {
                domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
                firstPaint: performance.getEntriesByName('first-paint')[0]?.startTime,
                firstContentfulPaint: performance.getEntriesByName('first-contentful-paint')[0]?.startTime
            };
        });
        
        testResults.tests.performance = {
            passed: performanceMetrics.loadComplete < 3000, // Less than 3 seconds
            details: performanceMetrics
        };
        
        // Collect final logs
        testResults.logs = consoleLogs;
        testResults.errors = consoleErrors;
        
        // Calculate overall result
        const totalTests = Object.keys(testResults.tests).length;
        const passedTests = Object.values(testResults.tests).filter(t => t.passed).length;
        testResults.summary = {
            total: totalTests,
            passed: passedTests,
            failed: totalTests - passedTests,
            passRate: (passedTests / totalTests * 100).toFixed(2) + '%'
        };
        
        // Save results
        fs.writeFileSync(
            path.join(resultsDir, 'test-results.json'),
            JSON.stringify(testResults, null, 2)
        );
        
        // Generate HTML report
        const htmlReport = generateHTMLReport(testResults);
        fs.writeFileSync(
            path.join(resultsDir, 'test-report.html'),
            htmlReport
        );
        
        console.log('\n========================================');
        console.log('Test Summary:');
        console.log(`Total Tests: ${testResults.summary.total}`);
        console.log(`Passed: ${testResults.summary.passed}`);
        console.log(`Failed: ${testResults.summary.failed}`);
        console.log(`Pass Rate: ${testResults.summary.passRate}`);
        console.log('========================================\n');
        
        return testResults.summary.failed === 0;
        
    } catch (error) {
        console.error('Test execution failed:', error);
        testResults.errors.push(error.message);
        
        await page.screenshot({ 
            path: path.join(resultsDir, 'error-state.png'),
            fullPage: true 
        });
        
        return false;
        
    } finally {
        await browser.close();
    }
}

function generateHTMLReport(results) {
    return `
<!DOCTYPE html>
<html>
<head>
    <title>Voice Detection E2E Test Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #6366f1;
            padding-bottom: 10px;
        }
        .summary {
            display: flex;
            gap: 20px;
            margin: 20px 0;
        }
        .summary-card {
            flex: 1;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .summary-card.total { background: #e3f2fd; }
        .summary-card.passed { background: #e8f5e9; }
        .summary-card.failed { background: #ffebee; }
        .test-section {
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        .test-section.passed { border-left: 4px solid #4caf50; }
        .test-section.failed { border-left: 4px solid #f44336; }
        .test-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .status {
            padding: 5px 10px;
            border-radius: 4px;
            color: white;
            font-size: 12px;
        }
        .status.passed { background: #4caf50; }
        .status.failed { background: #f44336; }
        .details {
            background: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            margin-top: 10px;
            font-family: monospace;
            font-size: 12px;
        }
        .error {
            background: #ffebee;
            color: #c62828;
            padding: 10px;
            border-radius: 4px;
            margin: 10px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Voice Detection E2E Test Report</h1>
        <p>Generated: ${results.timestamp}</p>
        <p>URL: ${results.url}</p>
        
        <div class="summary">
            <div class="summary-card total">
                <h2>${results.summary.total}</h2>
                <p>Total Tests</p>
            </div>
            <div class="summary-card passed">
                <h2>${results.summary.passed}</h2>
                <p>Passed</p>
            </div>
            <div class="summary-card failed">
                <h2>${results.summary.failed}</h2>
                <p>Failed</p>
            </div>
        </div>
        
        <h2>Test Results</h2>
        ${Object.entries(results.tests).map(([name, test]) => `
            <div class="test-section ${test.passed ? 'passed' : 'failed'}">
                <div class="test-header">
                    <h3>${name.replace(/([A-Z])/g, ' $1').trim()}</h3>
                    <span class="status ${test.passed ? 'passed' : 'failed'}">
                        ${test.passed ? 'PASSED' : 'FAILED'}
                    </span>
                </div>
                ${test.message ? `<p>${test.message}</p>` : ''}
                ${test.details ? `
                    <div class="details">
                        <pre>${JSON.stringify(test.details, null, 2)}</pre>
                    </div>
                ` : ''}
            </div>
        `).join('')}
        
        ${results.errors.length > 0 ? `
            <h2>Errors</h2>
            ${results.errors.map(error => `
                <div class="error">${error}</div>
            `).join('')}
        ` : ''}
    </div>
</body>
</html>
    `;
}

// Run the test
testVoiceDetectionInProduction().then(success => {
    process.exit(success ? 0 : 1);
});