#!/usr/bin/env python3
"""Tam ayet (f_) ve ayet başı (s_) görsellerinde, komşu satırdan kırpılıp kalmış KIRMIZI işaret artıklarını bulur / siler.
Artık = görselin en üstündeki (ya da en altındaki) küçük kırmızı bileşen ve geri kalan her şeyden EN AZ `--bosluk` px uzakta.
(Meşru vakıf işaretleri harfin hemen üstünde/altında durur; artık ise ayrık, boşlukta yüzer.)
  python3 tools/kirmizi_artik.py <paket_klasoru|paket_kok> [--bosluk 22] [--uygula] [--sayfa ciktisi.png]
Varsayılan KURU çalışma: yalnızca listeler. --uygula: bileşenin alfasını 0 yapar (RGB aynen; yazıya dokunulmaz).
Boyutlar: orta büyüklük değil, bileşen alanı <= --alan (varsayılan 260), yüksekliği <= 30."""
import argparse, os, sys, glob
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from concurrent.futures import ProcessPoolExecutor

def tara(a):
    p, bosluk, alan_max, uygula, aralik = a
    try:
        im = Image.open(p).convert('RGBA'); arr = np.asarray(im).copy()
    except Exception as e:
        return p, 'HATA ' + str(e), []
    al = arr[..., 3] > 0
    a_ = al
    lab, n = ndi.label(al, structure=np.ones((3, 3)))
    if n < 2:
        return p, 'OK', []
    objs = ndi.find_objects(lab)
    bilgi = []
    for i, s in enumerate(objs, 1):
        m = lab[s] == i
        px = arr[s][m]
        r, g, b = px[:, 0].astype(int).mean(), px[:, 1].astype(int).mean(), px[:, 2].astype(int).mean()
        kirmizi = r > g + 50 and r > b + 50
        bilgi.append((i, s[0].start, s[0].stop, s[1].start, s[1].stop, int(m.sum()), kirmizi))
    bul = []
    for (i, y0, y1, x0, x1, ar, kir) in bilgi:
        if not kir or ar > alan_max or (y1 - y0) > 30:
            continue
        digerler = [b for b in bilgi if b[0] != i]
        ust = min(b[1] for b in digerler); alt = max(b[2] for b in digerler)
        # yatay örtüşen en yakın gövde pikseline dikey uzaklık (meşru işaret harfe yakındır, artık havada durur)
        sut = a_[:, max(0, x0 - 4):x1 + 4].copy(); sut[y0:y1 + 1, :] = False
        if y1 <= ust and ust - y1 >= bosluk:
            r = np.where(sut[y1 + 1:].any(1))[0]; g = int(r[0]) + 1 if len(r) else 999
            if g >= aralik: bul.append(('ust', i, y0, y1, x0, x1, ar, g))
        elif y0 >= alt and y0 - alt >= bosluk:
            r = np.where(sut[:y0][::-1].any(1))[0]; g = int(r[0]) + 1 if len(r) else 999
            if g >= aralik: bul.append(('alt', i, y0, y1, x0, x1, ar, g))
    if bul and uygula:
        for t, i, *_ in bul:
            arr[lab == i, 3] = 0
        Image.fromarray(arr, 'RGBA').save(p, optimize=True)
    return p, 'OK', bul

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('yol'); ap.add_argument('--bosluk', type=int, default=22)
    ap.add_argument('--alan', type=int, default=260); ap.add_argument('--aralik', type=int, default=45, help='yatay örtüşen en yakın harfe dikey uzaklık (px)'); ap.add_argument('--uygula', action='store_true')
    ap.add_argument('--ornek', type=int, default=0, help='yalnız ilk N dosya (deneme)')
    ap.add_argument('--on', default='f_,s_', help='dosya ön ekleri')
    a = ap.parse_args()
    onl = tuple(a.on.split(','))
    dosyalar = []
    for r, _, fs in os.walk(a.yol):
        for f in fs:
            if f.endswith('.png') and f.startswith(onl) and os.sep + 'img' in r + os.sep:
                dosyalar.append(os.path.join(r, f))
    dosyalar.sort()
    if a.ornek: dosyalar = dosyalar[:a.ornek]
    print(len(dosyalar), 'dosya taranıyor', '(UYGULA)' if a.uygula else '(kuru)', file=sys.stderr)
    toplam = 0; hist = {}
    with ProcessPoolExecutor() as ex:
        for p, d, bul in ex.map(tara, [(p, a.bosluk, a.alan, a.uygula, a.aralik) for p in dosyalar], chunksize=8):
            if d != 'OK': print(p, d); continue
            for t, i, y0, y1, x0, x1, ar, bos in bul:
                toplam += 1
                print(f'{os.path.relpath(p, a.yol)}\t{t}\ty{y0}-{y1}\tx{x0}-{x1}\talan{ar}\tboşluk{bos}')
    print('TOPLAM artık:', toplam, file=sys.stderr)

if __name__ == '__main__':
    main()
