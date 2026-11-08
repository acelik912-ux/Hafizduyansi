#!/usr/bin/env python3
"""11. cüz (Tevbe 9:94 – Hûd 11:5) görsellerini kullanıcının görsellerinden kurar (theme19: sahil sahnesi). Yeniden çizmez;
yalnız beyaz zemini siler, boyutlandırır ve yerleştirir. Arka planlar (bg/) mevcut theme19 paketinden korunur.

    python3 tools/c19_gorsel.py [onizleme_klasoru]   # tools/c19_kaynak/NN_ad.png -> bundle/theme19.pNN
    python3 tools/flutter_varlik.py

Kipler: kure (kenardan beyaz sil + halka içi boşluklar) | bulut (yalnız kenardan) | parla (parlayan/yarı saydam nesne:
beyaza göre alfa çıkarılır, çekirdek beyaz kalır: şimşek, kıvılcım, gökkuşağı) | govde (hortum: baştan kalma gri gölge de silinir)
| oval (galaksi: kesik dikdörtgen kenarı oval yumuşatılır) | kar (kar tanesi: dallar arası beyaz boşluk silinir)."""
import glob, io, json, os, sys, zipfile
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_gorsel as mg
import kus_gorsel as kg

KAYNAK = os.path.join(KOK, 'tools', 'c19_kaynak')
# (ad, kip, md, yük)
ESYALAR = [
    ('Elhamra Sarayı', 'buz', 1000, 0),
    ('Topkapı Sarayı', 'buz', 1000, 0),
    ('Dolmabahçe Sarayı', 'buz', 1000, 0),
    ('Yıldız Sarayı', 'buz', 1000, 0),
    ('Çırağan Sarayı', 'buz', 1000, 0),
    ('İshak Paşa Sarayı', 'buz', 1000, 0),
    ('Âli Kapı Sarayı', 'buz', 1000, 0),
    ('Çehel Sütun Sarayı', 'buz', 1000, 0),
    ('Şirvanşahlar Sarayı', 'buz', 1000, 0),
    ('Lahor Kalesi ve Sarayı', 'buz', 1000, 0),
    ('Bahia Sarayı', 'buz', 1000, 0),
    ('Azem Sarayı', 'buz', 1000, 0),
    ('El Vatan Sarayı', 'buz', 1000, 0),
    ('Yasak Şehir', 'buz', 1000, 0),
    ('Himeji Kalesi ve Sarayı', 'buz', 1000, 0),
    ('Schönbrunn Sarayı', 'buz', 1000, 0),
    ('Buckingham Sarayı', 'buz', 1000, 0),
    ('Pena Sarayı', 'buz', 1000, 0),
    ('Neuschwanstein Sarayı', 'buz', 1000, 0),
    ('Kremlin Sarayı', 'buz', 1000, 0),
]
ADLAR = [e[0] for e in ESYALAR]


def kenar_bagli(maske):
    lab, n = ndi.label(maske)
    k = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(k))


def parla(im, kazanc, cekirdek=True, renk=(255, 255, 255), acik=0.0):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    mn = a.min(axis=2)
    dis = kenar_bagli(mn >= 250)
    ap = (255 - a).max(axis=2) / 255.0
    ap_g = np.maximum(ap, 1e-3)[..., None]
    rgb = np.clip((a - 255 * (1 - ap_g)) / ap_g, 0, 255)
    alfa = np.clip(ap * kazanc, 0, 1)
    alfa[dis] = 0
    if cekirdek:
        c = (mn >= 250) & ~dis
        lab, n = ndi.label(c)
        boy = ndi.sum(c, lab, range(1, n + 1))
        c = np.isin(lab, [k + 1 for k, b in enumerate(boy) if b < 600])  # büyük beyaz boşluklar çekirdek değil
        c = ndi.binary_dilation(c, iterations=1)
        alfa = np.where(c, 1.0, alfa)
        rgb = np.where(c[..., None], np.array(renk, np.float32), rgb)
    if acik:  # koyu gökte parlak görünsün: renk beyaza doğru açılır
        rgb = rgb * (1 - acik) + np.array(renk, np.float32) * acik
    return Image.fromarray(np.dstack([rgb, alfa * 255]).clip(0, 255).astype(np.uint8), 'RGBA')


