/**
 * Service Worker - Karaoke Kenz PWA
 * Cung cấp khả năng tải tức thì, hoạt động Offline & trải nghiệm Native App
 */

const CACHE_NAME = 'kenz-pwa-v1';
const STATIC_ASSETS = [
  './',
  './index.html',
  './ktv-hanoi.html',
  './admin.html',
  './config.js',
  './manifest.webmanifest',
  './css/base.css',
  './css/components.css',
  './css/animations.css',
  './css/ktv.css',
  './css/responsive.css',
  './js/app.js',
  './js/booking.js',
  './js/i18n.js',
  './js/pwa-install.js',
  './assets/apple-touch-icon.png',
  './assets/icon-192x192.png',
  './assets/icon-512x512.png',
  './assets/logo.png',
  './assets/kenz-logo.png',
  './favicon.ico'
];

// 1. Cài đặt Service Worker và lưu Cache các tài nguyên cốt lõi
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('[PWA SW] Một số file tĩnh không cache được lúc install:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// 2. Kích hoạt và dọn dẹp các bản Cache cũ
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            console.log('[PWA SW] Đang dọn dẹp cache cũ:', name);
            return caches.delete(name);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Xử lý yêu cầu tài nguyên (Chiến lược: Network-First cho HTML/API, Stale-While-Revalidate cho CSS/JS/Ảnh)
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Bỏ qua các request không phải GET hoặc là request tới Telegram/Zalo API/Google Analytics
  if (req.method !== 'GET') return;
  if (url.origin !== self.location.origin) return;

  // Cho trang HTML: Network first, fallback to Cache
  if (req.mode === 'navigate' || req.headers.get('accept')?.includes('text/html')) {
    event.respondWith(
      fetch(req)
        .then((networkRes) => {
          const clone = networkRes.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          return networkRes;
        })
        .catch(() => {
          return caches.match(req).then((cached) => cached || caches.match('./index.html'));
        })
    );
    return;
  }

  // Cho CSS, JS, Fonts, Images: Stale-While-Revalidate (Lấy từ cache ra ngay, đồng thời tải bản mới ngầm)
  event.respondWith(
    caches.match(req).then((cachedRes) => {
      const fetchPromise = fetch(req).then((networkRes) => {
        if (networkRes && networkRes.status === 200) {
          const clone = networkRes.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
        }
        return networkRes;
      }).catch(() => {/* Offline */});

      return cachedRes || fetchPromise;
    })
  );
});
