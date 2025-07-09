// Think AI Service Worker with intelligent cache management
//
// # What's a Service Worker?
// Imagine a smart assistant that sits between your app and the internet.
// When you ask for something, it checks:
// 1. "Do I have this saved?" (cache)
// 2. "Should I get a fresh copy?" (network)
// 3. "What if the internet is down?" (offline fallback)
//
// # Why This Makes Apps Fast
// Instead of downloading the same image 100 times, we save it once!
// Like keeping snacks in your desk drawer instead of going to the store every time.

const CACHE_VERSION = 'think-ai-v1.0.0';
// Unique cache name with timestamp - ensures old caches are replaced
// Like labeling leftovers with the date so you know what's fresh
const CACHE_NAME = `${CACHE_VERSION}-${new Date().getTime()}`;
const OFFLINE_URL = '/offline.html';

// Resources to cache immediately (the essentials)
// Like packing an emergency kit - these files MUST work offline
const STATIC_CACHE = [
  '/',                      // Homepage
  '/offline.html',          // What to show when offline
  '/manifest.json',         // App configuration
  '/favicon.ico',          // Browser tab icon
  '/icons/icon-192x192.png', // Small app icon
  '/icons/icon-512x512.png'  // Large app icon
];

// Dynamic cache for API responses
// Like a notepad where we write down answers to avoid asking twice
const API_CACHE_NAME = 'think-ai-api-v1';
const API_CACHE_DURATION = 5 * 60 * 1000; // 5 minutes (fresh enough!)

// Install event - cache static resources
// 
// # The Moving Day
// When the service worker first arrives (installs), it:
// 1. Opens a storage box (cache)
// 2. Downloads and saves essential files
// 3. Gets ready to serve immediately
//
// Like moving into a new apartment and stocking the kitchen first!
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  
  // event.waitUntil = "Don't finish installing until this is done"
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Caching static resources');
      // Force fresh downloads with {cache: 'reload'}
      // Like insisting on fresh groceries, not yesterday's
      return cache.addAll(STATIC_CACHE.map(url => new Request(url, {cache: 'reload'})));
    }).then(() => {
      console.log('[SW] Service worker installed');
      // skipWaiting = "Start using me right away, don't wait!"
      return self.skipWaiting();
    })
  );
});

// Activate event - clean old caches
//
// # Spring Cleaning Time!
// When a new service worker takes over (activates), it:
// 1. Looks at all storage boxes (caches)
// 2. Throws away old versions
// 3. Cleans expired API responses
// 4. Takes control of all tabs
//
// Like a new janitor who first cleans out old supplies!
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  
  event.waitUntil(
    // Get list of all cache names (like checking all storage boxes)
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          // Delete old version caches
          // If it starts with 'think-ai-v' but isn't current = OLD
          if (cacheName.startsWith('think-ai-v') && cacheName !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
          // Clean expired items from API cache
          // Like throwing away expired milk
          if (cacheName === API_CACHE_NAME) {
            return cleanExpiredApiCache();
          }
        })
      );
    }).then(() => {
      console.log('[SW] Service worker activated');
      // clients.claim = "I'm in charge of all tabs now!"
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache when offline
//
// # The Smart Waiter
// Every time the app asks for something (fetch), our waiter:
// 1. Checks what type of order it is (API? Image? Page?)
// 2. Decides the best way to serve it
// 3. Always has a backup plan if the kitchen (internet) is closed
//
// This is where the O(1) magic happens - instant cache lookups!
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-HTTP requests (like chrome-extension://)
  // We only handle web requests, not browser internals
  if (!url.protocol.startsWith('http')) {
    return;
  }

  // API requests: Smart caching with expiration
  // Like keeping meeting notes - useful for a while, then outdated
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/chat')) {
    event.respondWith(handleApiRequest(request));
    return;
  }

  // Static resources: Cache-first strategy
  // Like keeping a spare key - check your pocket before going to the locksmith
  event.respondWith(
    // Step 1: Check cache (O(1) lookup!)
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        // Found it! Serve from cache = instant
        // Also update cache in background for next time
        fetchAndUpdateCache(request);
        return cachedResponse;
      }

      // Step 2: Not cached? Get from network
      return fetch(request).then((response) => {
        // Only cache successful responses (status 200)
        // Don't cache errors - that would be embarrassing!
        if (response && response.status === 200) {
          // Clone because responses can only be read once
          // Like making a photocopy before filing the original
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseToCache);
          });
        }
        return response;
      }).catch(() => {
        // Step 3: Network failed? Show offline page
        // Better than Chrome's dinosaur!
        if (request.mode === 'navigate') {
          return caches.match(OFFLINE_URL);
        }
        throw new Error('Network request failed');
      });
    })
  );
});

