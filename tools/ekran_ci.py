"""CI'da web sürümünden ekran görüntüsü: Cüzler sekmesi görünümleri (geçici)."""
import os, sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(args=['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist', '--enable-webgl'])
    pg = b.new_page(viewport={'width': 412, 'height': 880}, device_scale_factor=1)
    pg.goto('http://localhost:8765/')
    time.sleep(25)
    pg.mouse.click(206, 845)  # alt çubuk: Cüzler
    time.sleep(6)
    pg.screenshot(path=os.path.join(out, 'c0_tek.png'))
    for ad, x in (('c1_iki', 160), ('c2_dort', 253), ('c3_liste', 346)):
        pg.mouse.click(x, 106)
        time.sleep(6)
        pg.screenshot(path=os.path.join(out, ad + '.png'))
    b.close()
