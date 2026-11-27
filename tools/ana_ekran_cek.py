# geçici: web sürümünden 1080x1920 ana ekran (Bugün) görüntüsü alır; ana dala ALINMAZ
import sys, time
from playwright.sync_api import sync_playwright
out = sys.argv[1]
import os; os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 360, 'height': 640}, device_scale_factor=3, is_mobile=True, has_touch=True)
    pg.goto('http://localhost:8765/')
    time.sleep(20)
    pg.screenshot(path=f'{out}/ana_ekran.png')
    b.close()
