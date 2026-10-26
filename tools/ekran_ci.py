"""CI'da web sürümünden ekran görüntüsü (playwright). Kullanım: python3 tools/ekran_ci.py ÇIKIŞ"""
import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
URLS = {
    'a_yol': '?c=1&x=0&z=-3&y=0',
    'b_agac': '?c=1&x=0&z=6&y=0',
    'c_sag': '?c=1&x=0&z=6&y=0.9',
    'd_yakin': '?c=1&x=0.9&z=0.5&y=0',
    'e_magara': '?c=2&x=0&z=-3&y=0',
}
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'])
    for ad, q in URLS.items():
        pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=1)
        pg.on('console', lambda m: print('console:', m.text[:200]) if 'zemin' in m.text.lower() or 'error' in m.type else None)
        pg.goto('http://localhost:8765/' + q)
        time.sleep(30)
        pg.screenshot(path=os.path.join(out, ad + '.png'))
        pg.close()
    b.close()
