#!/usr/bin/env python3
"""İllüstrasyonlardan Hafız Dünyası tema paketi (kind:'theme') üretir.

Kullanım:
  python3 tools/tema_paketle.py KLASOR --cuz 2 --cikis Tema_Cuz2.zip

KLASOR içinde:
  agaclar/01.png … 20.png      20 ağaç, şeffaf arka planlı PNG (önerilen oran 3:4, ör. 720x960). Küçültülmez.
  meyveler/01.png … 20.png     her ağacın meyvesi (tek görsel). 5 renk (siyah, kırmızı, sarı, yeşil, lacivert)
                               otomatik boyanır; yapraklar (yeşil kısımlar) yeşil kalır.
     ya da meyveler/01_0.png … 01_4.png  5 rengi hazır verirsen boyama yapılmaz (0 siyah, 1 kırmızı, 2 sarı, 3 yeşil, 4 lacivert).
  arka_plan/bahce.jpg          (isteğe bağlı) orman ekranı arka planı
  arka_plan/sayfa.jpg          (isteğe bağlı) ağaç sayfası arka planı
  arka_plan/ayet.jpg           (isteğe bağlı) ayet paneli arka planı
  adlar.txt                    (isteğe bağlı) 20 satır ağaç adı (ör. "Zeytin")
Verilmeyen arka planlar için uygulama 1. cüz temasındakileri kullanır.
--cuz verilmezse tema varsayılan tema olur (tüm cüzlerde geçerli; 1. cüz teması böyledir).
"""
import argparse, colorsys, io, json, os, re, sys, zipfile

import numpy as np
from PIL import Image

FRUIT_COL = [(17, 17, 17), (211, 47, 47), (242, 169, 0), (46, 158, 79), (31, 60, 136)]  # siyah, kırmızı, sarı, yeşil, lacivert


def recolor(img, k):
    """Meyveyi k. renge boyar: parlaklık korunur, renk değişir; yeşil yapraklar ve şeffaflık korunur."""
    a = np.array(img.convert('RGBA')).astype(np.float32) / 255
    rgb, al = a[..., :3], a[..., 3:]
    mx, mn = rgb.max(-1), rgb.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    # ton (0-1)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    d = np.maximum(mx - mn, 1e-6)
    hue = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) / 6
    leaf = (hue > 0.18) & (hue < 0.48) & (sat > 0.25)  # yeşil yapraklar
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    t = np.array(FRUIT_COL[k], np.float32) / 255
    tl = 0.299 * t[0] + 0.587 * t[1] + 0.114 * t[2]
    if k == 0:  # siyah: koyulaştır, parlak yerler gri kalsın
        out = np.repeat((lum ** 1.6 * 0.75)[..., None], 3, -1)
    else:
        # parlaklığı hedef rengin parlaklığı etrafında koru (gölge/ışık), rengi hedefe çek
        sh = lum / max(np.median(lum[(al[..., 0] > 0.5) & ~leaf]) if ((al[..., 0] > 0.5) & ~leaf).any() else 0.5, 1e-3)
        out = np.clip(t[None, None, :] * sh[..., None] * 0.85, 0, 1)
        hi = np.clip((lum - 0.75) / 0.25, 0, 1)[..., None]  # parlama noktaları beyaza yakın kalsın
        out = out * (1 - hi) + hi * np.clip(t + 0.4, 0, 1)
    out = np.where(leaf[..., None], rgb, out)
    return Image.fromarray((np.dstack([out, al]) * 255).astype(np.uint8), 'RGBA')


def png_bytes(img):
    b = io.BytesIO()
    img.save(b, 'PNG', optimize=True)
    return b.getvalue()


def num(f):
    m = re.match(r'(\d+)(?:_(\d))?\.png$', f, re.I)
    return (int(m.group(1)), None if m.group(2) is None else int(m.group(2))) if m else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('klasor')
    ap.add_argument('--cuz', type=int)
    ap.add_argument('--cikis', required=True)
    o = ap.parse_args()
    K = o.klasor
    meta = {'version': 7, 'kind': 'theme', 'name': f'Hafız Dünyası {o.cuz}. Cüz teması' if o.cuz else 'Hafız Dünyası teması', 'ui': {}, 'trees': {}}
    if o.cuz:
        meta['cuz'] = o.cuz
    files = {}
    td = os.path.join(K, 'agaclar')
    for f in sorted(os.listdir(td)):
        n = num(f)
        if not n:
            continue
        im = Image.open(os.path.join(td, f))
        if im.mode != 'RGBA':
            print(f'  ! {f}: şeffaf arka plan yok (RGBA değil)', file=sys.stderr)
        name = f'tree{n[0]:02d}.png'
        files['trees/' + name] = open(os.path.join(td, f), 'rb').read()
        meta['trees'][str(n[0])] = {'file': name, 'w': im.width, 'h': im.height}
    fd = os.path.join(K, 'meyveler')
    singles, ready = {}, {}
    for f in sorted(os.listdir(fd)) if os.path.isdir(fd) else []:
        n = num(f)
        if not n:
            continue
        if n[1] is None:
            singles[n[0]] = os.path.join(fd, f)
        else:
            ready[(n[0], n[1])] = os.path.join(fd, f)
    for i in sorted(set(singles) | {k[0] for k in ready}):
        for k in range(5):
            if (i, k) in ready:
                files[f'fruits/{i}_{k}.png'] = open(ready[(i, k)], 'rb').read()
            elif i in singles:
                files[f'fruits/{i}_{k}.png'] = png_bytes(recolor(Image.open(singles[i]), k))
    bgd = os.path.join(K, 'arka_plan')
    for src, kinds in (('bahce', ['bgGarden', 'bgForest']), ('sayfa', ['bgPage']), ('ayet', ['bgAyet'])):
        for ext in ('jpg', 'jpeg', 'png'):
            pth = os.path.join(bgd, f'{src}.{ext}')
            if os.path.exists(pth):
                files[f'bg/{src}.{ext}'] = open(pth, 'rb').read()
                for kd in kinds:
                    meta['ui'][kd] = f'{src}.{ext}'
                break
    an = os.path.join(K, 'adlar.txt')
    if os.path.exists(an):
        meta['names'] = [l.strip() for l in open(an, encoding='utf-8') if l.strip()]
    with zipfile.ZipFile(o.cikis, 'w', zipfile.ZIP_STORED) as z:
        z.writestr('project.json', json.dumps(meta, ensure_ascii=False))
        for n, d in files.items():
            z.writestr(n, d)
    nf = len([f for f in files if f.startswith('fruits/')])
    print(f'{o.cikis}: {len(meta["trees"])} ağaç, {nf} meyve görseli, arka planlar: {sorted(meta["ui"])}, {os.path.getsize(o.cikis) / 1e6:.1f} MB')
    if len(meta['trees']) != 20:
        print(f'  ! 20 ağaç bekleniyordu, {len(meta["trees"])} bulundu', file=sys.stderr)


if __name__ == '__main__':
    main()
