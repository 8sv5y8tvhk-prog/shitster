// Offline-Cache für die App-Hülle. Songs kommen immer live von Deezer.
const CACHE = 'shitster-v11';
const SHELL = [
  './',
  'index.html',
  'css/app.css',
  'js/app.js',
  'js/game.js',
  'js/audio.js',
  'js/deezer.js',
  'js/store.js',
  'data/categories.json',
  'data/deutschrap.json',
  'data/whitegirl.json',
  'data/dekaden.json',
  'data/rock.json',
  'data/edm.json',
  'assets/icon.svg',
  'assets/icon-180.png',
  'manifest.webmanifest',
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Network-first für eigene Dateien (Updates kommen sofort an), Cache als Fallback
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  if (e.request.method !== 'GET' || url.origin !== location.origin) return;
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, copy));
        return res;
      })
      .catch(() => caches.match(e.request, { ignoreSearch: true }))
  );
});
