import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
URLS = {}
for c in (4, 5, 6, 9, 10, 11, 12, 14, 18, 24):
    URLS['c%02d_a' % c] = '?c=%d&x=0&z=-3&y=0.7' % c
    URLS['c%02d_b' % c] = '?c=%d&x=0&z=-3&y=1.4' % c
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'])
    for ad, q in URLS.items():
        pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=1)
        pg.goto('http://localhost:8765/' + q); time.sleep(14)
        pg.screenshot(path=os.path.join(out, ad + '.png')); pg.close()
    b.close()