def govde(im):
    """kenardan beyaz VE nötr gri/siyah gölge (doygunluk çok düşük) silinir; gövde (mavi-gri) korunur"""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    mn, mx = a.min(axis=2), a.max(axis=2)
    aday = (mn >= 247) | ((mx - mn) < 7)
    zemin = kenar_bagli(aday)
    zemin = ndi.binary_dilation(zemin, iterations=1) & ((mx - mn) < 14)
    on = ~zemin
    lab, n = ndi.label(on)
    boy = ndi.sum(on, lab, range(1, n + 1))
    on = np.isin(lab, [k + 1 for k, b in enumerate(boy) if b >= 400])
    alfa = ndi.gaussian_filter(on.astype(np.float32), 0.9)
    alfa = np.clip((alfa - 0.25) / 0.6, 0, 1)
    ic = ndi.binary_erosion(on, iterations=2)
    idx = ndi.distance_transform_edt(~ic, return_distances=False, return_indices=True)
    rgb = np.where(ic[..., None], a, a[idx[0], idx[1]])
    return Image.fromarray(np.dstack([rgb, alfa * 255]).clip(0, 255).astype(np.uint8), 'RGBA')


def oval(im):
    im = mg.beyaz_sil(im)
    a = np.asarray(im).astype(np.float32)
    b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    rx, ry = (b[2] - b[0]) / 2, (b[3] - b[1]) / 2
    y, x = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    r = np.sqrt(((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2)
    m = np.clip((1.0 - r) / 0.16, 0, 1)
    m = m * m * (3 - 2 * m)
    a[..., 3] *= m
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')


def kar(im):
    im = mg.beyaz_sil(im)
    a = np.asarray(im).astype(np.float32)
    beyaz = (a[..., :3].min(axis=2) >= 246) & (a[..., 3] > 8)
    lab, n = ndi.label(beyaz)
    boy = ndi.sum(beyaz, lab, range(1, n + 1))
    sil = np.isin(lab, [k + 1 for k, b in enumerate(boy) if b >= 25])
    a[..., 3] = np.where(sil, 0, a[..., 3])
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def buz(im):
    """beyaza yakın nesneler (kar, buz): yalnız saf beyaz (>=252) kenardan silinir, kenar 1 px yumuşatılır"""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    mn, mx = a.min(axis=2), a.max(axis=2)
    zemin = kenar_bagli((mn >= 252) & (mx - mn < 5))
    on = ~zemin
    lab, n = ndi.label(on)
    boy = ndi.sum(on, lab, range(1, n + 1))
    on = np.isin(lab, [k + 1 for k, b in enumerate(boy) if b >= 400])
    alfa = np.clip((ndi.gaussian_filter(on.astype(np.float32), 0.8) - 0.3) / 0.5, 0, 1)
    return Image.fromarray(np.dstack([a, alfa * 255]).clip(0, 255).astype(np.uint8), 'RGBA')


def kart(im):
    """dikdörtgen resim (kenardan beyaz silinir): köşeleri yuvarlanır, kenar yumuşatılır"""
    im = mg.beyaz_sil(im)
    a = np.asarray(im).astype(np.float32)
    b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    x0, y0, x1, y1 = b
    y, x = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    r = 70.0
    dx = np.maximum(np.maximum(x0 + r - x, x - (x1 - r)), 0)
    dy = np.maximum(np.maximum(y0 + r - y, y - (y1 - r)), 0)
    d = np.sqrt(dx ** 2 + dy ** 2)
    m = np.clip((r - d) / 3.0 + 0.5, 0, 1)
    a[..., 3] *= m
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')


def yer_golgesi(im):
    """delik_sil + ayakların altındaki açık mavi/nötr yer gölgesi silinir: en alttaki koyu (gövde) satırın altı kesilir,
    ayak hizasındaki açık, kırmızıdan mavi olmayan pikseller de atılır (fildişi tırnaklar kalır)"""
    im = kg.delik_sil(im)
    a = np.asarray(im).astype(np.float32)
    rgb = a[..., :3]
    mn, mx = rgb.min(axis=2), rgb.max(axis=2)
    koyu = (mn < 140) & (a[..., 3] > 200)
    satir = np.where(koyu.sum(axis=1) > 12)[0]
    yf = int(satir.max())
    y = np.arange(a.shape[0])[:, None] * np.ones((1, a.shape[1]))
    sil = y > yf + 5
    acik = (mn >= 150) & (rgb[..., 2] >= rgb[..., 0] - 4) & (mx - mn < 70) & (y > yf - 70)
    sil |= acik
    a[..., 3] = np.where(sil, 0, a[..., 3])
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def kucuk_sil(im):
    """ana nesneden kopuk küçük parçaları (gölge kalıntısı) siler"""
    a = np.asarray(im).copy()
    on = a[..., 3] > 20
    lab, n = ndi.label(on)
    if n > 1:
        boy = ndi.sum(on, lab, range(1, n + 1))
        tut = [k + 1 for k, b in enumerate(boy) if b >= 0.05 * boy.max()]
        a[..., 3] = np.where(np.isin(lab, tut), a[..., 3], 0)
    return Image.fromarray(a, 'RGBA')


def isle(im, kip):
    if kip == 'balik':
        return kucuk_sil(mg.beyaz_sil(im, golge=True))
    if kip == 'kestane':
        r = np.asarray(parla(im, 1.25, cekirdek=True, renk=(25, 18, 25))).copy()
        r[..., 3] = np.where(r[..., 3] < 40, 0, r[..., 3])  # zeminin çok açık dikdörtgen izi
        return Image.fromarray(r, 'RGBA')
    if kip == 'dag':
        return mg.beyaz_sil(im)
    if kip == 'buz':
        return kucuk_sil(buz(im))  # alttaki yazı ve kopuk parçalar atılır
    if kip == 'kart':
        return kart(im)
    if kip == 'golge':
        return yer_golgesi(im)
    if kip == 'bacak':
        return kg.delik_sil(im)
    if kip == 'hayvan':
        return mg.beyaz_sil(im, golge=True)
    if kip == 'kure':
        return mg.beyaz_sil(im)
    if kip == 'halka':
        return kg.delik_sil(im)
    if kip == 'bulut':
        return mg.beyaz_sil(im)
    if kip == 'parla':
        return None  # ada göre
    if kip == 'govde':
        return govde(im)
    if kip == 'oval':
        return oval(im)
    if kip == 'kar':
        return kar(im)
    raise ValueError(kip)


def kaynak_yolu(i):
    on = '%02d_' % (i + 1)
    for f in sorted(os.listdir(KAYNAK)):
        if f.startswith(on):
            return os.path.join(KAYNAK, f)
    return None


def main():
    bundle = os.path.join(KOK, 'bundle')
    eski = b''.join(open(f, 'rb').read() for f in sorted(glob.glob(os.path.join(bundle, 'theme19.p*'))))
    ez = zipfile.ZipFile(io.BytesIO(eski))
    proje = json.loads(ez.read('project.json'))
    bgler = {n: ez.read(n) for n in ez.namelist() if n.startswith('bg/')}
    proje['trees'] = {}
    proje['name'] = 'Saraylar (19. Cüz)'
    proje['tanim'] = 'saraylar'
    proje['birim'] = 'saray'
    resimler, ikonlar = [], []
    for i, (ad, kip, md, yuk) in enumerate(ESYALAR):
        yol = kaynak_yolu(i)
        if not yol:
            sys.exit('eksik görsel: %02d_… (tools/c19_kaynak/) -> %s' % (i + 1, ad))
        kaynak = Image.open(yol)
        im = isle(kaynak, kip)
        resimler.append(kg.yerlestir(im, 'tek', md, yuk))
        ikonlar.append(kg.ikon(im, 'tek'))
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for n, b in bgler.items():
            z.writestr(n, b)
        for i, im in enumerate(resimler):
            d = 'c19_%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': mg.CW, 'h': mg.CH, 'name': ADLAR[i]}
            b = io.BytesIO(); ikonlar[i].save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    for f in os.listdir(bundle):
        if f.startswith('theme19.p'):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme19.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme19: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'c19_%02d.png' % (i + 1)))


if __name__ == '__main__':
    main()
