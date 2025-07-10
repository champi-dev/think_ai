// Think AI Service Worker with intelligent cache management
const CACHE_VERSION = 'think-ai-v1.0.0';
const CACHE_NAME = `${CACHE_VERSION}-${new Date().getTime()}`;
const OFFLINE_URL = '/offline.html';

// Resources to cache immediately
const STATIC_CACHE = [
  '/',
  '/offline.html',
  '/manifest.json',
  '/favicon.ico',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// Dynamic cache for API responses
const API_CACHE_NAME = 'think-ai-api-v1';
const API_CACHE_DURATION = 5 * 60 * 1000; // 5 minutes

// Install event - cache static resources
self.addEventListener('install', (event) => {
  console.log('[SW] Installing service worker...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[SW] Caching static resources');
      return cache.addAll(STATIC_CACHE.map(url => new Request(url, {cache: 'reload'})));
    }).then(() => {
      console.log('[SW] Service worker installed');
      return self.skipWaiting();
    })
  );
});

// Activate event - clean old caches
self.addEventListener('activate', (event) => {
  console.log('[SW] Activating service worker...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          // Delete old version caches
          if (cacheName.startsWith('think-ai-v') && cacheName !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
          // Clean old API caches
          if (cacheName === API_CACHE_NAME) {
            return cleanExpiredApiCache();
          }
        })
      );
    }).then(() => {
      console.log('[SW] Service worker activated');
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache when offline
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-HTTP requests
  if (!url.protocol.startsWith('http')) {
    return;
  }

  // Handle API requests with intelligent caching
  if (url.pathname.startsWith('/api/') || url.pathname.startsWith('/chat')) {
    event.respondWith(handleApiRequest(request));
    return;
  }

  // Handle static resources with cache-first strategy
  event.respondWith(
    caches.match(request).then((cachedResponse) => {
      if (cachedResponse) {
        // Return cached version and update in background
        fetchAndUpdateCache(request);
        return cachedResponse;
      }

      // Not in cache, fetch from network
      return fetch(request).then((response) => {
        // Cache successful responses
        if (response && response.status === 200) {
          const responseToCache = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseToCache);
          });
        }
        return response;
      }).catch(() => {
        // Offline fallback for navigation requests
        if (request.mode === 'navigate') {
          return caches.match(OFFLINE_URL);
        }
        throw new Error('Network request failed');
      });
    })
  );
});

// Handle API requests with smart caching
async function handleApiRequest(request) {
  try {
    // Try network first for POST requests
    if (request.method === 'POST') {
      const response = await fetch(request);
      
      // Cache successful responses
      if (response && response.status === 200) {
        const responseToCache = response.clone();
        const cache = await caches.open(API_CACHE_NAME);
        const cacheKey = await createApiCacheKey(request);
        
        // Store with timestamp
        const cacheData = {
          timestamp: Date.now(),
          response: await responseToCache.text()
        };
        
        const cacheResponse = new Response(JSON.stringify(cacheData), {
          headers: { 'Content-Type': 'application/json' }
        });
        
        await cache.put(cacheKey, cacheResponse);
      }
      
      return response;
    }
    
    // For GET requests, try cache first
    const cachedResponse = await getCachedApiResponse(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Fetch from network
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