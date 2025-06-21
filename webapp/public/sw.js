if (!self.define) {
  let e,
    s = {};
  const n = (n, c) => (
    (n = new URL(n + '.js', c).href),
    s[n] ||
      new Promise((s) => {
        if ('document' in self) {
          const e = document.createElement('script');
          (e.src = n), (e.onload = s), document.head.appendChild(e);
        } else (e = n), importScripts(n), s();
      }).then(() => {
        let e = s[n];
        if (!e) throw new Error(`Module ${n} didn’t register its module`);
        return e;
      })
  );
  self.define = (c, i) => {
    const a =
      e ||
      ('document' in self ? document.currentScript.src : '') ||
      location.href;
    if (s[a]) return;
    let t = {};
    const o = (e) => n(e, a),
      r = { module: { uri: a }, exports: t, require: o };
    s[a] = Promise.all(c.map((e) => r[e] || o(e))).then((e) => (i(...e), t));
  };
}
define(['./workbox-00a24876'], function (e) {
  'use strict';
  importScripts(),
    self.skipWaiting(),
    e.clientsClaim(),
    e.precacheAndRoute(
      [
        {
          url: '/_next/static/chunks/64-29178f792c1349ed.js',
          revision: '29178f792c1349ed',
        },
        {
          url: '/_next/static/chunks/91794568-17f676f22a1bb214.js',
          revision: '17f676f22a1bb214',
        },
        {
          url: '/_next/static/chunks/fb7d5399-a128ad8cbed3d85b.js',
          revision: 'a128ad8cbed3d85b',
        },
        {
          url: '/_next/static/chunks/framework-d6a7e6115aefd05a.js',
          revision: 'd6a7e6115aefd05a',
        },
        {
          url: '/_next/static/chunks/main-fa3f92bff0a5a566.js',
          revision: 'fa3f92bff0a5a566',
        },
        {
          url: '/_next/static/chunks/pages/_app-46c76043e4379e98.js',
          revision: '46c76043e4379e98',
        },
        {
          url: '/_next/static/chunks/pages/_error-ee5b5fb91d29d86f.js',
          revision: 'ee5b5fb91d29d86f',
        },
        {
          url: '/_next/static/chunks/pages/index-37cb7c034f5a96b4.js',
          revision: '37cb7c034f5a96b4',
        },
        {
          url: '/_next/static/chunks/pages/websocket-test-dd5f36fdc0f51803.js',
          revision: 'dd5f36fdc0f51803',
        },
        {
          url: '/_next/static/chunks/polyfills-c67a75d1b6f99dc8.js',
          revision: '837c0df77fd5009c9e46d446188ecfd0',
        },
        {
          url: '/_next/static/chunks/webpack-ee7e63bc15b31913.js',
          revision: 'ee7e63bc15b31913',
        },
        {
          url: '/_next/static/css/b12ac5fb7820280d.css',
          revision: 'b12ac5fb7820280d',
        },
        {
          url: '/_next/static/d6hAkjamjeDWMJCsFWw6U/_buildManifest.js',
          revision: 'c4b840e2816a50f0a7d6e48f592cb822',
        },
        {
          url: '/_next/static/d6hAkjamjeDWMJCsFWw6U/_ssgManifest.js',
          revision: 'b6652df95db52feb4daf4eca35380933',
        },
        {
          url: '/icons/icon-128x128.png',
          revision: 'aba3757f250e48b3be1806900a7f9b9e',
        },
        {
          url: '/icons/icon-144x144.png',
          revision: 'a54e82f370cb49194295e00593c5d6b7',
        },
        {
          url: '/icons/icon-152x152.png',
          revision: '90c9c39e4e342032102f4a471506165d',
        },
        {
          url: '/icons/icon-16x16.png',
          revision: '7c5156eb0ca6547d7adbaf518a3a5fdf',
        },
        {
          url: '/icons/icon-192x192.png',
          revision: '88ba9b9573a782f2c413ee478bbcaa58',
        },
        {
          url: '/icons/icon-32x32.png',
          revision: 'eec6811107a4fcd103b8da3a6260adb3',
        },
        {
          url: '/icons/icon-384x384.png',
          revision: '6b405463798e6ea2803ccc2b9f3d6b34',
        },
        {
          url: '/icons/icon-512x512.png',
          revision: '4acc5e5044e947fef67617487e29c4f5',
        },
        {
          url: '/icons/icon-72x72.png',
          revision: '5488f850f1280078893a69e14b2b16cf',
        },
        {
          url: '/icons/icon-96x96.png',
          revision: '1ee64e3ea3c2fe76eb9ef55e4e39af6c',
        },
        { url: '/manifest.json', revision: '3925234fac47a06dce6e5151c37196e4' },
      ],
      { ignoreURLParametersMatching: [] }
    ),
    e.cleanupOutdatedCaches(),
    e.registerRoute(
      '/',
      new e.NetworkFirst({
        cacheName: 'start-url',
        plugins: [
          {
            cacheWillUpdate: async ({
              request: e,
              response: s,
              event: n,
              state: c,
            }) =>
              s && 'opaqueredirect' === s.type
                ? new Response(s.body, {
                    status: 200,
                    statusText: 'OK',
                    headers: s.headers,
                  })
                : s,
          },
        ],
      }),
      'GET'
    ),
    e.registerRoute(
      /^https:\/\/fonts\.googleapis\.com\/.*/i,
      new e.CacheFirst({
        cacheName: 'google-fonts',
        plugins: [
          new e.ExpirationPlugin({ maxEntries: 10, maxAgeSeconds: 31536e3 }),
        ],
      }),
      'GET'
    ),
    e.registerRoute(
      /^https:\/\/fonts\.gstatic\.com\/.*/i,
      new e.CacheFirst({
        cacheName: 'gstatic-fonts',
        plugins: [
          new e.ExpirationPlugin({ maxEntries: 10, maxAgeSeconds: 31536e3 }),
        ],
      }),
      'GET'
    ),
    e.registerRoute(
      /^\/api\/.*/i,
      new e.NetworkFirst({
        cacheName: 'api-cache',
        networkTimeoutSeconds: 10,
        plugins: [
          new e.ExpirationPlugin({ maxEntries: 16, maxAgeSeconds: 60 }),
        ],
      }),
      'GET'
    ),
    e.registerRoute(
      /\.(?:jpg|jpeg|gif|png|svg|ico|webp)$/i,
      new e.StaleWhileRevalidate({
        cacheName: 'static-images',
        plugins: [
          new e.ExpirationPlugin({ maxEntries: 64, maxAgeSeconds: 2592e3 }),
        ],
      }),
      'GET'
    ),
    e.registerRoute(
      /\.(?:js|css)$/i,
      new e.StaleWhileRevalidate({
        cacheName: 'static-resources',
        plugins: [
          new e.ExpirationPlugin({ maxEntries: 32, maxAgeSeconds: 86400 }),
        ],
      }),
      'GET'
    );
});
