import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
URLS = {}
for ic in [0,3,5,8,12,15]:
    URLS['ic%02d_a' % ic] = '?c=18&ic=%d' % ic
    URLS['ic%02d_b' % ic] = '?c=18&ic=%d&x=0&z=14&y=3.14' % ic
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'])
    for ad, q in URLS.items():
        pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=1)
        pg.on('console', lambda m: print('console:', m.text[:200]) if 'error' in m.type else None)
        pg.goto('http://localhost:8765/' + q)
        time.sleep(14)
        pg.screenshot(path=os.path.join(out, ad + '.png'))
        pg.close()
    b.close()
