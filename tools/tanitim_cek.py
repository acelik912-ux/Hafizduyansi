"""CI: tanıtım videosu için 1080x1918 sabit görüntüler (DSF 2.62). Kullanım: tanitim_cek.py ÇIKIŞ"""
import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
ARGS = ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl']
W, H = 412, 732


def acik(p, url):
    b = p.chromium.launch(args=ARGS)
    pg = b.new_page(viewport={'width': W, 'height': H}, device_scale_factor=2.62)
    pg.goto(url); time.sleep(18)
    return b, pg


def sh(pg, ad, bekle=1.0):
    time.sleep(bekle)
    pg.screenshot(path=os.path.join(out, ad + '.png'), timeout=180000)


def surukle(pg, x0, x1, y=300, adim=12):
    pg.mouse.move(x0, y); pg.mouse.down()
    for i in range(1, adim + 1):
        pg.mouse.move(x0 + (x1 - x0) * i / adim, y, steps=3)
    pg.mouse.up(); time.sleep(1.2)


def ana():
    with sync_playwright() as p:
        b, pg = acik(p, 'http://localhost:8765/')
        sh(pg, 'ana_bugun')
        pg.mouse.click(68, 714); sh(pg, 'ana_cuzler', 2)
        pg.mouse.click(339, 714); sh(pg, 'ana_ayarlar', 2)
        b.close()
    for ad, (x, y) in (('mushaf', (204, 414)), ('ezber', (333, 414))):
        with sync_playwright() as p:
            b, pg = acik(p, 'http://localhost:8765/')
            pg.mouse.click(x, y); sh(pg, 'ana_' + ad + '_1', 3)
            sh(pg, 'ana_' + ad + '_2', 4)
            b.close()


def cuz(c):
    with sync_playwright() as p:
        b, pg = acik(p, 'http://localhost:8765/?c=' + c)
        sh(pg, 'c%s_a' % c)
        surukle(pg, 320, 120); sh(pg, 'c%s_b' % c)
        surukle(pg, 80, 360); surukle(pg, 80, 330); sh(pg, 'c%s_c' % c)
        pg.mouse.click(W // 2, 620); time.sleep(9); sh(pg, 'c%s_d' % c)
        pg.mouse.click(W // 2, 640); time.sleep(9); sh(pg, 'c%s_e' % c)
        b.close()


def agac1():
    with sync_playwright() as p:
        b, pg = acik(p, 'http://localhost:8765/?c=1')
        sh(pg, 'a1_0')
        pg.mouse.click(88, 258); time.sleep(10); sh(pg, 'a1_1')
        pg.mouse.click(88, 258); time.sleep(5); sh(pg, 'a1_2')
        pg.mouse.click(206, 300); time.sleep(4); sh(pg, 'a1_3')
        pg.mouse.click(206, 400); time.sleep(4); sh(pg, 'a1_4')
        b.close()


for f in (ana, agac1):
    try: f()
    except Exception as e: print('HATA', f.__name__, str(e)[:300])
for c in ('1', '2', '3', '7', '18', '24'):
    try: cuz(c)
    except Exception as e: print('HATA', c, str(e)[:300])
