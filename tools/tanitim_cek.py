"""CI: tanıtım videosu için 1080x1920 ham ekran kayıtları (webm) + ilk kare PNG. Kullanım: tanitim_cek.py ÇIKIŞ ; CUZ=1,2,3 """
import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
W, H = 412, 732


def cek(c):
    with sync_playwright() as p:
        b = p.chromium.launch(args=ARGS)
        ctx = b.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1,
                            record_video_dir=os.path.join(out, 'v' + c), record_video_size={'width': 1080, 'height': 1920})
        pg = ctx.new_page()
        pg.on('console', lambda m: print('console:', m.text[:160]) if 'error' in m.type else None)
        pg.goto('http://localhost:8765/?c=' + c)
        time.sleep(18)
        pg.screenshot(path=os.path.join(out, 'c%s_ilk.png' % c), timeout=120000)
        # yavaş sola-sağa bak
        x = 300
        pg.mouse.move(x, 300); pg.mouse.down()
        for i in range(10):
            x -= 20; pg.mouse.move(x, 300, steps=6); time.sleep(0.25)
        pg.mouse.up(); time.sleep(1.5)
        x = 100
        pg.mouse.move(x, 300); pg.mouse.down()
        for i in range(16):
            x += 15; pg.mouse.move(x, 300, steps=6); time.sleep(0.25)
        pg.mouse.up(); time.sleep(1.5)
        # ileri yürü
        pg.mouse.click(W // 2, 600); time.sleep(7)
        pg.screenshot(path=os.path.join(out, 'c%s_son.png' % c), timeout=120000)
        ctx.close(); b.close()


for c in os.environ.get('CUZ', '1').split(','):
    try: cek(c)
    except Exception as e: print('HATA', c, str(e)[:300])
