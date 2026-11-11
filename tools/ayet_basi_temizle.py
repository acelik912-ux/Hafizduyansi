#!/usr/bin/env python3
"""Ayet başı görsellerinden (s_*.png, ayetin ilk kelimeleri) kesim kalıntılarını siler. Yazıya DOKUNMAZ:
yalnızca ayrık küçük bileşenlerin alfası 0 yapılır (RGB aynen kalır; yeniden çizim/küçültme yok).
Silinen kalıntı türleri (hepsi 'esas' yazı bileşeninden ayrık parçalardır):
  yan   : sol/sağ kenara değen, tüm yazının x aralığının DIŞINDA kalan dar parça (komşu kelimenin kenar kırıntısı)
  alt   : alt kenara değen, dar-dikey, üstündeki yazıdan en az 5 px boşlukla ayrık parça (alttaki satırın elif/lam uçları)
  ust   : üst kenara değen, dar-dikey, altındaki yazıdan en az 5 px boşlukla ayrık parça (üstteki satırın harf kuyrukları)
  kirinti: kenara değen, alanı çok küçük (≤6 px) ayrık parça
  uzak  : hiçbir yazıya 8 px'ten yakın olmayan çok küçük (≤8 px) parça
  cizgi : yatay ince uzun çizgi (sayfa çerçevesi / alt çizgi)
Kesre, fetha, nokta, vakıf işareti (ط ج ۛ), ayet numarası gibi yazının parçaları, esas yazıya yakın oldukları için silinmez.
Kullanım: python3 tools/ayet_basi_temizle.py [--uygula] [--cuz N] [--rapor dosya.json]
Varsayılan kuru çalışma (hiçbir dosyaya yazmaz)."""
import argparse, glob, json, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAKET = os.path.join(KOK, 'flutter_app', 'assets', 'paket')
S8 = np.ones((3, 3), bool)


def bosluk(m, c, x0, x1, y0, y1, yon):
    """Bileşenin (c) x aralığında (±3 px), yon='ust' ise üstündeki, 'alt' ise altındaki en yakın başka yazıya uzaklık (px)."""
    diger = m & ~c
    xa, xb = max(0, x0 - 3), x1 + 3
    if yon == 'ust':
        sat = np.where(diger[:y0, xa:xb].any(axis=1))[0]
        return (y0 - (sat.max() + 1)) if len(sat) else 99
    sat = np.where(diger[y1:, xa:xb].any(axis=1))[0]
    return (sat.min()) if len(sat) else 99


