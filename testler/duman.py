# Hızlı kontrol: siteyi derle (python3 build.py), sonra proje klasöründe: python3 testler/duman.py
# Gerekenler: Pillow ve Playwright (Chromium). Deneme görseli burada üretilir.
import os,subprocess,sys,tempfile,time
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
tmp=tempfile.mkdtemp(); img=os.path.join(tmp,'sayfa.png')
im=Image.new('RGB',(900,1200),'white'); d=ImageDraw.Draw(im)
for y in range(120,1080,48): d.rectangle((90,y,810,y+14),fill='black')
im.save(img)
srv=subprocess.Popen([sys.executable,'-m','http.server','8790','-d','site'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        pg=p.chromium.launch().new_context(accept_downloads=True,viewport={'width':390,'height':780}).new_page()
        errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto('http://localhost:8790/'); pg.wait_for_timeout(2500)
        for t in (8,0,3,1,2,4,6,5,7):
            pg.click(f'#tab{t}'); pg.wait_for_timeout(200); assert pg.is_visible(f'#panel{t}'),t
            assert pg.evaluate('document.documentElement.scrollWidth<=innerWidth'),f'taşma: {t}'
        pg.click('#tab0'); pg.set_input_files('#file',img); pg.wait_for_selector('#grid .item'); pg.wait_for_timeout(800)
        pg.click('#make'); pg.wait_for_selector('#saver:not([hidden])',timeout=60000)
        with pg.expect_download() as dl: pg.click('#sgo')
        out=os.path.join(tmp,'cikti.pdf'); dl.value.save_as(out); assert open(out,'rb').read(5)==b'%PDF-'
        assert not errs,errs
    print('TAMAM: sekmeler açılıyor, görüntüden PDF oluşuyor')
finally: srv.terminate()
