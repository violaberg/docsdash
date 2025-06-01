// Service Worker for DocsDash PWA

const CACHE_NAME = 'docsdash-cache-v1';
const urlsToCache = [
  '/',
  '/static/css/main.css',
  '/static/js/main.js',
  '/static/images/logo.png',
  '/static/offline.html',
];

// Install event - cache assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  const cacheWhitelist = [CACHE_NAME];
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheWhitelist.indexOf(cacheName) === -1) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        // Cache hit - return response
        if (response) {
          return response;
        }
        
        // Clone the request
        const fetchRequest = event.request.clone();
        
        return fetch(fetchRequest)
          .then(response => {
            // Check if valid response
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }
            
            // Clone the response
            const responseToCache = response.clone();
            
            // Cache the fetched response
            caches.open(CACHE_NAME)
              .then(cache => {
                cache.put(event.request, responseToCache);
              });
            
            return response;
          })
          .catch(error => {
            // Offline fallback
            if (event.request.mode === 'navigate') {
              return caches.match('/static/offline.html');
            }
          });
      })
  );
});

// Background sync for offline data
self.addEventListener('sync', event => {
  if (event.tag === 'sync-patients') {
    event.waitUntil(syncPatients());
  } else if (event.tag === 'sync-appointments') {
    event.waitUntil(syncAppointments());
  }
});

// Function to sync patient data
async function syncPatients() {
  const db = await openDatabase();
  const pendingPatients = await db.getAll('pending-patients');
  
  for (const patient of pendingPatients) {
    try {
      const response = await fetch('/api/patients/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(patient.data),
      });
      
      if (response.ok) {
        await db.delete('pending-patients', patient.id);
      }
    } catch (error) {
      console.error('Failed to sync patient:', error);
    }
  }
}

// Function to sync appointment data
async function syncAppointments() {
  const db = await openDatabase();
  const pendingAppointments = await db.getAll('pending-appointments');
  
  for (const appointment of pendingAppointments) {
    try {
      const response = await fetch('/api/appointments/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(appointment.data),
      });
      
      if (response.ok) {
        await db.delete('pending-appointments', appointment.id);
      }
    } catch (error) {
      console.error('Failed to sync appointment:', error);
    }
  }
}

// Function to open IndexedDB database
function openDatabase() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('docsdash-db', 1);
    
    request.onerror = () => reject(request.error);
    request.onsuccess = () => {
      const db = request.result;
      resolve({
        getAll: (storeName) => {
          return new Promise((resolve, reject) => {
            const transaction = db.transaction(storeName, 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.getAll();
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve(request.result);
          });
        },
        delete: (storeName, id) => {
          return new Promise((resolve, reject) => {
            const transaction = db.transaction(storeName, 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.delete(id);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve();
          });
        }
      });
    };
    
    request.onupgradeneeded = () => {
      const db = request.result;
      db.createObjectStore('pending-patients', { keyPath: 'id', autoIncrement: true });
      db.createObjectStore('pending-appointments', { keyPath: 'id', autoIncrement: true });
    };
  });
}

// Push notification event
self.addEventListener('push', event => {
  const data = event.data.json();
  
  const options = {
    body: data.body,
    icon: '/static/images/logo.png',
    badge: '/static/images/badge.png',
    data: {
      url: data.url
    }
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// Notification click event
self.addEventListener('notificationclick', event => {
  event.notification.close();
  
  if (event.notification.data && event.notification.data.url) {
    event.waitUntil(
      clients.openWindow(event.notification.data.url)
    );
  }
});