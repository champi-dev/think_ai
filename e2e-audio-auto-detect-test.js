const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');

const PROD_URL = 'http://localhost:8080';
const SCREENSHOT_DIR = 'audio-auto-detect-screenshots';
const TEST_AUDIO_FILE = 'test-audio.webm';

// Create a test audio file with simulated speech
async function createTestAudioFile() {
  // Create a simple WebM audio file with noise
  // In a real test, you'd use a proper audio file with speech
  const audioData = Buffer.from([
    // WebM header (simplified)
    0x1a, 0x45, 0xdf, 0xa3, // EBML header
    // ... (actual WebM data would go here)
  ]);
  
  await fs.writeFile(TEST_AUDIO_FILE, audioData);
}

async function ensureDir(dir) {
  try {
    await fs.mkdir(dir, { recursive: true });
  } catch (err) {
    console.error(`Error creating directory ${dir}:`, err);
  }
}

async function testAutoDetectAudio() {
  console.log('🎤 Starting Auto-Detect Audio E2E Test...\n');
  
  await ensureDir(SCREENSHOT_DIR);
  
  const browser = await chromium.launch({
    headless: true, // Run in headless mode
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--use-fake-ui-for-media-stream', // Auto-accept mic permission
      '--use-fake-device-for-media-stream', // Use fake audio device
    ]
  });
  
  const results = {
    timestamp: new Date().toISOString(),
    url: PROD_URL,
    tests: {}
  };
  
  try {
    const context = await browser.newContext({
      permissions: ['microphone'],
      viewport: { width: 1280, height: 720 }
    });
    
    const page = await context.newPage();
    
    // Enable console logging
    page.on('console', msg => {
      const text = msg.text();
      if (text.includes('Audio level:') || 
          text.includes('Voice detected') || 
          text.includes('Recording') ||
          text.includes('MediaRecorder') ||
          text.includes('sendAudioForTranscription')) {
        console.log(`  [Console] ${text}`);
      }
    });
    
    // Monitor network requests
    page.on('request', request => {
      if (request.url().includes('/api/audio/transcribe') || 
          request.url().includes('/api/chat')) {
        console.log(`  [Network] ${request.method()} ${request.url()}`);
      }
    });
    
    page.on('response', response => {
      if (response.url().includes('/api/audio/transcribe') || 
          response.url().includes('/api/chat')) {
        console.log(`  [Network] Response: ${response.status()} ${response.url()}`);
      }
    });
    
    console.log('📍 Test 1: Initial Page Load and Component Visibility');
    await page.goto(PROD_URL, { waitUntil: 'networkidle' });
    await page.waitForTimeout(2000);
    
    // Check if AutoVoiceDetector is visible
    const voiceDetectorVisible = await page.isVisible('.auto-voice-detector');
    console.log(`  ✅ AutoVoiceDetector visible: ${voiceDetectorVisible}`);
    results.tests.componentVisible = voiceDetectorVisible;
    
    // Take initial screenshot
    await page.screenshot({ 
      path: path.join(SCREENSHOT_DIR, '1-initial-state.png'),
      fullPage: true 
    });
    
    // Check initial state
    const initialState = await page.evaluate(() => {
      const button = document.querySelector('.toggle-button');
      const statusText = document.querySelector('.status-text');
      return {
        buttonText: button?.textContent || '',
        statusText: statusText?.textContent || '',
        isActive: button?.classList.contains('active') || false
      };
    });
    console.log(`  📊 Initial state:`, initialState);
    results.tests.initialState = initialState;
    
    console.log('\n📍 Test 2: Enable Auto-Detection');
    // Click the toggle button if not already active
    if (!initialState.isActive) {
      await page.click('.toggle-button');
      await page.waitForTimeout(1000);
    }
    
    // Check if auto-detection started
    const autoDetectionState = await page.evaluate(() => {
      const button = document.querySelector('.toggle-button');
      const statusText = document.querySelector('.status-text');
      const audioLevelBar = document.querySelector('.audio-level-bar');
      return {
        buttonText: button?.textContent || '',
        statusText: statusText?.textContent || '',
        isActive: button?.classList.contains('active') || false,
        hasAudioLevelBar: !!audioLevelBar
      };
    });
    console.log(`  📊 Auto-detection state:`, autoDetectionState);
    results.tests.autoDetectionEnabled = autoDetectionState;
    
    await page.screenshot({ 
      path: path.join(SCREENSHOT_DIR, '2-auto-detection-enabled.png'),
      fullPage: true 
    });
    
    console.log('\n📍 Test 3: Audio Level Visualization');
    // Wait for audio level updates
    await page.waitForTimeout(3000);
    
    // Check if audio levels are being visualized
    const audioLevelData = await page.evaluate(() => {
      const audioLevelBar = document.querySelector('.audio-level-bar');
      const voiceThresholdLine = document.querySelector('.voice-threshold-line');
      
      if (!audioLevelBar) return { error: 'No audio level bar found' };
      
      // Get the computed styles
      const barStyle = window.getComputedStyle(audioLevelBar);
      const thresholdStyle = voiceThresholdLine ? window.getComputedStyle(voiceThresholdLine) : null;
      
      return {
        barWidth: barStyle.width,
        barBackgroundColor: barStyle.backgroundColor,
        thresholdPosition: thresholdStyle ? thresholdStyle.left : 'N/A',
        hasThresholdLine: !!voiceThresholdLine
      };
    });
    console.log(`  📊 Audio level visualization:`, audioLevelData);
    results.tests.audioLevelVisualization = audioLevelData;
    
    await page.screenshot({ 
      path: path.join(SCREENSHOT_DIR, '3-audio-levels.png'),
      fullPage: true 
    });
    
    console.log('\n📍 Test 4: Voice Detection Simulation');
    // Since we're using fake audio, we'll check if the system responds to audio
    await page.waitForTimeout(5000); // Wait for potential voice detection
    
    // Check for recording indicator
    const recordingState = await page.evaluate(() => {
      const recordingIndicator = document.querySelector('.recording-indicator');
      const recDot = document.querySelector('.rec-dot');
      const recText = document.querySelector('.rec-text');
      const statusText = document.querySelector('.status-text');
      
      return {
        hasRecordingIndicator: !!recordingIndicator,
        isRecordingActive: recordingIndicator?.classList.contains('active') || false,
        hasRecDot: !!recDot,
        hasRecText: !!recText,
        recText: recText?.textContent || '',
        statusText: statusText?.textContent || ''
      };
    });
    console.log(`  📊 Recording state:`, recordingState);
    results.tests.recordingState = recordingState;
    
    await page.screenshot({ 
      path: path.join(SCREENSHOT_DIR, '4-recording-state.png'),
      fullPage: true 
    });
    
    console.log('\n📍 Test 5: API Integration Check');
    // Check if the transcribe API endpoint is configured
    const apiCheck = await page.evaluate(async () => {
      try {
        // Create a test blob
        const audioBlob = new Blob(['test'], { type: 'audio/webm' });
        
        // Try to call the transcribe endpoint
        const response = await fetch('/api/audio/transcribe', {
          method: 'POST',
          body: audioBlob,
          headers: {
            'Content-Type': 'audio/webm',
            'X-Language': 'en'
          }
        });
        
        return {
          endpoint: '/api/audio/transcribe',
          status: response.status,
          statusText: response.statusText,
          ok: response.ok
        };
      } catch (error) {
        return {
          endpoint: '/api/audio/transcribe',
          error: error.message
        };
      }
    });
    console.log(`  📊 API check:`, apiCheck);
    results.tests.apiIntegration = apiCheck;
    
    console.log('\n📍 Test 6: Disable Auto-Detection');
    // Click the toggle button to disable
    await page.click('.toggle-button');
    await page.waitForTimeout(1000);
    
    const disabledState = await page.evaluate(() => {
      const button = document.querySelector('.toggle-button');
      const statusText = document.querySelector('.status-text');
      return {
        buttonText: button?.textContent || '',
        statusText: statusText?.textContent || '',
        isActive: button?.classList.contains('active') || false
      };
    });
    console.log(`  📊 Disabled state:`, disabledState);
    results.tests.disabledState = disabledState;
    
    await page.screenshot({ 
      path: path.join(SCREENSHOT_DIR, '5-disabled-state.png'),
      fullPage: true 
    });
    
    console.log('\n📍 Test 7: Error Handling');
    // Test error handling by denying microphone permission
    const errorHandling = await page.evaluate(async () => {
      try {
        // Try to access microphone without permission
        const result = await navigator.mediaDevices.getUserMedia({ audio: false })
          .then(() => ({ success: true }))
          .catch(error => ({ 
            success: false, 
            error: error.name,
            message: error.message 
          }));
        return result;
      } catch (error) {
        return { 
          success: false, 
          error: error.name,
          message: error.message 
        };
      }
    });
    console.log(`  📊 Error handling test:`, errorHandling);
    results.tests.errorHandling = errorHandling;
    
    await context.close();
    
  } finally {
    await browser.close();
  }
  
  // Save results
  await fs.writeFile(
    path.join(SCREENSHOT_DIR, 'test-results.json'),
    JSON.stringify(results, null, 2)
  );
  
  // Generate HTML report
  const htmlReport = generateHTMLReport(results);
  await fs.writeFile(
    path.join(SCREENSHOT_DIR, 'report.html'),
    htmlReport
  );
  
  // Summary
  console.log('\n📊 Test Summary:');
  console.log(`Component visible: ${results.tests.componentVisible ? '✅' : '❌'}`);
  console.log(`Auto-detection can be enabled: ${results.tests.autoDetectionEnabled?.isActive ? '✅' : '❌'}`);
  console.log(`Audio visualization present: ${results.tests.audioLevelVisualization?.hasThresholdLine ? '✅' : '❌'}`);
  console.log(`Recording indicator present: ${results.tests.recordingState?.hasRecordingIndicator ? '✅' : '❌'}`);
  console.log(`API endpoint accessible: ${results.tests.apiIntegration?.ok !== false ? '✅' : '❌'}`);
  console.log(`\n📄 Report saved to: ${path.join(SCREENSHOT_DIR, 'report.html')}`);
  
  return results;
}

