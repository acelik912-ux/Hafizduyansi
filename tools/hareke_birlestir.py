#!/usr/bin/env python3
"""Düzeltilmiş cuz_kes.py ile yeniden kesilen ayet görsellerini (s_/f_) mevcut paketlere birleştirir.
Neden: eski kesim, satır aralığına taşan harekeleri (örn. وَإِذَا'daki ذ üstü fetha) yanlış satıra sayıp siliyordu.
Yeni görsel ancak ESKİNİN ÜST KÜMESİ ise (eski mürekkebin >= %95'i yeni üzerinde, boyut makul) eskinin yerine konur;
elle kırpılmış / farklı kesilmiş görsellere dokunulmaz (rapora yazılır).
Kullanım: python3 tools/hareke_birlestir.py [--uygula] zip1 [zip2 ...]   (zip'ler cuz_kes.py çıktısı; cüz no project.json'dan)
"""
import argparse, io, json, os, sys, zipfile
import numpy as np
from PIL import Image
from scipy.signal import fftconvolve

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAKET = os.path.join(KOK, 'flutter_app', 'assets', 'paket')


def kirmizi_alt_sil(im):
    """Ayet başı (tek satır) görselinde yazı bandının DIŞINDA kalan küçük parçaları siler (komşu satıra ait işaret
    kırıntıları): yazının asıl bandının (satırların mürekkep yoğunluğunun >= %25'i) üstünde 0,75, altında 0,6 gövde
    yüksekliğinden uzak küçük parçalar; ayrıca yazının alt kısmındaki küçük KIRMIZI parçalar (vakıf/med işaretleri
    harfin üstünde durur, altında asla). Alfa=0 (RGB aynen)."""
    from scipy import ndimage as ndi
    arr = np.array(im.convert('RGBA'))
    a = arr[:, :, 3] > 8
    if not a.any():
        return im
    prof = a.sum(1).astype(float)
    govde = np.where(prof >= 0.25 * prof.max())[0]
    bt, bb = int(govde[0]), int(govde[-1])
    bh = max(1, bb - bt)
    kir = a & ((arr[:, :, 0].astype(int) - arr[:, :, 1]) > 60)
    lab, n = ndi.label(a, structure=np.ones((3, 3), bool))
    sil = np.zeros_like(a)
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
        if h > 45 or w > 80:
            continue
        cy = (sl[0].start + sl[0].stop) / 2
        mk = lab[sl] == i
        kirmizi = float(kir[sl][mk].mean()) > 0.5
        disarda = sl[0].stop < bt - 0.75 * bh or sl[0].start > bb + 0.6 * bh
        if disarda or (kirmizi and h <= 24 and sl[0].start > bb - 0.1 * bh):
            sil |= lab == i
    if not sil.any():
        return im
    arr[:, :, 3][sil] = 0
    return Image.fromarray(arr, 'RGBA')


def maske(im):
    return np.array(im.convert('RGBA'))[:, :, 3] > 8


def bilesenler(im):
    import collections, hashlib
    from scipy import ndimage as ndi
    m = maske(im)
    lab, n = ndi.label(m, structure=np.ones((3, 3), bool))
    out = collections.Counter()
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        c = lab[sl] == i
        out[(c.shape, hashlib.md5(np.packbits(c).tobytes()).hexdigest())] += int(c.sum())
    return out, int(m.sum())


def kapsama(eski, yeni):
    """Eskinin bileşenlerinden (harf gövdesi, nokta, hareke) yenide BİREBİR aynısı bulunanların piksel oranı:
    aynı sayfadan aynı çözünürlükte kesilmişse eski, yeninin üst kümesidir (yeni yalnızca fazladan hareke/komşu içerir)."""
    a, ta = bilesenler(eski)
    b, _ = bilesenler(yeni)
    return sum(min(v, b.get(k, 0)) for k, v in a.items()) / max(1, ta)


