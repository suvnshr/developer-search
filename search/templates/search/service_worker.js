// Base Service Worker implementation.  To use your own Service Worker, set the PWA_SERVICE_WORKER_PATH variable in settings.py

var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/offline/',

    // CSS
    '/static/css/django-pwa-app.css',
    '/static/index.min.css/',
    '/static/light-variables.min.css/',
    '/static/dark-variables.min.css/',

    // JS
    '/static/index.min.js',

    // Logo
    '/static/logo.png',
    '/static/short-logo.png',

    // Android Icons
    '/static/icons/android-icon-36x36.png',
    '/static/icons/android-icon-48x48.png',
    '/static/icons/android-icon-72x72.png',
    '/static/icons/android-icon-96x96.png',
    '/static/icons/android-icon-144x144.png',
    '/static/icons/android-icon-192x192.png',

    //  Apple Icons
    '/static/icons/apple-icon-57x57.png',
    '/static/icons/apple-icon-60x60.png',
    '/static/icons/apple-icon-72x72.png',
    '/static/icons/apple-icon-76x76.png',
    '/static/icons/apple-icon-114x114.png',
    '/static/icons/apple-icon-120x120.png',
    '/static/icons/apple-icon-144x144.png',
    '/static/icons/apple-icon-152x152.png',
    '/static/icons/apple-icon-180x180.png',
];

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
            .catch(err => {
                console.log(`Error: Can't open files to be cached. ${err}`)
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames
                    .filter(cacheName => (cacheName.startsWith("django-pwa-")))
                    .filter(cacheName => (cacheName !== staticCacheName))
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/offline/');
            })
    )
});
