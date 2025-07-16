const { chromium } = require('playwright');
const fs = require('fs');

async function captureAudioUIEvidence() {
  console.log('🎨 Audio UI Visual Test');
  console.log('======================\n');
  
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  try {
    // 1. Initial page load
    console.log('1️⃣ Loading application...');
    await page.goto('https://thinkai.lat');
    await page.waitForTimeout(3000);
    await page.screenshot({ path: 'audio-test-evidence/ui-1-initial.png', fullPage: true });
    console.log('   ✅ Captured initial state\n');
    
    // 2. Highlight mic button
    console.log('2️⃣ Highlighting mic button...');
    await page.evaluate(() => {
      const micBtn = document.querySelector('.input-feature-toggle.mic');
      if (micBtn) {
        micBtn.style.border = '3px solid red';
        micBtn.style.boxShadow = '0 0 10px red';
      }
    });
    await page.screenshot({ path: 'audio-test-evidence/ui-2-mic-highlighted.png', fullPage: true });
    console.log('   ✅ Mic button highlighted and captured\n');
    
    // 3. Send a message
    console.log('3️⃣ Sending test message...');
    await page.fill('#queryInput', 'Hello! Please tell me about your audio capabilities.');
    await page.screenshot({ path: 'audio-test-evidence/ui-3-message-typed.png', fullPage: true });
    
    await page.press('#queryInput', 'Enter');
    console.log('   ⏳ Waiting for response...');
    
    // Wait for AI response
    await page.waitForSelector('.message.ai', { timeout: 30000 });
    await page.waitForTimeout(2000);
    
    // 4. Highlight audio playback button
    console.log('4️⃣ Highlighting audio playback button...');
    await page.evaluate(() => {
      const audioBtn = document.querySelector('.message.ai .audio-button');
      if (audioBtn) {
        audioBtn.style.border = '3px solid green';
        audioBtn.style.boxShadow = '0 0 10px green';
      }
    });
    await page.screenshot({ path: 'audio-test-evidence/ui-4-audio-button-highlighted.png', fullPage: true });
    console.log('   ✅ Audio button highlighted and captured\n');
    
    // 5. Test at different resolutions
    console.log('5️⃣ Testing responsive design...');
    
    const resolutions = [
      { width: 1920, height: 1080, name: 'desktop' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 375, height: 667, name: 'mobile' },
      { width: 320, height: 480, name: 'small-mobile' }
    ];
    
    for (const res of resolutions) {
      await page.setViewportSize({ width: res.width, height: res.height });
      await page.waitForTimeout(1000);
      await page.screenshot({ 
        path: `audio-test-evidence/ui-5-responsive-${res.name}.png`,
        fullPage: true 
      });
      console.log(`   ✅ Captured ${res.name} (${res.width}x${res.height})`);
    }
    
    console.log('\n✅ All visual tests completed successfully!');
    console.log('📁 Evidence saved in: audio-test-evidence/');
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    await page.screenshot({ path: 'audio-test-evidence/ui-error.png', fullPage: true });
  } finally {
    await browser.close();
  }
}

captureAudioUIEvidence().catch(console.error);