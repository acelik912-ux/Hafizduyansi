#!/usr/bin/env python3
"""Tema modülünün 20 görselini çizer ve temas sayfası (önizleme) üretir: python3 tools/onizle.py c05 ÇIKIŞ_KLASÖRÜ [ölçek] [numaralar...]"""
import importlib, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw
import svg_png

modül, çıkış = sys.argv[1], sys.argv[2]
ölçek = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
seç = [int(x) for x in sys.argv[4:]]
m = importlib.import_module(modül)
sd = os.path.join(çıkış, 'svg'); pd = os.path.join(çıkış, 'png')
os.makedirs(sd, exist_ok=True)
import shutil; shutil.rmtree(pd, ignore_errors=True)
for f in os.listdir(sd): os.remove(os.path.join(sd, f))
for i in range(len(m.ADLAR)):
    if seç and (i + 1) not in seç: continue
    sv = m.ciz(i, random.Random(1000 + i))
    open(os.path.join(sd, '%02d.svg' % (i + 1)), 'w', encoding='utf-8').write(str(sv))
svg_png.donustur(ölçek, sd, pd)
fs = sorted(os.listdir(pd))
w, h = int(720 * ölçek), int(960 * ölçek)
cols = 5
rows = (len(fs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * (h + 18)), tuple(int(x) for x in getattr(m, 'ONIZLEME_ZEMIN', (150, 190, 120))))
d = ImageDraw.Draw(sheet)
for k, f in enumerate(fs):
    im = Image.open(os.path.join(pd, f))
    x, y = (k % cols) * w, (k // cols) * (h + 18)
    sheet.paste(im, (x, y + 18), im)
    d.text((x + 4, y + 2), '%s %s' % (f[:2], m.ADLAR[int(f[:2]) - 1]), fill='black')
sheet.save(os.path.join(çıkış, 'sayfa.png'))
print('tamam', len(fs))
