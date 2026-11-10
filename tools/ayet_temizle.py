#!/usr/bin/env python3
"""Tam ayet görsellerinden (f_NNN.png) kesim kalıntılarını siler. Ayet yazısına DOKUNMAZ:
yalnızca şu bileşenler silinir (alfa kanalı 0 yapılır, RGB aynen kalır, yeniden çizim/küçültme yok):
  A) kenara değen, dar ve küçük parçalar (komşu kelime/ayet işareti kırıntısı),
  B) metnin altında/üstünde duran ince uzun çizgiler (sayfa çerçevesi/altçizgi),
Kullanım: python3 tools/ayet_temizle.py [--uygula] [--cuz N] [--onizleme klasör]
Varsayılan kuru çalışma: sadece sayar ve önizleme üretir."""
import argparse, glob, json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAKET = os.path.join(KOK, 'flutter_app', 'assets', 'paket')
S8 = np.ones((3, 3), bool)

def analiz(yol):
    im = Image.open(yol)
    arr = np.array(im)
    a = arr[:, :, 3]
    m = a > 8
    h, w = m.shape
    lab, n = ndi.label(m, structure=S8)
    if n == 0:
        return None
    sl = ndi.find_objects(lab)
    alan = np.asarray(ndi.sum(m, lab, range(1, n + 1)))
    toplam = alan.sum()
    kutu = []
    for i in range(n):
        y0, y1 = sl[i][0].start, sl[i][0].stop
        x0, x1 = sl[i][1].start, sl[i][1].stop
        kutu.append((x0, y0, x1, y1))
    # "esas" bileşenler: harf gövdeleri / ayet numarası (büyük); küçükler harekeler/noktalar
    esas = [i for i in range(n) if alan[i] >= 0.03 * alan.max()]
    medh = float(np.median([kutu[i][3] - kutu[i][1] for i in esas]))
    ex0 = min(kutu[i][0] for i in esas); ex1 = max(kutu[i][2] for i in esas)
    ey0 = min(kutu[i][1] for i in esas); ey1 = max(kutu[i][3] for i in esas)
    sil = {}
    for i in range(n):
        x0, y0, x1, y1 = kutu[i]
        bw, bh = x1 - x0, y1 - y0
        kenar = (x0 <= 1) or (y0 <= 1) or (x1 >= w - 1) or (y1 >= h - 1)
        oran = alan[i] / toplam
        neden = None
        # B) ince uzun çizgi
        if bw >= 0.12 * w and bh <= max(8, 0.045 * h) and bw / max(bh, 1) >= 12 and (y0 >= ey1 - 3 or y1 <= ey0 + 3 or y0 >= 0.8 * h):
            neden = 'cizgi'
        # A) kenara değen dar/küçük parça
        elif kenar and oran < 0.05 and bh <= 0.6 * medh and ((bw <= 16 and (x0 <= 1 or x1 >= w - 1)) or (bh <= 14 and (y0 <= 1 or y1 >= h - 1))):
            neden = 'kenar'
        # A2) yatayda esas bölgenin dışında kalmış dar kırıntı
        elif i not in esas and oran < 0.03 and bw <= 16 and (x1 <= ex0 - 6 or x0 >= ex1 + 6):
            neden = 'yan'
        if neden:
            sil[i + 1] = (neden, int(alan[i]), kutu[i], round(bh / medh, 2))
    return arr, lab, sil, int(toplam), (w, h)

def isle(yol, uygula):
    r = analiz(yol)
    if r is None:
        return None
    arr, lab, sil, toplam, (w, h) = r
    if not sil:
        return None
    silinen = sum(v[1] for v in sil.values() if v[0] != 'cizgi')
    if silinen > 0.10 * toplam:
        return {'dosya': yol, 'atlandi': 'cok_fazla', 'sil': sil}
    if uygula:
        mask = np.isin(lab, list(sil.keys()))
        arr[mask, 3] = 0
        Image.fromarray(arr, 'RGBA').save(yol, optimize=False)
    return {'dosya': yol, 'sil': sil}

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--uygula', action='store_true')
    ap.add_argument('--cuz', type=int)
    ap.add_argument('--oneki', default='f')
    ap.add_argument('--rapor', default='/tmp/tv/chk/temizle_rapor.json')
    a = ap.parse_args()
    sonuc = []
    cuzler = [a.cuz] if a.cuz else range(1, 31)
    for c in cuzler:
        for y in sorted(glob.glob(f'{PAKET}/cuz{c}/img/{a.oneki}_*.png')):
            r = isle(y, a.uygula)
            if r:
                sonuc.append({'dosya': os.path.relpath(y, PAKET), 'atlandi': r.get('atlandi'),
                              'sil': [[v[0], v[1], list(map(int, v[2])), v[3]] for v in r['sil'].values()]})
    json.dump(sonuc, open(a.rapor, 'w'), ensure_ascii=False)
    from collections import Counter
    t = Counter(); atl = 0
    for s in sonuc:
        if s['atlandi']: atl += 1
        for v in s['sil']: t[v[0]] += 1
    print('değişecek dosya:', len(sonuc), 'atlanan:', atl, dict(t))