def kayip(eski, yeni):
    """(kayıp, toplam): eskide olup yenide birebir (aynı şekil) bulunmayan bileşenlerin sayısı ve eskinin toplam bileşen sayısı.
    Aynı çözünürlükte kesilen görsellerde eski bileşenler yenide aynen bulunmalı; bulunmayan harf/hemze/hareke kaybıdır.
    Görselin kenarına değen eski bileşenler (komşu kelime/satır kırıntıları) ve 6 px'ten küçük benekler sayılmaz."""
    import collections, hashlib
    from scipy import ndimage as ndi
    m = maske(eski)
    lab, n = ndi.label(m, structure=np.ones((3, 3), bool))
    yb, _ = bilesenler(yeni)
    kalan = collections.Counter(yb)
    H, W = m.shape
    say = tot = big = 0
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        c = lab[sl] == i
        if c.sum() < 6 or sl[0].start == 0 or sl[1].start == 0 or sl[0].stop == H or sl[1].stop == W:
            continue
        tot += 1
        key = (c.shape, hashlib.md5(np.packbits(c).tobytes()).hexdigest())
        if kalan.get(key, 0) > 0:
            kalan[key] -= 1
        else:
            say += 1
            if c.sum() >= 60:
                big += 1
    return say, tot, big


def ayni_kelime(eski, yeni):
    """Cüz 1 (eski kesim ~1,05x küçük): eski ayet başının, ölçeklenmiş hâliyle yenide ne kadarının (3 px toleransla) bulunduğu (0–1).
    Aynı kelimelerse ~0,9; farklı kelimeye kaymışsa düşük."""
    from scipy import ndimage as ndi
    n = ndi.binary_dilation(maske(yeni), iterations=3).astype(np.float32)
    en = 0.0
    a0 = maske(eski)
    for sc in (1.0, 1.02, 1.04, 1.05, 1.06, 1.08, 1.1):
        w, h = round(eski.width * sc), round(eski.height * sc)
        if h > n.shape[0] + 6 or w > n.shape[1] + 6:
            continue
        a = np.array(Image.fromarray((a0 * 255).astype(np.uint8)).resize((w, h), Image.BILINEAR)) > 100
        if a.sum() == 0:
            continue
        pad = np.pad(n, ((h, h), (w, w)))
        c = fftconvolve(pad, a[::-1, ::-1].astype(np.float32), mode='valid')
        en = max(en, float(c.max()) / float(a.sum()))
    return en


def kayip_ok(eski, yeni):
    k, t, big = kayip(eski, yeni)
    return big == 0 and k <= max(0, int(0.03 * t))


