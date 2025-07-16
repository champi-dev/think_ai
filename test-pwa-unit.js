#!/usr/bin/env node
/**
 * Unit tests for PWA functionality
 * Tests service worker registration, manifest, and install button behavior
 */

const assert = require('assert');
const fs = require('fs');
const path = require('path');

console.log('🧪 Think AI PWA Unit Tests');
console.log('=========================\n');

let passedTests = 0;
let failedTests = 0;

function test(name, fn) {
    try {
        fn();
        console.log(`✅ ${name}`);
        passedTests++;
    } catch (error) {
        console.log(`❌ ${name}`);
        console.log(`   Error: ${error.message}`);
        failedTests++;
    }
}

// Test 1: Check manifest.json exists and is valid
test('Manifest file exists and is valid JSON', () => {
    const manifestPath = path.join(__dirname, 'static', 'manifest.json');
    assert(fs.existsSync(manifestPath), 'manifest.json should exist');
    
    const manifestContent = fs.readFileSync(manifestPath, 'utf8');
    const manifest = JSON.parse(manifestContent);
    
    // Check required fields
    assert(manifest.name, 'Manifest should have a name');
    assert(manifest.short_name, 'Manifest should have a short_name');
    assert(manifest.start_url, 'Manifest should have a start_url');
    assert(manifest.display, 'Manifest should have a display mode');
    assert(manifest.icons && manifest.icons.length > 0, 'Manifest should have icons');
});

// Test 2: Check service worker file exists
test('Service worker file exists', () => {
    const swPath = path.join(__dirname, 'static', 'sw.js');
    assert(fs.existsSync(swPath), 'sw.js should exist');
    
    const swContent = fs.readFileSync(swPath, 'utf8');
    assert(swContent.includes('install'), 'Service worker should handle install event');
    assert(swContent.includes('activate'), 'Service worker should handle activate event');
    assert(swContent.includes('fetch'), 'Service worker should handle fetch event');
});

// Test 3: Check PWA meta tags in index.html
test('Index.html contains PWA meta tags', () => {
    const indexPath = path.join(__dirname, 'static', 'index.html');
    assert(fs.existsSync(indexPath), 'index.html should exist');
    
    const indexContent = fs.readFileSync(indexPath, 'utf8');
    assert(indexContent.includes('manifest.json'), 'Should link to manifest.json');
    assert(indexContent.includes('theme-color'), 'Should have theme-color meta tag');
    assert(indexContent.includes('apple-mobile-web-app-capable'), 'Should have iOS meta tags');
});

// Test 4: Check install button exists
test('Install button exists in HTML', () => {
    const indexPath = path.join(__dirname, 'static', 'index.html');
    const indexContent = fs.readFileSync(indexPath, 'utf8');
    
    assert(indexContent.includes('pwaInstallButton'), 'Should have install button with ID');
    assert(indexContent.includes('Install App'), 'Should have install button text');
});

// Test 5: Check service worker registration code
test('Service worker registration code exists', () => {
    const indexPath = path.join(__dirname, 'static', 'index.html');
    const indexContent = fs.readFileSync(indexPath, 'utf8');
    
    assert(indexContent.includes('serviceWorker.register'), 'Should register service worker');
    assert(indexContent.includes('beforeinstallprompt'), 'Should handle install prompt');
});

// Test 6: Verify no caching in service worker
test('Service worker has no caching (as requested)', () => {
    const swPath = path.join(__dirname, 'static', 'sw.js');
    const swContent = fs.readFileSync(swPath, 'utf8');
    
    assert(!swContent.includes('caches.open'), 'Should not open caches');
    assert(!swContent.includes('cache.put'), 'Should not cache responses');
    assert(swContent.includes('fetch(event.request)'), 'Should pass through fetch requests');
});

// Test 7: Check icon files referenced in manifest
test('Icon files exist', () => {
    const manifestPath = path.join(__dirname, 'static', 'manifest.json');
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
    
    manifest.icons.forEach(icon => {
        const iconPath = path.join(__dirname, 'static', icon.src.replace('/', ''));
        assert(fs.existsSync(iconPath), `Icon ${icon.src} should exist`);
    });
});

// Test 8: Check PWA install button styling
test('PWA install button has proper styling', () => {
    const indexPath = path.join(__dirname, 'static', 'index.html');
    const indexContent = fs.readFileSync(indexPath, 'utf8');
    
    assert(indexContent.includes('.pwa-install-button'), 'Should have install button styles');
    assert(indexContent.includes('display: none'), 'Button should be hidden by default');
    assert(indexContent.includes('.show'), 'Should have show class for visibility');
});

// Summary
console.log('\n📊 Test Summary');
console.log('==============');
console.log(`✅ Passed: ${passedTests}`);
console.log(`❌ Failed: ${failedTests}`);
console.log(`📈 Success Rate: ${((passedTests / (passedTests + failedTests)) * 100).toFixed(1)}%`);

if (failedTests === 0) {
    console.log('\n🎉 All PWA unit tests passed!');
    process.exit(0);
} else {
    console.log('\n⚠️  Some tests failed. Please fix the issues above.');
    process.exit(1);
}