// Handle API requests with smart caching
//
// # The Smart Restaurant Order System
// This function is like a restaurant that remembers your favorite orders:
// - POST requests (new orders): Always make fresh, but remember for next time
// - GET requests (asking for menu): Check if we have a recent copy first
// - Offline mode: Serve the last thing you ordered
//
// The O(1) trick: We hash the request to instantly find cached responses!
async function handleApiRequest(request) {
  try {
    // POST = "I want to order something new"
    // Always go to the kitchen (network) for fresh food
    if (request.method === 'POST') {
      const response = await fetch(request);
      
      // If the order was successful, remember it for later
      if (response && response.status === 200) {
        // Clone the response (can't eat the same sandwich twice!)
        const responseToCache = response.clone();
        const cache = await caches.open(API_CACHE_NAME);
        
        // Create unique recipe card for this exact order
        const cacheKey = await createApiCacheKey(request);
        
        // Write down when we made it (for freshness checking)
        const cacheData = {
          timestamp: Date.now(),              // When we cooked it
          response: await responseToCache.text() // What we cooked
        };
        
        // Package it nicely for storage
        const cacheResponse = new Response(JSON.stringify(cacheData), {
          headers: { 'Content-Type': 'application/json' }
        });
        
        // Store in our recipe book (O(1) storage!)
        await cache.put(cacheKey, cacheResponse);
      }
      
      return response;
    }
    
    // GET = "What's on the menu?" or "I'll have the usual"
    // Check our recipe book first (O(1) lookup!)
    const cachedResponse = await getCachedApiResponse(request);
    if (cachedResponse) {
      return cachedResponse;  // Found it! Instant service!
    }
    
    // Not in recipe book? Ask the kitchen
    const response = await fetch(request);
    return response;
    
  } catch (error) {
    // Try to return cached response when offline
    const cachedResponse = await getCachedApiResponse(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline response
    return new Response(JSON.stringify({
      error: 'Offline',
      message: 'Think AI is currently offline. Cached responses are being used.',
      cached: true
    }), {
      status: 503,
      headers: { 'Content-Type': 'application/json' }
    });
  }
}

// Create cache key for API requests
async function createApiCacheKey(request) {
  if (request.method === 'POST') {
    const body = await request.clone().text();
    return new Request(`${request.url}#${hashString(body)}`);
  }
  return request;
}

// Get cached API response if not expired
async function getCachedApiResponse(request) {
  const cache = await caches.open(API_CACHE_NAME);
  const cacheKey = await createApiCacheKey(request);
  const cachedResponse = await cache.match(cacheKey);
  
  if (!cachedResponse) {
    return null;
  }
  
  const cacheData = await cachedResponse.json();
  const age = Date.now() - cacheData.timestamp;
  
  if (age > API_CACHE_DURATION) {
    // Cache expired
    await cache.delete(cacheKey);
    return null;
  }
  
  // Return cached response
  return new Response(cacheData.response, {
    headers: {
      'Content-Type': 'application/json',
      'X-Cache': 'HIT',
      'X-Cache-Age': age.toString()
    }
  });
}

// Clean expired API cache entries
async function cleanExpiredApiCache() {
  const cache = await caches.open(API_CACHE_NAME);
  const requests = await cache.keys();
  
  for (const request of requests) {
    const response = await cache.match(request);
    if (response) {
      try {
        const cacheData = await response.json();
        const age = Date.now() - cacheData.timestamp;
        if (age > API_CACHE_DURATION) {
          await cache.delete(request);
        }
      } catch (e) {
        // Invalid cache entry, delete it
        await cache.delete(request);
      }
    }
  }
}

// Update cache in background
function fetchAndUpdateCache(request) {
  fetch(request).then((response) => {
    if (response && response.status === 200) {
      caches.open(CACHE_NAME).then((cache) => {
        cache.put(request, response);
      });
    }
  }).catch(() => {
    // Silently fail background updates
  });
}

// Simple string hash for cache keys
function hashString(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return hash.toString(36);
}

// Listen for messages from the app
self.addEventListener('message', (event) => {
  if (event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => caches.delete(cacheName))
        );
      }).then(() => {
        return self.clients.matchAll();
      }).then((clients) => {
        clients.forEach(client => {
          client.postMessage({
            type: 'CACHE_CLEARED',
            message: 'All caches have been cleared'
          });
        });
      })
    );
  }
});