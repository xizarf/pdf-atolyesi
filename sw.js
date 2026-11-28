// Önce internetten dener, bağlantı yoksa saklanan kopyayı verir.
const CACHE='pdf-atolyesi-9fe220efe3', FILES=['./','index.html','icon.png','manifest.webmanifest'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES.map(f=>new Request(f,{cache:'reload'})))).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n.startsWith('pdf-atolyesi-')&&n!==CACHE).map(n=>caches.delete(n)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{ const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin) return;
  e.respondWith(fetch(u.href,{cache:'no-cache'}).then(r=>{ if(r.ok){ const copy=r.clone(); caches.open(CACHE).then(c=>c.put(e.request,copy)); } return r; })
    .catch(()=>caches.match(e.request,{ignoreSearch:true}).then(r=>r||(e.request.mode==='navigate'?caches.match('index.html'):Response.error())))); });
