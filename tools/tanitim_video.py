"""CI (geçici): tanıtım videosu için uygulamanın web sürümünü gezdirir; gerçek zamanlı video + ara görüntüler. Kullanım: tanitim_video.py ÇIKIŞ"""
import os, sys, time, json, glob, subprocess
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
W, H = 412, 893
K = W / 1080.0  # telefon pikseli -> görünüm pikseli


def pt(x, y): return (x * K, y * K)


INIT = """
localStorage.setItem('flutter.hd_tur_ana','true');
localStorage.setItem('flutter.hd_tur_cuz','true');
localStorage.setItem('flutter.hd_namaz_v1', JSON.stringify(JSON.stringify({lat:41.0082,lon:28.9784,ad:'İstanbul'})));
localStorage.setItem('flutter.hd_ezber_v1', JSON.stringify(JSON.stringify([{t:'ayet',c:0,p:0,s:3,a1:101,a2:101}])));
"""


def sahne(ad, url, adimlar):
    d = os.path.join(out, ad); os.makedirs(d, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=ARGS)
        ctx = b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=2, has_touch=False,
                            record_video_dir=d, record_video_size={'width': 824, 'height': 1786})
        ctx.add_init_script(INIT)
        pg = ctx.new_page()
        pg.on('console', lambda m: print(ad, 'console:', m.text[:160]) if m.type == 'error' else None)
        pg.goto(url)
        n = [0]
        def sh(bekle=0.5, ad2=None):
            time.sleep(bekle)
            pg.screenshot(path=os.path.join(d, (ad2 or 's%02d' % n[0]) + '.png'), timeout=120000); n[0] += 1
        def tikla(x, y, bekle=1.5):
            pg.mouse.click(*pt(x, y)); time.sleep(bekle)
        def surukle(x0, y0, x1, y1, adim=14, bekle=1.0):
            a = pt(x0, y0); z = pt(x1, y1)
            pg.mouse.move(*a); pg.mouse.down()
            for i in range(1, adim + 1):
                pg.mouse.move(a[0] + (z[0] - a[0]) * i / adim, a[1] + (z[1] - a[1]) * i / adim, steps=2); time.sleep(0.03)
            pg.mouse.up(); time.sleep(bekle)
        def basili(x, y, sn=1.2):
            pg.mouse.move(*pt(x, y)); pg.mouse.down(); time.sleep(sn); pg.mouse.up(); time.sleep(1.2)
        try:
            time.sleep(14)
            adimlar(pg, sh, tikla, surukle, basili)
        except Exception as e:
            print('HATA', ad, str(e)[:300])
        ctx.close(); b.close()
    for w in glob.glob(os.path.join(d, '*.webm')):
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', w, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', os.path.join(out, ad + '.mp4')])
        os.remove(w)


# 1) ana ekran + sekmeler
def a_ana(pg, sh, tikla, surukle, basili):
    sh(4, 'ana')
    tikla(270, 2210, 3); sh(2, 'cuzler')
    tikla(450, 2210, 3); sh(2, 'ezberlerim')
    tikla(630, 2210, 3); sh(3, 'namaz')
    surukle(540, 1700, 540, 900, bekle=2); sh(2, 'namaz2')
    tikla(810, 2210, 3); sh(2, 'merasim')
    tikla(990, 2210, 3); sh(2, 'ayarlar')
    surukle(540, 1700, 540, 600, bekle=2); sh(2, 'ayarlar2')


# 2) 4. cüz bahçesi: yürü, bak, ağaca git
def a_bahce(pg, sh, tikla, surukle, basili):
    sh(3, 'b0')
    surukle(800, 1200, 300, 1200, bekle=2); sh(1, 'b1')
    surukle(300, 1200, 800, 1200, bekle=2); sh(1, 'b2')
    tikla(540, 1700, 5); sh(1, 'b3')
    tikla(540, 1500, 5); sh(1, 'b4')
    tikla(540, 1250, 6); sh(1, 'b5')
    tikla(540, 1250, 6); sh(1, 'b6')
    sh(4, 'b7')


sahne('ana', 'http://localhost:8765/', a_ana)
sahne('bahce', 'http://localhost:8765/?c=4', a_bahce)
