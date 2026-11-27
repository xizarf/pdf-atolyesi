from playwright.sync_api import sync_playwright
html='''<html><body style="margin:0;width:1200px;height:630px;background:#000;color:#fff;font-family:Inter,system-ui,sans-serif;overflow:hidden;position:relative">
<div style="position:absolute;width:560px;height:560px;border-radius:50%;background:#fff;right:-130px;bottom:-250px"></div>
<div style="position:absolute;width:110px;height:110px;border-radius:50%;background:#fff;right:520px;bottom:60px"></div>
<div style="position:absolute;right:190px;bottom:120px;width:430px;height:130px;border-radius:99px;background:rgba(255,255,255,.1);backdrop-filter:blur(10px);border:1.5px solid rgba(255,255,255,.4);box-shadow:inset 2px 2px 1px -1px #fff,inset -2px -2px 1px -1px #fff,0 20px 40px rgba(0,0,0,.4)"></div>
<div style="position:absolute;left:80px;top:80px;font-size:34px;font-weight:700">PDF Atölyesi</div>
<div style="position:absolute;left:76px;top:170px;font-size:112px;font-weight:800;letter-spacing:-.045em;line-height:1">Çek. Kırp.<br>PDF hazır.</div>
<div style="position:absolute;left:80px;top:440px;font-size:30px;line-height:1.5">Sayfa tara, yanlışlarını tekrar et,<br>programını takip et.</div></body></html>'''
with sync_playwright() as p:
    pg=p.chromium.launch().new_page(viewport={'width':1200,'height':630}); pg.set_content(html); pg.screenshot(path='assets/og.png')
