from PIL import Image, ImageDraw, ImageFont
import subprocess, shutil, os
os.makedirs('site',exist_ok=True)
# Alan adı değişirse yalnızca bu satır güncellenir.
SITE='https://xizarf.github.io/pdf-atolyesi/'
BASE='/'+SITE.split('/',3)[3]
ABOUT='Ders sayfalarını PDF’e çevir, yanlışlarını tekrar et, haftalık programını ve sınava hazırlığını takip et. Dosyaların cihazında işlenir.'
s=open('foy/index.html').read()
def rep(a,n):
    global s
    assert s.count(a)==1,a
    s=s.replace(a,n)
rep('<title>PDF Atölyesi</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n','')
# Claude dışında kaydetme: dosya hazır olunca kullanıcı dokunuşuyla paylaşılır veya indirilir.
rep("const dl = window.claude ? window.claude.use('downloads') : Promise.resolve(null);","const dl = Promise.resolve({save:saveFile});")
rep('<div id="editor" hidden>','''<div id="saver" hidden role="dialog" aria-modal="true" aria-labelledby="sname"><div class="glass">
<p id="sname"></p><button id="sgo" class="main">Kaydet</button><button id="sno">Kapat</button></div></div>
<div id="editor" hidden>''')
rep('</style>','''#saver{position:fixed;inset:0;z-index:30;display:flex;align-items:flex-end;justify-content:center;background:rgba(0,0,0,.4);padding:16px 12px calc(16px + env(safe-area-inset-bottom,0px))}
#saver>div{width:100%;max-width:480px;border-radius:34px;padding:18px 14px 8px;text-align:center;background:var(--solid)}
#sname{font-weight:600;overflow-wrap:anywhere;margin:0 0 14px}#sno{width:100%;padding:14px}
</style>''')
rep('// Beyaz sayfayı bulur.','''function saveFile({filename,data}){
  return new Promise((ok,no)=>{
    const types={pdf:'application/pdf',zip:'application/zip',json:'application/json'};
    const file=new File([data],filename,{type:types[filename.split('.').pop()]});
    const share=/iP(hone|ad|od)/.test(navigator.userAgent)||(navigator.platform==='MacIntel'&&navigator.maxTouchPoints>1);
    const el=id=>document.getElementById(id);
    el('sname').textContent=filename+' hazır'; el('saver').hidden=false;
    const done=()=>{ el('saver').hidden=true; };
    const download=()=>{ const url=URL.createObjectURL(file), a=document.createElement('a'); a.href=url; a.download=filename;
      document.body.appendChild(a); a.click(); a.remove(); setTimeout(()=>URL.revokeObjectURL(url),60000); done(); ok({status:'saved'}); };
    el('sgo').onclick=async()=>{
      if(share&&navigator.canShare&&navigator.canShare({files:[file]})){
        try{ await navigator.share({files:[file]}); done(); ok({status:'saved'}); }
        catch(e){ if(e.name!=='AbortError') download(); } // paylaşım iptalinde pencere açık kalır
      } else download();
    };
    el('sno').onclick=()=>{ done(); no({code:'declined'}); };
  });
}

// Beyaz sayfayı bulur.''')
head='''<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>PDF Atölyesi</title>
<meta name="description" content="@ABOUT@">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; media-src blob: data:; connect-src 'self' blob: data:; worker-src 'self'; object-src 'none'; base-uri 'none'; form-action 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">
<link rel="canonical" href="@SITE@">
<meta property="og:type" content="website">
<meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="PDF Atölyesi">
<meta property="og:title" content="PDF Atölyesi: sayfa tara, yanlışlarını tekrar et">
<meta property="og:description" content="@ABOUT@">
<meta property="og:url" content="@SITE@">
<meta property="og:image" content="@SITE@og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="apple-mobile-web-app-title" content="PDF Atölyesi">
<link rel="apple-touch-icon" href="icon.png">
<link rel="icon" href="icon.png">
<style>:root{color-scheme:light;padding:env(safe-area-inset-top,0px) 0 env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
<noscript><p style="padding:24px;font:17px system-ui">PDF Atölyesi’nin çalışması için tarayıcında JavaScript açık olmalı.</p></noscript>
'''
head=head.replace('@ABOUT@',ABOUT).replace('@SITE@',SITE)
open('site/index.html','w').write(head+s+'\n</body>\n</html>\n')
# simge: siyah zemin, beyaz belge. "maskable" olan kenar kırpılmasına karşı içeriği küçültür.
def icon(size,scale=1.0):
    im=Image.new('RGB',(512,512),'black'); d=ImageDraw.Draw(im)
    P=lambda x,y:(256+(x-256)*scale,256+(y-256)*scale)
    d.polygon([P(*p) for p in ((144,96),(296,96),(368,168),(368,416),(144,416))],fill='white'); d.polygon([P(*p) for p in ((296,96),(296,168),(368,168))],fill=(150,150,150))
    for y,w in ((232,160),(280,160),(328,104)): d.rounded_rectangle((*P(176,y),*P(176+w,y+20)),10*scale,fill='black')
    return im.resize((size,size),Image.LANCZOS)
