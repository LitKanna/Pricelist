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

  const urlToOpen = event.notification.data?.url || '/Pricelist/order.html';

  event.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then((windowClients) => {
      // Check if app is already open
      for (let client of windowClients) {
        if (client.url.includes('Pricelist') && 'focus' in client) {
          client.navigate(urlToOpen);
          return client.focus();
        }
      }
      // Open new window
      return clients.openWindow(urlToOpen);
    })
  );
});
