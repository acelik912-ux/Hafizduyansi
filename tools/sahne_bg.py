#!/usr/bin/env python3
"""Konsept sahneleri için sayfa arka planları (ağaç sayfası / kart görünümü) ve ayet paneli kemeri üretir.

    python3 tools/sahne_bg.py ÇIKIŞ_KLASÖRÜ [sahne ...]
      -> ÇIKIŞ/<sahne>_sayfa.jpg (1620x2880, bgGarden/bgForest/bgPage) ve ÇIKIŞ/<sahne>_kemer.jpg (1080x1920, bgAyet)

Sayfa arka planı varsayılan temanın (theme1/garden_page.jpg) düzenini izler: koyu gökyüzü, ufukta ışıma, ufuk silueti, ışık huzmeleri,
zeminde ince tane. Kemer, varsayılan temanın altın çerçevesini (theme1/bg/arch.jpg) korur; yalnızca iç görüntüyü konsepte göre değiştirir.
Her sahne paletinin adı bahce3d.dart içindeki _ayarlar anahtarıyla aynıdır."""
import math, os, random, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEMER = os.path.join(KOK, 'flutter_app', 'assets', 'paket', 'theme1', 'bg', 'arch.jpg')


def hx(s):
    return np.array([int(s[i:i + 2], 16) for i in (0, 2, 4)], dtype=np.float32)


# ad: (gök üst, ufuk ışıması, zemin üst, zemin alt, huzme, siluet, tür, yıldız)
PALET = {
    'orman': ('15332A', 'C9E3B2', '2F6B3B', '102F1E', 'FFF2B0', '1B4429', 'agac', False),
    'gok': ('050824', '5A4F8E', '1A2254', '090D2A', 'AFC4FF', '0E1336', 'tepe', True),
    'otlak': ('2A3A24', 'F0CE7C', '55712F', '1D3012', 'FFE8A8', '3C5226', 'tepe', False),
    'col': ('3A2418', 'F3C47C', '93603A', '3A2214', 'FFD9A0', '6E4528', 'kum', False),
    'ova': ('1E3550', 'F4DC8E', '82712F', '2F2A10', 'FFF0B8', '5F5A28', 'tepe', False),
    'sahil': ('0C3450', 'B4E4F0', '1D7396', '082C42', 'D8F4FF', '1B6C8C', 'deniz', False),
    'vadi': ('1C2A37', 'A2B8C2', '3B5C5A', '14242A', 'D8E6EE', '2A4846', 'bulut', False),
    'nahl': ('3A3012', 'FFE38C', '62802B', '1E2E0E', 'FFEDB0', '48611F', 'tepe', False),
    'dag': ('26263F', 'F6CCAA', '5C5C56', '1C1C20', 'FFE2CC', '3A3A46', 'dag', False),
}


def gradyan(h, w, renkler, duraklar):
    y = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    out = np.zeros((h, 1, 3), np.float32)
    for c in range(3):
        out[:, 0, c] = np.interp(y[:, 0], duraklar, [r[c] for r in renkler])
    return np.repeat(out, w, axis=1)


def siluet(w, h, yh, tur, rnd, col, olc):
    m = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(m)
    if tur == 'agac':
        x = -40
        while x < w + 40:
            r = rnd.uniform(60, 150) * olc
            top = yh - rnd.uniform(0.5, 2.2) * r
            d.ellipse([x - r * 0.8, top, x + r * 0.8, top + r * 1.8], fill=255)
            d.rectangle([x - r * 0.07, min(top + r, yh), x + r * 0.07, yh + 8], fill=255)
            x += r * rnd.uniform(0.7, 1.3)
        d.rectangle([0, yh - 6, w, h], fill=255)
    elif tur in ('tepe', 'kum', 'bulut'):
        pts = [(0, h)]
        ph = [rnd.uniform(0, 6.28) for _ in range(4)]
        amp = {'tepe': 70, 'kum': 120, 'bulut': 40}[tur] * olc
        for x in range(0, w + 8, 8):
            t = x / w
            v = math.sin(t * 5.0 + ph[0]) * 0.55 + math.sin(t * 11 + ph[1]) * 0.25 + math.sin(t * 23 + ph[2]) * 0.1
            pts.append((x, yh - 20 * olc - amp * v))
        pts.append((w, h))
        d.polygon(pts, fill=255)
    elif tur == 'dag':
        pts = [(0, h), (0, yh)]
        x, y = 0, yh
        while x < w:
            x += rnd.uniform(40, 120) * olc
            y = yh - rnd.uniform(40, 340) * olc if rnd.random() < 0.55 else yh - rnd.uniform(0, 120) * olc
            pts.append((x, y))
        pts += [(w, yh), (w, h)]
        d.polygon(pts, fill=255)
    elif tur == 'deniz':
        d.rectangle([0, yh, w, h], fill=255)
    return m


