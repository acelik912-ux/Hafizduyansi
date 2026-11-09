"""CI: web uygulamasında otlak (8. cüz) sahnesinde dönüş + yürüme karelerini çekip mp4 yapar. Kullanım: ekran_video.py ÇIKIŞ"""
import os, subprocess, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']


def cek(mod, ad):
    kare = os.path.join(out, ad + '_kareler'); os.makedirs(kare, exist_ok=True)
    n = [0]
    with sync_playwright() as p:
        b = p.chromium.launch(args=ARGS)
        pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=2)
        pg.on('console', lambda m: print('console:', m.text[:200]) if 'error' in m.type else None)
        pg.goto('http://localhost:8765/?c=' + os.environ.get('CUZ1','8') + ('&eski=1' if mod == 'eski' else ''))
        time.sleep(16)

        def kaydet(bekle=0.35):
            time.sleep(bekle)
            pg.screenshot(path=os.path.join(kare, '%04d.png' % n[0])); n[0] += 1

        kaydet(1.0)
        pg.screenshot(path=os.path.join(out, ad + '_ilk.png'))
        # 1) sağa/sola dön: 40 px ≈ 6° ; yarım tur
        for tur in range(4):
            x = 380
            pg.mouse.move(x, 300); pg.mouse.down()
            for i in range(6):
                x -= 50
                pg.mouse.move(x, 300, steps=4); kaydet(0.25)
            pg.mouse.up(); time.sleep(0.2)
        # 2) yürü: yere dokun
        pg.mouse.click(206, 700)
        for i in range(24):
            kaydet(0.3)
        pg.screenshot(path=os.path.join(out, ad + '_son.png'))
        b.close()
    subprocess.run(['ffmpeg', '-y', '-framerate', '6', '-i', os.path.join(kare, '%04d.png'), '-vf', 'scale=412:880', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', os.path.join(out, '%s.mp4' % ad)], check=False)


for c in os.environ.get('CUZ','4').split(','):
    os.environ['CUZ1']=c
    cek('yeni', 'c'+c)
