#!/usr/bin/env python3
"""3. cüz kuşlarını kullanıcının görsellerinden kurar (theme3: kuş bahçesi). Yeniden çizmez; yalnız arka planı siler, boyutlandırır ve yerleştirir.

    python3 tools/kus_gorsel.py [onizleme_klasoru]   # tools/kus_kaynak/NN_ad.png -> bundle/theme3.pNN
    python3 tools/flutter_varlik.py                  # paketi flutter_app/assets/paket/theme3 altına açar

Sıra, 3. cüzün sayfa sırasıdır (sayfa 3 = 2:260 İbrahim'in dört kuşu -> Güvercin; sayfa 7 = 2:282 tek ayetli -> Anka).
Görsellerin bir kısmı ahşap tarhlı ('tarh'), bir kısmı tek başına kuş ('tek'). Tek kuşlar gerçek büyüklüklerine göre
ölçeklenir (md = en büyük kenar, px) ve yere oturur; uçan kuşlar 'yuk' kadar yerden yüksekte durur.
Tuval 1080x1440, dibi y=1425 (ağaç/maden görselleriyle aynı)."""
import io, json, os, sys, zipfile
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_gorsel as mg

KAYNAK = os.path.join(KOK, 'tools', 'kus_kaynak')
# (ad, tür, md, yük, arka plan)   tür: tarh | tek ; arka plan: beyaz | gri | delik (beyaz + bacak aralarındaki kapalı beyaz boşluklar)
KUSLAR = [
    ('Kartal', 'tarh', 0, 0, 'beyaz'), ('Şahin', 'tarh', 0, 0, 'beyaz'), ('Güvercin', 'tarh', 0, 0, 'beyaz'),
    ('Altın Sülün', 'tarh', 0, 0, 'beyaz'), ('Tavus', 'tarh', 0, 0, 'beyaz'),
    ('Keklik', 'tek', 640, 0, 'delik'), ('Anka', 'tek', 1130, 0, 'beyaz'), ('Hüthüt', 'tek', 700, 0, 'beyaz'),
    ('Puhu', 'tek', 960, 0, 'beyaz'), ('Tukan', 'tek', 1000, 0, 'beyaz'), ('Kırmızı Papağan', 'tek', 1130, 0, 'beyaz'),
    ('Pelikan', 'tek', 1130, 0, 'beyaz'), ('Ağaçkakan', 'tek', 1130, 0, 'beyaz'), ('Flamingo', 'tek', 1140, 0, 'delik'),
    ('Kolibri', 'tek', 520, 260, 'beyaz'), ('Saka', 'tek', 560, 0, 'beyaz'), ('Bülbül', 'tek', 1000, 0, 'gri'),
    ('Kerkenez', 'tek', 700, 230, 'beyaz'), ('Atmaca', 'tek', 480, 0, 'beyaz'), ('Leylek', 'tek', 1130, 0, 'beyaz'),
]
ADLAR = [k[0] for k in KUSLAR]


def kaynak_yolu(i):
    on = '%02d_' % (i + 1)
    for f in sorted(os.listdir(KAYNAK)):
        if f.startswith(on):
            return os.path.join(KAYNAK, f)
    return None


def gri_sil(im):
    """açık gri/beyaz gökyüzü zemini (bülbül): kenara bağlı olanı ve dallar arasında kalan büyük boşlukları sil, tek parça kuşu bırak"""
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    mn = a.min(axis=2)
    sat = a.max(axis=2) - mn
    aday = (mn >= 222) & (sat < 16)
    lab, n = ndi.label(aday)
    boy = ndi.sum(aday, lab, range(1, n + 1))
    kenar = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    zemin = np.isin(lab, [k for k in kenar] + [k + 1 for k, b in enumerate(boy) if b > 3000])
    on = ndi.binary_opening(~zemin, iterations=1)
    lab2, n2 = ndi.label(on)
    boy2 = ndi.sum(on, lab2, range(1, n2 + 1))
    on = np.isin(lab2, [k + 1 for k, b in enumerate(boy2) if b >= 0.12 * boy2.max()])  # uzaktaki yaprak/dal parçalarını at
    ic = ndi.binary_erosion(on, iterations=2)
    alfa = np.clip((ndi.gaussian_filter(on.astype(np.float32), 0.9) - 0.25) / 0.6, 0, 1)
    idx = ndi.distance_transform_edt(~ic, return_distances=False, return_indices=True)
    rgb = np.where(ic[..., None], a, a[idx[0], idx[1]])
    return Image.fromarray(np.dstack([rgb, alfa * 255]).clip(0, 255).astype(np.uint8), 'RGBA')