def sayfa(ad, w=1620, h=2880, aydinlik=0.0, seed=7):
    ust, ufuk, zu, za, hz, si, tur, yildiz = PALET[ad]
    rnd = random.Random(seed)
    olc = w / 1080
    yh = int(h * 0.30)
    ust, ufuk, zu, za, hz, si = (hx(v) for v in (ust, ufuk, zu, za, hz, si))
    beyaz = np.array([255, 255, 255], np.float32)
    if aydinlik:
        ust, ufuk, zu, za = (v + (beyaz - v) * aydinlik for v in (ust, ufuk, zu, za))
    gok = gradyan(yh, w, [ust, ust * 0.6 + ufuk * 0.4, ufuk], [0, 0.55, 1])
    zem = gradyan(h - yh, w, [zu, za], [0, 1])
    img = np.vstack([gok, zem])
    # ufuk ışıması
    yy = np.arange(h, dtype=np.float32)[:, None]
    isik = np.exp(-((yy - yh) / (h * 0.09)) ** 2)
    img += (ufuk - img) * (isik * 0.35)[:, :, None]
    # yıldızlar
    if yildiz:
        im0 = Image.fromarray(img.clip(0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im0)
        for _ in range(420):
            x, y = rnd.uniform(0, w), rnd.uniform(0, yh * 0.95)
            r = rnd.uniform(1.0, 3.2) * olc
            a = int(rnd.uniform(140, 255))
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 252, 240))
        mx, my, mr = w * 0.68, yh * 0.32, 70 * olc
        g = Image.new('RGB', (w, h), (0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.ellipse([mx - mr * 3, my - mr * 3, mx + mr * 3, my + mr * 3], fill=(40, 40, 60))
        g = g.filter(ImageFilter.GaussianBlur(mr))
        img = np.asarray(im0).astype(np.float32) + np.asarray(g).astype(np.float32)
        im0 = Image.fromarray(img.clip(0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im0)
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(248, 242, 214))
        d.ellipse([mx - mr + mr * 0.45, my - mr - mr * 0.1, mx + mr + mr * 0.45, my + mr - mr * 0.1], fill=tuple(int(v) for v in img[int(my), int(mx - mr * 1.6)]))
        img = np.asarray(im0).astype(np.float32)
    # bulutlar (vadi) / yumuşak sis
    if tur == 'bulut':
        b = Image.new('L', (w, h), 0)
        d = ImageDraw.Draw(b)
        for _ in range(26):
            x, y = rnd.uniform(-100, w), rnd.uniform(0, yh * 0.9)
            r = rnd.uniform(120, 300) * olc
            d.ellipse([x - r, y - r * 0.38, x + r, y + r * 0.38], fill=int(rnd.uniform(60, 130)))
        b = np.asarray(b.filter(ImageFilter.GaussianBlur(60 * olc))).astype(np.float32) / 255
        img = img + (np.array([225, 232, 238], np.float32) - img) * b[:, :, None]
    # ışık huzmeleri
    r = Image.new('L', (w, h), 0)
    d = ImageDraw.Draw(r)
    for i in range(7):
        x = w * (0.05 + 0.15 * i) + rnd.uniform(-50, 50)
        gen = rnd.uniform(60, 140) * olc
        d.polygon([(x, 0), (x + gen, 0), (x + gen + 300 * olc, h * 0.62), (x + 300 * olc, h * 0.62)], fill=int(rnd.uniform(40, 90)))
    r = np.asarray(r.filter(ImageFilter.GaussianBlur(45 * olc))).astype(np.float32) / 255
    ay = 0.0 if ad == 'gok' else 0.30
    img = img + (hx(PALET[ad][4]) - img) * (r * ay)[:, :, None]
    # siluet
    sm = siluet(w, h, yh, tur, rnd, si, olc)
    if tur != 'deniz':
        sm = np.asarray(sm.filter(ImageFilter.GaussianBlur(1.2 * olc))).astype(np.float32) / 255
        img = img + (si - img) * sm[:, :, None] * 0.85
    else:
        # deniz: ufukta ince parlak çizgi + dalga parıltıları (sabit)
        im0 = Image.fromarray(img.clip(0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im0)
        for _ in range(900):
            x, y = rnd.uniform(0, w), yh + (rnd.random() ** 1.6) * (h - yh)
            gen = rnd.uniform(20, 90) * olc * (0.4 + (y - yh) / (h - yh))
            d.line([x, y, x + gen, y], fill=(190, 235, 245), width=max(1, int(2 * olc)))
        img = np.asarray(im0).astype(np.float32)
        img[yh - 3:yh + 3] = np.array([210, 240, 250], np.float32)
    # zemin: ince tane + alta doğru kararma
    gur = np.random.default_rng(seed).normal(0, 4.5, (h, w, 1)).astype(np.float32)
    img = img + gur * (yy > yh)[:, :, None]
    alcak = ndi.gaussian_filter(np.random.default_rng(seed + 1).normal(0, 1, (h // 4, w // 4)).astype(np.float32), 46 * olc / 4)
    alcak = np.asarray(Image.fromarray(alcak).resize((w, h), Image.BILINEAR))
    img = img + (alcak / (alcak.std() + 1e-6) * 2.6)[:, :, None] * (yy > yh)[:, :, None]
    kar = 1 - 0.28 * np.clip((yy - h * 0.75) / (h * 0.25), 0, 1)
    img = img * kar[:, :, None]
    return Image.fromarray(img.clip(0, 255).astype(np.uint8), 'RGB')


def kemer(ad):
    """altın çerçeveyi koru, içini konsepte göre değiştir (çerçevenin iç sınırı satır satır bulunur)"""
    src = Image.open(KEMER).convert('RGB')
    w, h = src.size
    a = np.asarray(src).astype(int)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    altin = ndi.binary_closing((R - B > 45) & (R > 150) & (G > 110) & (R >= G), iterations=3)
    lab, _ = ndi.label(~altin)
    ic = lab == lab[h // 2, w // 2]
    ic = ndi.binary_fill_holes(ic)
    ys = np.where(ic.any(axis=1))[0]
    ytop, ybot = int(ys.min()), int(ys.max())
    xmin = np.array([np.where(ic[y])[0].min() for y in range(int(h * 0.45), int(h * 0.80))])
    xmax = np.array([np.where(ic[y])[0].max() for y in range(int(h * 0.45), int(h * 0.80))])
    L, Rr = int(np.median(xmin)), int(np.median(xmax))
    r, cx = (Rr - L) / 2.0, (Rr + L) / 2.0
    cy = ytop + r
    yy, xx = np.mgrid[0:h, 0:w]
    maske = (xx >= L) & (xx <= Rr) & (yy >= cy) & (yy <= ybot)
    maske |= (yy < cy) & (yy >= ytop) & (((xx - cx) ** 2 + (yy - cy) ** 2) <= r * r)
    maske = ndi.binary_erosion(maske, iterations=3)  # çerçevenin kenar yumuşatmasına dokunma
    yeni = sayfa(ad, w, h, aydinlik=0.0 if ad == 'gok' else 0.52, seed=11).filter(ImageFilter.GaussianBlur(3))
    f = ndi.gaussian_filter(maske.astype(np.float32), 1.4)[:, :, None]
    out = np.asarray(yeni).astype(np.float32) * f + np.asarray(src).astype(np.float32) * (1 - f)
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), 'RGB')


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cikis = sys.argv[1]
    os.makedirs(cikis, exist_ok=True)
    adlar = sys.argv[2:] or list(PALET)
    for ad in adlar:
        sayfa(ad).save(os.path.join(cikis, ad + '_sayfa.jpg'), quality=93, subsampling=0)
        kemer(ad).save(os.path.join(cikis, ad + '_kemer.jpg'), quality=94, subsampling=0)
        print(ad)


if __name__ == '__main__':
    main()
