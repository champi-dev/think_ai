const { chromium } = require('playwright');
const fs = require('fs').promises;
const path = require('path');

const PROD_URL = 'http://localhost:8080';
const SCREENSHOT_DIR = 'responsive-ui-screenshots';

// Test viewports including ultra-small resolutions
const VIEWPORTS = [
  { name: 'desktop-4k', width: 3840, height: 2160 },
  { name: 'desktop-1080p', width: 1920, height: 1080 },
  { name: 'laptop', width: 1366, height: 768 },
  { name: 'tablet-landscape', width: 1024, height: 768 },
  { name: 'tablet-portrait', width: 768, height: 1024 },
  { name: 'mobile-large', width: 414, height: 896 }, // iPhone 11 Pro Max
  { name: 'mobile-medium', width: 375, height: 667 }, // iPhone 8
  { name: 'mobile-small', width: 320, height: 568 }, // iPhone 5/SE
  { name: 'ultra-small', width: 280, height: 480 },
  { name: 'micro', width: 200, height: 300 },
  { name: 'nano', width: 150, height: 200 },
  { name: 'minimum', width: 100, height: 100 }
];

async function ensureDir(dir) {
  try {
    await fs.mkdir(dir, { recursive: true });
  } catch (err) {
    console.error(`Error creating directory ${dir}:`, err);
  }
}

async function checkElementOverlap(page) {
  return await page.evaluate(() => {
    function getElementBounds(selector) {
      const el = document.querySelector(selector);
      if (!el) return null;
      const rect = el.getBoundingClientRect();
      return {
        top: rect.top,
        left: rect.left,
        bottom: rect.bottom,
        right: rect.right,
        width: rect.width,
        height: rect.height
      };
    }

    function doElementsOverlap(rect1, rect2) {
      if (!rect1 || !rect2) return false;
      return !(rect1.right < rect2.left || 
               rect2.right < rect1.left || 
               rect1.bottom < rect2.top || 
               rect2.bottom < rect1.top);
    }

    const elements = {
      header: getElementBounds('.header'),
      messages: getElementBounds('.messages'),
      input: getElementBounds('.input-container'),
      voiceDetector: getElementBounds('.auto-voice-detector'),
      modeToggle: getElementBounds('.mode-toggle'),
      sendButton: getElementBounds('#sendBtn')
    };

    const overlaps = [];
    const elementNames = Object.keys(elements);
    
    for (let i = 0; i < elementNames.length; i++) {
      for (let j = i + 1; j < elementNames.length; j++) {
        const name1 = elementNames[i];
        const name2 = elementNames[j];
        if (doElementsOverlap(elements[name1], elements[name2])) {
          overlaps.push(`${name1} overlaps with ${name2}`);
        }
      }
    }

    return {
      elements,
      overlaps,
      hasOverlaps: overlaps.length > 0
    };
  });
}

