// Service Worker for Everfresh PWA
const CACHE_NAME = 'everfresh-v1';

// Install event
self.addEventListener('install', (event) => {
  self.skipWaiting();
});

// Activate event
self.addEventListener('activate', (event) => {
  event.waitUntil(clients.claim());
});

// Push notification received
self.addEventListener('push', (event) => {
  const data = event.data ? event.data.json() : {};

  const options = {
    body: data.body || 'New prices available!',
    icon: 'logo.png',
    badge: 'logo.png',
    vibrate: [200, 100, 200],
    data: {
      url: data.url || '/Pricelist/order.html'
    },
    actions: [
      {
        action: 'order',
        title: '📦 Order Now'
      },
      {
        action: 'call',
        title: '📞 Call'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification(data.title || '🥬 Everfresh', options)
  );
});

// Notification click handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'order') {
    event.waitUntil(clients.openWindow(event.notification.data.url));
  } else if (event.action === 'call') {
    event.waitUntil(clients.openWindow('tel:+61412345678'));
  } else {
    event.waitUntil(clients.openWindow(event.notification.data.url));
  }
});
