import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'])
    pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=1)
    pg.on('console', lambda m: print('console:', m.text[:200]) if 'error' in m.type else None)
    pg.goto('http://localhost:8765/'); time.sleep(10)
    pg.screenshot(path=out + '/a.png')
    pg.mouse.click(40, 370); time.sleep(2)
    pg.keyboard.type('hedef'); pg.keyboard.press('Enter'); time.sleep(2)
    pg.screenshot(path=out + '/b.png')
    pg.goto('http://localhost:8765/?c=12'); time.sleep(14)
    pg.mouse.click(30, 840); time.sleep(1)
    pg.keyboard.type('x'); pg.keyboard.press('Enter'); time.sleep(1)
    pg.mouse.click(120, 500); time.sleep(5)   # yere yürü
    pg.screenshot(path=out + '/c.png')
    b.close()
