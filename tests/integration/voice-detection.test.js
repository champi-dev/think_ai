const { test, expect } = require('@playwright/test');
const fs = require('fs');
const path = require('path');

// Helper to create mock audio blob
function createMockAudioBlob() {
  // Create a simple WAV file header
  const sampleRate = 44100;
  const numChannels = 1;
  const bitsPerSample = 16;
  const duration = 2; // 2 seconds
  const numSamples = sampleRate * duration;
  const dataSize = numSamples * numChannels * (bitsPerSample / 8);
  
  const buffer = new ArrayBuffer(44 + dataSize);
  const view = new DataView(buffer);
  
  // WAV header
  const setString = (offset, string) => {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  };
  
  setString(0, 'RIFF');
  view.setUint32(4, 36 + dataSize, true);
  setString(8, 'WAVE');
  setString(12, 'fmt ');
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, numChannels, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * numChannels * (bitsPerSample / 8), true);
  view.setUint16(32, numChannels * (bitsPerSample / 8), true);
  view.setUint16(34, bitsPerSample, true);
  setString(36, 'data');
  view.setUint32(40, dataSize, true);
  
  // Generate simple sine wave audio data
  for (let i = 0; i < numSamples; i++) {
    const sample = Math.sin(2 * Math.PI * 440 * i / sampleRate) * 32767;
    view.setInt16(44 + i * 2, sample, true);
  }
  
  return new Blob([buffer], { type: 'audio/wav' });
}

