/* L'école à la maison : copie hors ligne.
   À CHAQUE MISE À JOUR de index.html, change le numéro de VERSION ci-dessous. */
const VERSION = 'v3.1';
const CACHE = 'ecole-maison-' + VERSION;
const FICHIERS = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './icon-512.png', './apple-touch-icon.png'];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FICHIERS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(cles => Promise.all(cles.filter(k => k.startsWith('ecole-maison-') && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  // Police Google : copie locale, rafraîchie en arrière-plan
  if (url.hostname.endsWith('googleapis.com') || url.hostname.endsWith('gstatic.com')) {
    e.respondWith(caches.open(CACHE).then(async c => {
      const copie = await c.match(req);
      const reseau = fetch(req).then(r => { c.put(req, r.clone()); return r; }).catch(() => copie);
      return copie || reseau;
    }));
    return;
  }
  if (url.origin !== location.origin) return;
  // Page de l'appli : réseau d'abord (pour avoir la dernière version), copie si hors ligne
  if (req.mode === 'navigate') {
    e.respondWith(fetch(req).then(r => { const k = r.clone(); caches.open(CACHE).then(c => c.put('./index.html', k)); return r; })
      .catch(() => caches.match('./index.html')));
    return;
  }
  e.respondWith(caches.match(req).then(r => r || fetch(req)));
});