def ustkume(eski, yeni):
    """(kapsama, dx, dy): eski görselin mürekkebi yeninin içinde en iyi hizada ne kadar bulunuyor."""
    a, b = maske(eski), maske(yeni)
    if a.sum() == 0:
        return 0.0, 0, 0
    if a.shape[0] > b.shape[0] + 4 or a.shape[1] > b.shape[1] + 4:
        return 0.0, 0, 0
    ker = a[::-1, ::-1].astype(np.float32)
    c = fftconvolve(b.astype(np.float32), ker, mode='full')
    iy, ix = np.unravel_index(int(np.argmax(c)), c.shape)
    return float(c[iy, ix]) / float(a.sum()), ix - (a.shape[1] - 1), iy - (a.shape[0] - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--uygula', action='store_true')
    ap.add_argument('--rapor')
    ap.add_argument('--atla', default='', help="dokunulmayacak ayetler, ör. '1:1,1:2,2:1' (elle hazırlanmış büyük özel görseller)")
    ap.add_argument('--gevsek', type=int, nargs='*', default=[], help='boyut uyumuyla kabul edilecek cüzler (örn. 1)')
    ap.add_argument('zips', nargs='+')
    o = ap.parse_args()
    yeni = {}  # cüz -> {(sura,no): {'s': bytes, 'f': bytes}}, ve rects
    rects = {}
    cuzno = None
    for zp in o.zips:
        z = zipfile.ZipFile(zp)
        pj = json.loads(z.read('project.json'))
        c = pj['cuz']
        d = yeni.setdefault(c, {})
        for pg in pj['pages']:
            for a in pg['ayat']:
                d[(a['sura'], a['no'])] = {'s': z.read(a['start']['file']), 'f': z.read(a['full']['file'])}
            rects.setdefault(c, {})[tuple((r['sura'], r['no']) for r in pg['sheets'][0]['rects'])] = pg['sheets'][0]['rects']
    rapor = []
    for c, d in sorted(yeni.items()):
        pdir = os.path.join(PAKET, f'cuz{c}')
        pjp = os.path.join(pdir, 'project.json')
        pj = json.load(open(pjp, encoding='utf-8'))
        say = dict(kabul=0, ayni=0, ret=0, yok=0)
        for pg in pj['pages']:
            for a in pg['ayat']:
                k = (a['sura'], a['no'])
                if f"{k[0]}:{k[1]}" in o.atla.split(','):
                    say['atla'] = say.get('atla', 0) + 1
                    continue
                if k not in d:
                    say['yok'] += 1
                    rapor.append((c, k, 'yok', 0))
                    continue
                for tur, anah in (('s', 'start'), ('f', 'full')):
                    yol = os.path.join(pdir, a[anah]['file'])
                    eski = Image.open(yol)
                    yenim = Image.open(io.BytesIO(d[k][tur]))
                    if tur == 's':
                        yenim2 = kirmizi_alt_sil(yenim)
                        if yenim2 is not yenim:
                            b = io.BytesIO(); yenim2.save(b, 'PNG', optimize=True); d[k][tur] = b.getvalue(); yenim = yenim2
                    kap = kapsama(eski, yenim)
                    buyume = (yenim.width - eski.width, yenim.height - eski.height)
                    ayni = yenim.size == eski.size and np.array_equal(maske(eski), maske(yenim))
                    if ayni:
                        say['ayni'] += 1
                        continue
                    ok = kap >= 0.85 and kayip_ok(eski, yenim) and -10 <= buyume[0] <= 80 and (-4 if kap < 0.97 else -60) <= buyume[1] <= 0.6 * eski.height + 40
                    if c in o.gevsek and tur == 'f' and kap < 0.85:
                        ok = False  # eski kesimle ölçek farkı: harf kaybı denetlenemez, eski tam ayet görseli korunur
                    elif not ok and c in o.gevsek and kap < 0.85:
                        # eski kesim başka çözünürlükte/başka kelime seçimiyle yapılmış (1. cüz): yalnızca boyut uyumuna bakılır
                        oran_w, oran_h = yenim.width / eski.width, yenim.height / eski.height
                        ok = (0.75 <= oran_w <= 1.25 and 0.8 <= oran_h <= 1.35) if tur == 's' else (0.75 <= oran_h <= 1.4)
                        if ok and tur == 's' and ayni_kelime(eski, yenim) < 0.8:
                            ok = False
                    if not ok:
                        say['ret'] += 1
                        rapor.append((c, k, tur + ' ret', round(kap, 3), buyume))
                        continue
                    say['kabul'] += 1
                    if o.uygula:
                        open(yol, 'wb').write(d[k][tur])
                        a[anah]['w'], a[anah]['h'] = yenim.size
        # sayfa dikdörtgenleri (ezber kapağı): aynı ayet dizisi ise yenisi
        if o.uygula:
            for pg in pj['pages']:
                sh = pg['sheets'][0]
                an = tuple((r['sura'], r['no']) for r in sh['rects'])
                if an in rects.get(c, {}):
                    sh['rects'] = rects[c][an]
            json.dump(pj, open(pjp, 'w', encoding='utf-8'), ensure_ascii=False)
        print(f'cuz{c}: {say}')
    if o.rapor:
        json.dump(rapor, open(o.rapor, 'w'), ensure_ascii=False, indent=0)
    print(f'rapor: {len(rapor)} kayıt')


main()