def delik_sil(im):
    """beyaz zemini sil, ayrıca kuşun içinde kalan (bacak arası) saf beyaz boşlukları da sil"""
    im = mg.beyaz_sil(im)
    a = np.asarray(im).astype(np.float32)
    beyaz = (a[..., :3].min(axis=2) >= 250) & (a[..., 3] > 8)
    lab, n = ndi.label(beyaz)
    boy = ndi.sum(beyaz, lab, range(1, n + 1))
    sil = np.isin(lab, [k + 1 for k, b in enumerate(boy) if b > 1500])
    golge = (a[..., :3].min(axis=2) >= 235) & (a[..., :3].max(axis=2) - a[..., :3].min(axis=2) < 8) & (a[..., 3] > 8)  # yerdeki açık gölge/leke
    lab2, n2 = ndi.label(golge)
    boy2 = ndi.sum(golge, lab2, range(1, n2 + 1))
    sil |= np.isin(lab2, [k + 1 for k, b in enumerate(boy2) if b > 150])
    a[..., 3] = np.where(sil, 0, a[..., 3])
    return Image.fromarray(a.astype(np.uint8), 'RGBA')


def yerlestir(im, tur, md, yuk):
    if tur == 'tarh':
        return mg.yerlestir(im)
    b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(b)
    s = md / max(im.size)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    if im.width > mg.MAXW:
        im = im.resize((mg.MAXW, round(im.height * mg.MAXW / im.width)), Image.LANCZOS)
    tuval = Image.new('RGBA', (mg.CW, mg.CH), (0, 0, 0, 0))
    tuval.alpha_composite(im, ((mg.CW - im.width) // 2, mg.TABAN - yuk - im.height))
    return tuval


def ikon(im, tur, n=384):
    """kuşun kendi küçük görseli (tarhlılarda kutunun üstündeki bölüm), kare tuvale ortalanır"""
    b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    if tur == 'tarh':
        im = im.crop((b[0], b[1], b[2], b[1] + int((b[3] - b[1]) * 0.66)))
    else:
        im = im.crop(b)
    b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
    im = im.crop(b)
    s = (n * 0.9) / max(im.size)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    t = Image.new('RGBA', (n, n), (0, 0, 0, 0))
    t.alpha_composite(im, ((n - im.width) // 2, (n - im.height) // 2))
    return t


def main():
    resimler, ikonlar = [], []
    for i, (ad, tur, md, yuk, zemin) in enumerate(KUSLAR):
        yol = kaynak_yolu(i)
        if not yol:
            sys.exit('eksik görsel: %02d_… (tools/kus_kaynak/) -> %s' % (i + 1, ad))
        src = Image.open(yol)
        im = gri_sil(src) if zemin == 'gri' else delik_sil(src) if zemin == 'delik' else mg.beyaz_sil(src)
        resimler.append(yerlestir(im, tur, md, yuk))
        b = im.getchannel('A').point(lambda v: 255 if v > 8 else 0).getbbox()
        ikonlar.append(ikon(im, tur))
    proje = {'version': 7, 'kind': 'theme', 'cuz': 3, 'name': 'Kuşlar (3. Cüz)', 'sahne': 'kus', 'ek': '', 'birim': 'kuş',
             'tanim': 'kuşlar bahçesi', 'ui': {}, 'trees': {}}
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for i, im in enumerate(resimler):
            d = 'kus%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': mg.CW, 'h': mg.CH, 'name': ADLAR[i]}
            b = io.BytesIO(); ikonlar[i].save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    bundle = os.path.join(KOK, 'bundle')
    for f in os.listdir(bundle):
        if f.startswith('theme3.p'):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme3.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme3: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'kus%02d.png' % (i + 1)))


if __name__ == '__main__':
    main()