test.describe('Voice Auto-Detection Integration Tests', () => {
  test.beforeEach(async ({ page, context }) => {
    // Grant microphone permissions
    await context.grantPermissions(['microphone']);
    
    // Mock getUserMedia to return a fake stream
    await page.addInitScript(() => {
      const mockStream = {
        getTracks: () => [{
          stop: () => {},
          kind: 'audio',
          enabled: true
        }],
        getAudioTracks: () => [{
          stop: () => {},
          enabled: true
        }]
      };
      
      window.navigator.mediaDevices.getUserMedia = async () => mockStream;
    });
  });

  test('should initialize auto-detection on page load', async ({ page }) => {
    await page.goto('http://localhost:8080');
    
    // Wait for AutoVoiceDetector to mount
    await page.waitForTimeout(2000);
    
    // Check console logs
    const consoleLogs = [];
    page.on('console', msg => consoleLogs.push(msg.text()));
    
    expect(consoleLogs.some(log => log.includes('AutoVoiceDetector component mounted'))).toBeTruthy();
    expect(consoleLogs.some(log => log.includes('Auto-starting voice monitoring'))).toBeTruthy();
    
    // Check UI elements
    const toggleButton = await page.locator('.auto-voice-detector button');
    await expect(toggleButton).toBeVisible();
    
    // Should show monitoring state after auto-start
    await expect(page.locator('.status-text')).toContainText(/Listening for voice|Mic permission needed/);
  });

  test('should toggle monitoring on/off', async ({ page }) => {
    await page.goto('http://localhost:8080');
    await page.waitForTimeout(2000);
    
    const toggleButton = await page.locator('.auto-voice-detector button');
    const statusText = await page.locator('.status-text');
    
    // Turn off if auto-started
    if (await toggleButton.locator('text=Auto-Detection ON').isVisible()) {
      await toggleButton.click();
      await expect(toggleButton).toContainText('Auto-Detection OFF');
      await expect(statusText).toContainText('Auto-detection off');
    }
    
    // Turn on
    await toggleButton.click();
    await expect(toggleButton).toContainText('Auto-Detection ON');
    await expect(statusText).toContainText('Listening for voice');
    
    // Turn off again
    await toggleButton.click();
    await expect(toggleButton).toContainText('Auto-Detection OFF');
  });

  test('should show audio level visualization', async ({ page }) => {
    await page.goto('http://localhost:8080');
    await page.waitForTimeout(2000);
    
    // Ensure monitoring is on
    const toggleButton = await page.locator('.auto-voice-detector button');
    if (await toggleButton.locator('text=Auto-Detection OFF').isVisible()) {
      await toggleButton.click();
    }
    
    // Check for audio level elements
    const audioLevelBar = await page.locator('.audio-level-bar');
    const voiceThresholdLine = await page.locator('.voice-threshold-line');
    
    await expect(audioLevelBar).toBeVisible();
    await expect(voiceThresholdLine).toBeVisible();
    
    // Check that threshold line is positioned correctly (8% from left)
    const thresholdStyle = await voiceThresholdLine.getAttribute('style');
    expect(thresholdStyle).toContain('left: 8%');
  });

  test('should handle full voice interaction flow', async ({ page }) => {
    // Mock API responses
    await page.route('/api/audio/transcribe', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ text: 'Hello, how are you?' })
      });
    });
    
    await page.route('/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ 
          response: "I'm doing great, thank you for asking!",
          session_id: 'test-session'
        })
      });
    });
    
    await page.route('/api/audio/synthesize', async route => {
      // Return a mock audio file
      const audioBlob = createMockAudioBlob();
      const buffer = await audioBlob.arrayBuffer();
      await route.fulfill({
        status: 200,
        contentType: 'audio/mp3',
        body: Buffer.from(buffer)
      });
    });
    
    await page.goto('http://localhost:8080');
    await page.waitForTimeout(2000);
    
    // Simulate recording completion
    await page.evaluate(() => {
      const recorder = window.mediaRecorderRef?.current;
      if (recorder && recorder.ondataavailable && recorder.onstop) {
        recorder.ondataavailable({ 
          data: new Blob(['mock audio'], { type: 'audio/webm' }) 
        });
        recorder.onstop();
      }
    });
    
    // Check status updates
    const statusText = await page.locator('.status-text');
    
    // Should show transcribing
    await expect(statusText).toContainText('Transcribing', { timeout: 5000 });
    
    // Should show thinking
    await expect(statusText).toContainText('Thinking', { timeout: 5000 });
    
    // Should show speaking
    await expect(statusText).toContainText('Speaking', { timeout: 5000 });
  });

  test('should handle API errors gracefully', async ({ page }) => {
    // Mock failed transcription
    await page.route('/api/audio/transcribe', async route => {
      await route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Server error' })
      });
    });
    
    await page.goto('http://localhost:8080');
    await page.waitForTimeout(2000);
    
    // Simulate recording completion
    await page.evaluate(() => {
      const recorder = window.mediaRecorderRef?.current;
      if (recorder && recorder.ondataavailable && recorder.onstop) {
        recorder.ondataavailable({ 
          data: new Blob(['mock audio'], { type: 'audio/webm' }) 
        });
        recorder.onstop();
      }
    });
    
    // Should show error
    const statusText = await page.locator('.status-text');
    await expect(statusText).toContainText('Error occurred', { timeout: 5000 });
    
    // Should resume monitoring after delay
    await page.waitForTimeout(3000);
    await expect(statusText).toContainText('Listening for voice');
  });

  test('should show recording indicator when recording', async ({ page }) => {
    await page.goto('http://localhost:8080');
    await page.waitForTimeout(2000);
    
    const recordingIndicator = await page.locator('.recording-indicator');
    
    // Initially not active
    await expect(recordingIndicator).not.toHaveClass(/active/);
    
    // Simulate recording start
    await page.evaluate(() => {
      window.setIsRecording?.(true);
      window.isRecordingRef = { current: true };
    });
    
    // Should show active recording indicator
    await expect(recordingIndicator).toHaveClass(/active/);
  });

  test('should work with different languages', async ({ page }) => {
    // Mock language detection
    await page.addInitScript(() => {
      window.detectLanguage = async () => 'es'; // Spanish
    });
    
    await page.goto('http://localhost:8080');
    await page.waitForTimeout(2000);
    
    // Check that language is passed to API calls
    let chatRequestBody;
    await page.route('/api/chat', async route => {
      chatRequestBody = route.request().postDataJSON();
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ response: 'Hola!' })
      });
    });
    
    // Trigger a transcription
    await page.evaluate(() => {
      window.sendAudioForTranscription?.(new Blob(['audio'], { type: 'audio/webm' }));
    });
    
    await page.waitForTimeout(1000);
    
    // Verify language was included in request
    expect(chatRequestBody?.language).toBe('es');
  });
});