icon(180).save('site/icon.png'); icon(192).save('site/icon-192.png'); icon(512).save('site/icon-512.png'); icon(512,.82).save('site/icon-maskable.png')
shutil.copyfile('assets/og.png','site/og.png')
# olmayan bir adrese gidilirse
open('site/404.html','w').write("""<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Sayfa bulunamadı · PDF Atölyesi</title><meta name="robots" content="noindex">
<style>:root{color-scheme:light dark}body{margin:0;min-height:100vh;display:grid;place-items:center;padding:24px;box-sizing:border-box;font:18px/1.5 -apple-system,BlinkMacSystemFont,Inter,system-ui,sans-serif;background:#fff;color:#000;text-align:center}h1{font-size:clamp(40px,12vw,76px);line-height:1;letter-spacing:-.04em;margin:0 0 16px}a{display:inline-block;margin-top:12px;padding:15px 28px;border-radius:99px;background:#000;color:#fff;font-weight:600;text-decoration:none}@media (prefers-color-scheme:dark){body{background:#000;color:#fff}a{background:#fff;color:#000}}</style></head>
<body><main><h1>Bu sayfa yok.</h1><p>Adres yanlış yazılmış veya sayfa kaldırılmış olabilir.</p><a href="%s">Ana sayfaya dön</a></main></body></html>
""" % BASE)

# Çevrimdışı kullanım (yalnızca bağımsız sitede)
import json, hashlib
page=open('site/index.html').read()
page=page.replace('<link rel="icon" href="icon.png">','<link rel="icon" href="icon.png">\n<link rel="manifest" href="manifest.webmanifest">')
reg="""<script>if('serviceWorker' in navigator) addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));</script>"""
page=page.replace('\n</body>\n</html>\n',reg+'\n</body>\n</html>\n')
open('site/index.html','w').write(page)
json.dump({"name":"PDF Atölyesi","short_name":"PDF Atölyesi","description":ABOUT,"lang":"tr","categories":["education","productivity"],"start_url":"./","scope":"./","display":"standalone","background_color":"#000000","theme_color":"#000000","icons":[{"src":"icon.png","sizes":"180x180","type":"image/png"},{"src":"icon-192.png","sizes":"192x192","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"},{"src":"icon-maskable.png","sizes":"512x512","type":"image/png","purpose":"maskable"}]},open('site/manifest.webmanifest','w'),ensure_ascii=False)
ver=hashlib.sha256(page.encode()).hexdigest()[:10]
open('site/sw.js','w').write("""// Önce internetten dener, bağlantı yoksa saklanan kopyayı verir.
const CACHE='pdf-atolyesi-%s', FILES=['./','index.html','icon.png','manifest.webmanifest'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES.map(f=>new Request(f,{cache:'reload'})))).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(n=>n.startsWith('pdf-atolyesi-')&&n!==CACHE).map(n=>caches.delete(n)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{ const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin) return;
  e.respondWith(fetch(u.href,{cache:'no-cache'}).then(r=>{ if(r.ok){ const copy=r.clone(); caches.open(CACHE).then(c=>c.put(e.request,copy)); } return r; })
    .catch(()=>caches.match(e.request,{ignoreSearch:true}).then(r=>r||(e.request.mode==='navigate'?caches.match('index.html'):Response.error())))); });
""" % ver)