def analiz(yol):
    arr = np.array(Image.open(yol))
    m = arr[:, :, 3] > 8
    h, w = m.shape
    lab, n = ndi.label(m, structure=S8)
    if n < 2:
        return None
    sl = ndi.find_objects(lab)
    alan = np.asarray(ndi.sum(m, lab, range(1, n + 1)))
    toplam = float(alan.sum())
    esas = int(alan.argmax())
    kutu = [(s[1].start, s[0].start, s[1].stop, s[0].stop) for s in sl]
    sil = {}
    for i in range(n):
        if i == esas:
            continue
        x0, y0, x1, y1 = kutu[i]
        bw, bh, a = x1 - x0, y1 - y0, alan[i]
        c = lab == (i + 1)
        # "yazının x aralığı": yalnızca büyük gövdeler (alan >= %10); harekeler/işaretler ve diğer kırıntılar sayılmaz
        buyuk = [j for j in range(n) if j != i and alan[j] >= 0.10 * alan.max()]
        digx0 = min(kutu[j][0] for j in buyuk)
        digx1 = max(kutu[j][2] for j in buyuk)
        kenarL, kenarR, kenarT, kenarB = x0 <= 1, x1 >= w - 1, y0 <= 1, y1 >= h - 1
        neden = None
        # yatay ince uzun çizgi
        if bw >= 0.12 * w and bh <= max(8, 0.045 * h) and bw / max(bh, 1) >= 12 and (y0 >= 0.8 * h or y1 <= 0.2 * h):
            neden = 'cizgi'
        # sol/sağ kenar kırıntısı: tüm yazının yatay aralığının dışında
        elif ((kenarR and x0 >= digx1 - 4) or (kenarL and x1 <= digx0 + 4)) and bw <= 12 and a <= 160 and (bh >= 1.5 * bw or a <= 40):
            neden = 'yan'
        # yan (2): yazıdan ≥3 px boşlukla ayrık, kenara değen, ince-uzun dikey kırıntı (kırmızı medde çubuğu vb. 'yazı aralığını' bozsa bile)
        elif (kenarL or kenarR) and bw <= 12 and bh >= 12 and bh >= 2.5 * bw and a <= 200 and not (m & ~c)[y0:y1, (slice(max(0, x0 - 3), x0) if kenarR else slice(x1, min(w, x1 + 3)))].any():
            neden = 'yan'
        # köşe: iki kenara birden değen küçük parça (yazı parçası kenarda böyle kesilmez)
        elif (kenarL + kenarR + kenarT + kenarB) >= 2 and bw <= 12 and bh <= 12 and a <= 80:
            neden = 'kose'
        # alt kenar: alttaki satırın harf uçları
        elif kenarB and 2 <= bw <= 10 and bh >= 6 and bh >= 1.5 * bw and (bosluk(m, c, x0, x1, y0, y1, 'ust') >= 5 or (bw <= 5 and bh >= 3 * bw and bh >= 10)):
            neden = 'alt'
        # üst kenar: üstteki satırın harf kuyrukları
        elif kenarT and 2 <= bw <= 10 and bh >= 6 and bh >= 1.5 * bw and bosluk(m, c, x0, x1, y0, y1, 'alt') >= 5:
            neden = 'ust'
        elif (kenarL or kenarR or kenarT or kenarB) and a <= 6 and bw <= 4 and bh <= 4:
            neden = 'kirinti'
        elif a <= 8 and bw <= 5 and bh <= 5:
            # hiçbir yazıya 8 px'ten yakın değilse
            xa, xb, ya, yb = max(0, x0 - 8), min(w, x1 + 8), max(0, y0 - 8), min(h, y1 + 8)
            yakin = (m[ya:yb, xa:xb] & ~c[ya:yb, xa:xb]).any()
            if not yakin:
                neden = 'uzak'
        if neden:
            sil[i + 1] = (neden, int(a), kutu[i])
    return arr, lab, sil, toplam


def isle(yol, uygula):
    r = analiz(yol)
    if r is None:
        return None
    arr, lab, sil, toplam = r
    if not sil:
        return None
    silinen = sum(v[1] for v in sil.values() if v[0] != 'cizgi')
    if silinen > 0.10 * toplam:
        return {'atlandi': 'cok_fazla', 'sil': sil}
    if uygula:
        arr[np.isin(lab, list(sil.keys())), 3] = 0
        Image.fromarray(arr, 'RGBA').save(yol, optimize=False)
    return {'sil': sil}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--uygula', action='store_true')
    ap.add_argument('--cuz', type=int)
    ap.add_argument('--rapor', default='/tmp/s_temizle_rapor.json')
    a = ap.parse_args()
    sonuc = []
    for c in ([a.cuz] if a.cuz else range(1, 31)):
        for y in sorted(glob.glob(f'{PAKET}/cuz{c}/img/s_*.png')):
            r = isle(y, a.uygula)
            if r:
                sonuc.append({'dosya': os.path.relpath(y, PAKET), 'atlandi': r.get('atlandi'),
                              'sil': [[v[0], v[1], list(map(int, v[2]))] for v in r['sil'].values()]})
    json.dump(sonuc, open(a.rapor, 'w'), ensure_ascii=False)
    from collections import Counter
    t = Counter()
    atl = 0
    for s in sonuc:
        atl += bool(s['atlandi'])
        for v in s['sil']:
            t[v[0]] += 1
    print('değişecek dosya:', len(sonuc), 'atlanan:', atl, dict(t))
