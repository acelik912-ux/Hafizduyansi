import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'])
    pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=1)
    pg.on('console', lambda m: print('console:', m.text[:200]) if 'error' in m.type else None)
    pg.goto('http://localhost:8765/?c=5')
    time.sleep(14)
    pg.screenshot(path=os.path.join(out, 'c5_a.png'))
    pg.mouse.click(206, 560); time.sleep(5)
    pg.screenshot(path=os.path.join(out, 'c5_b.png'))
    b.close()
