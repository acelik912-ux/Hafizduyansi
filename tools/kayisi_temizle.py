#!/usr/bin/env python3
"""Kayısı ağacındaki (theme1 trees/tree01.png) çizili renkli topları yaprakla örter:
    python3 tools/kayisi_temizle.py   ->  flutter_app/assets/ozel/tree01_temiz.png
Her topun üzerine ağacın topsuz bir yerinden aynı boyda yaprak dokusu kopyalanır, kenarı yumuşatılarak kaynaştırılır.
Kaynak otomatik seçilir: tamamen opak, hiçbir topa değmeyen, topa en yakın daire (ton uyumu için).
Orijinal dosyaya dokunulmaz; çözünürlük aynı kalır (720×960). Yalnızca 1. cüz 1. sayfa ağaç ekranında kullanılır."""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIRDI = os.path.join(KOK, 'flutter_app', 'assets', 'paket', 'theme1', 'trees', 'tree01.png')
CIKTI = os.path.join(KOK, 'flutter_app', 'assets', 'ozel', 'tree01_temiz.png')

# (top merkezi x, y, yarıçap, aynala) — piksel, 720×960 görsel üzerinde
TOPLAR = [
    (415, 330, 52, None),  # siyah
    (243, 442, 52, None),  # sarı
    (517, 455, 58, 'x'),   # kırmızı
    (383, 547, 60, None),  # turuncu
    (203, 640, 60, 'x'),   # lacivert (+ arkasındaki turuncu parça)
    (557, 627, 55, 'y'),   # yeşil
]
YUMUSAK = 7  # kenar yumuşatma (px)

im = Image.open(GIRDI).convert('RGBA')
kaynak = im.copy()  # yamalar hep orijinalden alınır (bir yama diğerine taşınmasın)
alfa = np.array(kaynak.getchannel('A'))
H, W = alfa.shape
yy, xx = np.mgrid[0:H, 0:W]


def kaynak_bul(x, y, r):
    rr = r + YUMUSAK
    en_iyi = None
    for sy in range(rr, H - rr, 4):
        for sx in range(rr, W - rr, 4):
            d = ((sx - x) ** 2 + (sy - y) ** 2) ** 0.5
            if en_iyi and d >= en_iyi[0]:
                continue
            if any(((sx - bx) ** 2 + (sy - by) ** 2) ** 0.5 < rr + br + YUMUSAK for bx, by, br, _ in TOPLAR):
                continue  # kaynak hiçbir topa değmemeli
            kes = alfa[sy - rr:sy + rr + 1, sx - rr:sx + rr + 1]
            daire = (yy[:2 * rr + 1, :2 * rr + 1] - rr) ** 2 + (xx[:2 * rr + 1, :2 * rr + 1] - rr) ** 2 <= rr * rr
            if (kes[daire] < 250).any():
                continue  # kenardan alınırsa beyaz/saydam yay kalır
            en_iyi = (d, sx, sy)
    return en_iyi


for x, y, r, ayna in TOPLAR:
    b = kaynak_bul(x, y, r)
    if not b:
        raise SystemExit(f'({x},{y}) için opak kaynak bulunamadı')
    _, sx, sy = b
    print(f'top ({x},{y}) r={r}  <- kaynak ({sx},{sy})')
    R = r + YUMUSAK * 2
    yama = kaynak.crop((sx - R, sy - R, sx + R, sy + R))
    if ayna == 'x': yama = yama.transpose(Image.FLIP_LEFT_RIGHT)
    if ayna == 'y': yama = yama.transpose(Image.FLIP_TOP_BOTTOM)
    # ton eşitleme: yamanın ortalama rengi, topun çevresindeki halkanın (topsuz, opak) ortalama rengine çekilir
    org = np.array(kaynak).astype(np.float32)
    dist = np.sqrt((xx - x) ** 2 + (yy - y) ** 2)
    halka = (dist > r + 4) & (dist < r + 28) & (alfa >= 250)
    for bx, by, br, _ in TOPLAR:
        halka &= np.sqrt((xx - bx) ** 2 + (yy - by) ** 2) > br + 4
    hedef = org[halka][:, :3].mean(0)
    ya = np.array(yama).astype(np.float32)
    ic = ya[:, :, 3] >= 250
    oran = hedef / ya[ic][:, :3].mean(0)
    ya[:, :, :3] = np.clip(ya[:, :, :3] * oran, 0, 255)
    yama = Image.fromarray(ya.astype(np.uint8))
    print(f'   ton oranı R{oran[0]:.2f} G{oran[1]:.2f} B{oran[2]:.2f}')
    maske = Image.new('L', (2 * R, 2 * R), 0)
    ImageDraw.Draw(maske).ellipse((R - r - YUMUSAK, R - r - YUMUSAK, R + r + YUMUSAK, R + r + YUMUSAK), fill=255)
    maske = maske.filter(ImageFilter.GaussianBlur(YUMUSAK / 2))
    im.paste(yama, (x - R, y - R), maske)

os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
im.save(CIKTI, optimize=True)
print('yazıldı:', CIKTI, im.size)
