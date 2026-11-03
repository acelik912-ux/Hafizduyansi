import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
URLS = {'a': '?c=12&x=0&z=-3&y=0', 'b': '?c=12&x=0&z=-3&y=1.6', 'c': '?c=12&x=0&z=-3&y=3.14', 'd': '?c=12&x=0&z=-3&y=-1.6', 'e': '?c=12&x=0&z=-3&y=0.5'}
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'])
    for ad, q in URLS.items():
        pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=1)
        pg.on('console', lambda m: print('console:', m.text[:200]) if 'error' in m.type else None)
        pg.goto('http://localhost:8765/' + q)
        time.sleep(16)
        pg.screenshot(path=os.path.join(out, ad + '.png'))
        pg.close()
    b.close()