async function testResponsiveUI() {
  console.log('🚀 Starting Responsive UI Test...\n');
  
  await ensureDir(SCREENSHOT_DIR);
  
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const results = {
    timestamp: new Date().toISOString(),
    url: PROD_URL,
    viewports: []
  };
  
  try {
    for (const viewport of VIEWPORTS) {
      console.log(`\n📱 Testing ${viewport.name} (${viewport.width}x${viewport.height})...`);
      
      const context = await browser.newContext({
        viewport: { width: viewport.width, height: viewport.height },
        deviceScaleFactor: 1,
        permissions: ['microphone']
      });
      
      const page = await context.newPage();
      
      try {
        // Navigate to the page
        await page.goto(PROD_URL, { waitUntil: 'networkidle' });
        await page.waitForTimeout(2000); // Wait for animations
        
        // Take initial screenshot
        const screenshotPath = path.join(SCREENSHOT_DIR, `${viewport.name}-initial.png`);
        await page.screenshot({ 
          path: screenshotPath,
          fullPage: true 
        });
        console.log(`  ✅ Screenshot saved: ${screenshotPath}`);
        
        // Check for element overlaps
        const overlapCheck = await checkElementOverlap(page);
        console.log(`  📊 Elements analysis:`);
        console.log(`     - Header present: ${!!overlapCheck.elements.header}`);
        console.log(`     - Messages area present: ${!!overlapCheck.elements.messages}`);
        console.log(`     - Input area present: ${!!overlapCheck.elements.input}`);
        console.log(`     - Voice detector present: ${!!overlapCheck.elements.voiceDetector}`);
        
        if (overlapCheck.hasOverlaps) {
          console.log(`  ❌ OVERLAPS DETECTED:`);
          overlapCheck.overlaps.forEach(overlap => {
            console.log(`     - ${overlap}`);
          });
        } else {
          console.log(`  ✅ No overlapping elements`);
        }
        
        // Check visibility of critical elements
        const visibility = await page.evaluate(() => {
          function isElementVisible(selector) {
            const el = document.querySelector(selector);
            if (!el) return false;
            const rect = el.getBoundingClientRect();
            const style = window.getComputedStyle(el);
            return rect.width > 0 && 
                   rect.height > 0 && 
                   style.opacity !== '0' && 
                   style.visibility !== 'hidden' &&
                   style.display !== 'none';
          }
          
          return {
            header: isElementVisible('.header'),
            messages: isElementVisible('.messages'),
            input: isElementVisible('.input-container'),
            sendButton: isElementVisible('#sendBtn'),
            voiceDetector: isElementVisible('.auto-voice-detector'),
            queryInput: isElementVisible('#queryInput')
          };
        });
        
        console.log(`  👁️  Visibility check:`);
        Object.entries(visibility).forEach(([element, visible]) => {
          console.log(`     - ${element}: ${visible ? '✅ visible' : '❌ hidden'}`);
        });
        
        // Test input interaction
        if (visibility.queryInput) {
          await page.fill('#queryInput', 'Test message');
          await page.screenshot({ 
            path: path.join(SCREENSHOT_DIR, `${viewport.name}-with-text.png`),
            fullPage: true 
          });
        }
        
        // Store results
        results.viewports.push({
          ...viewport,
          screenshot: `${viewport.name}-initial.png`,
          overlaps: overlapCheck.overlaps,
          hasOverlaps: overlapCheck.hasOverlaps,
          visibility,
          elementBounds: overlapCheck.elements
        });
        
      } catch (error) {
        console.error(`  ❌ Error testing ${viewport.name}:`, error.message);
        results.viewports.push({
          ...viewport,
          error: error.message
        });
      } finally {
        await context.close();
      }
    }
    
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
  console.log(`Total viewports tested: ${VIEWPORTS.length}`);
  const withOverlaps = results.viewports.filter(v => v.hasOverlaps).length;
  const fullyVisible = results.viewports.filter(v => 
    v.visibility && Object.values(v.visibility).every(v => v)
  ).length;
  
  console.log(`Viewports with overlaps: ${withOverlaps}`);
  console.log(`Viewports with all elements visible: ${fullyVisible}`);
  console.log(`\n📄 Report saved to: ${path.join(SCREENSHOT_DIR, 'report.html')}`);
  
  return results;
}

function generateHTMLReport(results) {
  const viewportHTML = results.viewports.map(vp => `
    <div class="viewport-section">
      <h3>${vp.name} (${vp.width}x${vp.height})</h3>
      ${vp.error ? `
        <div class="error">Error: ${vp.error}</div>
      ` : `
        <div class="screenshot">
          <img src="${vp.screenshot}" alt="${vp.name}" />
        </div>
        <div class="details">
          <h4>Overlaps: ${vp.hasOverlaps ? '❌ YES' : '✅ NONE'}</h4>
          ${vp.overlaps.length > 0 ? `
            <ul class="overlaps">
              ${vp.overlaps.map(o => `<li>${o}</li>`).join('')}
            </ul>
          ` : ''}
          <h4>Visibility:</h4>
          <ul class="visibility">
            ${Object.entries(vp.visibility || {}).map(([el, vis]) => 
              `<li>${el}: ${vis ? '✅' : '❌'}</li>`
            ).join('')}
          </ul>
        </div>
      `}
    </div>
  `).join('');
  
  return `
<!DOCTYPE html>
<html>
<head>
  <title>Responsive UI Test Report</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
      background: #f5f5f5;
    }
    .container {
      max-width: 1400px;
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
    .viewport-section {
      margin: 30px 0;
      padding: 20px;
      border: 1px solid #ddd;
      border-radius: 8px;
    }
    .viewport-section h3 {
      margin-top: 0;
      color: #6366f1;
    }
    .screenshot {
      margin: 20px 0;
      text-align: center;
      background: #f0f0f0;
      padding: 10px;
      border-radius: 8px;
    }
    .screenshot img {
      max-width: 100%;
      height: auto;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .details {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-top: 20px;
    }
    .error {
      background: #ffebee;
      color: #c62828;
      padding: 10px;
      border-radius: 4px;
      margin: 10px 0;
    }
    .overlaps {
      color: #f44336;
      list-style-type: none;
      padding-left: 0;
    }
    .overlaps li::before {
      content: "⚠️ ";
    }
    .visibility {
      list-style-type: none;
      padding-left: 0;
    }
    h4 {
      margin-top: 0;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Responsive UI Test Report</h1>
    <p>Generated: ${results.timestamp}</p>
    <p>URL: ${results.url}</p>
    ${viewportHTML}
  </div>
</body>
</html>
  `;
}

// Run the test
testResponsiveUI().catch(console.error);