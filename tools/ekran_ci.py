"""CI'da web sürümünden ekran görüntüsü (geçici). Her cüz için iki kamera: yol üstü ve yandan."""
import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
URLS = {}
for c in range(5, 16):
    URLS['c%02d_a' % c] = '?c=%d&x=0&z=8&y=0' % c
    URLS['c%02d_b' % c] = '?c=%d&x=0&z=30&y=-0.7' % c
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'])
    for ad, q in URLS.items():
        pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=1)
        pg.on('console', lambda m: print('console:', m.text[:200]) if 'error' in m.type else None)
        pg.goto('http://localhost:8765/' + q)
        time.sleep(28)
        pg.screenshot(path=os.path.join(out, ad + '.png'))
        pg.close()
    b.close()