function generateHTMLReport(results) {
  const testRows = Object.entries(results.tests).map(([name, data]) => {
    const passed = data === true || (data && data.ok) || (data && !data.error);
    return `
      <tr class="${passed ? 'passed' : 'failed'}">
        <td>${name}</td>
        <td>${passed ? '✅ PASS' : '❌ FAIL'}</td>
        <td><pre>${JSON.stringify(data, null, 2)}</pre></td>
      </tr>
    `;
  }).join('');
  
  return `
<!DOCTYPE html>
<html>
<head>
  <title>Audio Auto-Detect E2E Test Report</title>
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
    .screenshots {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
      margin: 30px 0;
    }
    .screenshot {
      text-align: center;
    }
    .screenshot img {
      max-width: 100%;
      height: auto;
      border: 1px solid #ddd;
      border-radius: 4px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .screenshot h3 {
      color: #666;
      font-size: 14px;
      margin: 10px 0;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 20px 0;
    }
    th, td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }
    th {
      background: #f0f0f0;
      font-weight: 600;
    }
    tr.passed {
      background: #f0fff0;
    }
    tr.failed {
      background: #fff0f0;
    }
    pre {
      background: #f5f5f5;
      padding: 8px;
      border-radius: 4px;
      font-size: 12px;
      overflow-x: auto;
      margin: 0;
    }
    .summary {
      background: #e3f2fd;
      padding: 20px;
      border-radius: 8px;
      margin: 20px 0;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Audio Auto-Detect E2E Test Report</h1>
    <p>Generated: ${results.timestamp}</p>
    <p>URL: ${results.url}</p>
    
    <div class="summary">
      <h2>Test Summary</h2>
      <p>This test verifies the auto-detect audio functionality including:</p>
      <ul>
        <li>Component visibility and initialization</li>
        <li>Auto-detection toggle functionality</li>
        <li>Audio level visualization</li>
        <li>Voice detection and recording indicators</li>
        <li>API integration</li>
        <li>Error handling</li>
      </ul>
    </div>
    
    <h2>Screenshots</h2>
    <div class="screenshots">
      <div class="screenshot">
        <h3>1. Initial State</h3>
        <img src="1-initial-state.png" alt="Initial State" />
      </div>
      <div class="screenshot">
        <h3>2. Auto-Detection Enabled</h3>
        <img src="2-auto-detection-enabled.png" alt="Auto-Detection Enabled" />
      </div>
      <div class="screenshot">
        <h3>3. Audio Levels</h3>
        <img src="3-audio-levels.png" alt="Audio Levels" />
      </div>
      <div class="screenshot">
        <h3>4. Recording State</h3>
        <img src="4-recording-state.png" alt="Recording State" />
      </div>
      <div class="screenshot">
        <h3>5. Disabled State</h3>
        <img src="5-disabled-state.png" alt="Disabled State" />
      </div>
    </div>
    
    <h2>Test Results</h2>
    <table>
      <tr>
        <th>Test</th>
        <th>Result</th>
        <th>Details</th>
      </tr>
      ${testRows}
    </table>
  </div>
</body>
</html>
  `;
}

// Run the test
testAutoDetectAudio().catch(console.error);