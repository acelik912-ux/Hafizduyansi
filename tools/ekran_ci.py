"""CI'da web sürümünden ekran görüntüsü (playwright). Kullanım: python3 tools/ekran_ci.py ÇIKIŞ"""
import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
URLS = {
    'k1_giris': '?c=3&x=0&z=-3&y=0',
    'k2_yol': '?c=3&x=0&z=8&y=0',
    'k3_sol': '?c=3&x=0&z=14&y=0.7',
    'k4_sag': '?c=3&x=0&z=30&y=-0.7',
}
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'])
    for ad, q in URLS.items():
        pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=1)
        pg.on('console', lambda m: print('console:', m.text[:200]) if 'zemin' in m.text.lower() or 'error' in m.type else None)
        pg.goto('http://localhost:8765/' + q)
        time.sleep(35)
        pg.screenshot(path=os.path.join(out, ad + '.png'))
        pg.close()
    b.close()
