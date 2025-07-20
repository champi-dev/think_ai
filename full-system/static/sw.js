// Minimal Service Worker - No Caching
// This service worker only handles the install event for PWA functionality

self.addEventListener('install', (event) => {
    console.log('[Service Worker] Installing...');
    // Skip waiting to activate immediately
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Activated');
    // Take control of all pages immediately
    event.waitUntil(clients.claim());
});

// Handle fetch events but don't cache - just pass through
self.addEventListener('fetch', (event) => {
    // Simply fetch from network, no caching
    event.respondWith(fetch(event.request));
});