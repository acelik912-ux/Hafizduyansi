#!/usr/bin/env python3
"""SVG klasörünü saydam zeminli PNG'ye çevirir (Playwright/Chromium; Mac'siz ortam için svg_png.mjs'in karşılığı).
    python3 tools/svg_png.py ÖLÇEK GİRİŞ ÇIKIŞ"""
import os, re, sys
from playwright.sync_api import sync_playwright

def donustur(olcek, giris, cikis):
    os.makedirs(cikis, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for f in sorted(os.listdir(giris)):
            if not f.endswith('.svg'):
                continue
            svg = open(os.path.join(giris, f), encoding='utf-8').read()
            w, h = (int(x) for x in re.search(r'width="(\d+)" height="(\d+)"', svg).groups())
            pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=olcek)
            pg.set_content('<html><body style="margin:0;background:transparent">' + svg + '</body></html>')
            pg.screenshot(path=os.path.join(cikis, f[:-4] + '.png'), omit_background=True, clip={'x': 0, 'y': 0, 'width': w, 'height': h})
            pg.close()
        b.close()

if __name__ == '__main__':
    donustur(float(sys.argv[1]), sys.argv[2], sys.argv[3])
