#!/usr/bin/env python3
"""6. cüz (Nisâ 4:148 – Mâide 5:82) görsellerini kullanıcının görsellerinden kurar (theme6: orman sahnesi). Yeniden çizmez;
yalnız beyaz zemini siler, boyutlandırır ve yerleştirir. Arka planlar (bg/) mevcut theme6 paketinden korunur.

    python3 tools/c06_gorsel.py [onizleme_klasoru]   # tools/c06_kaynak/NN_ad.png -> bundle/theme6.pNN
    python3 tools/flutter_varlik.py

Sıra, 12. cüzün sayfa sırasıdır (sayfa 1 = 11:6-12 ... sayfa 20 = 12:44-52). Hepsi tek başına nesne ('tek')."""
import glob, io, json, os, sys, zipfile
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_gorsel as mg
import kus_gorsel as kg

KAYNAK = os.path.join(KOK, 'tools', 'c06_kaynak')
# (ad, md, yük)
ESYALAR = [
    ('Hünnap', 1000, 0),
    ('Ceviz', 1000, 0),
    ('Kızılcık', 1000, 0),
    ('Limon', 1000, 0),
    ('Kestane', 1000, 0),
    ('Mango', 1000, 0),
    ('Alıç', 1000, 0),
    ('Hindistan Cevizi', 1200, 0),
    ('Portakal', 1000, 0),
    ('Fındık', 1000, 0),
    ('Yaban Mersini', 1000, 0),
    ('Avokado', 1000, 0),
    ('Kaju', 1000, 0),
    ('Keçiboynuzu', 1000, 0),
    ('Mandalina', 1000, 0),
    ('Liçi', 1000, 0),
    ('Kahve', 1000, 0),
    ('Muşmula', 1000, 0),
    ('Ekmek Ağacı', 1000, 0),
    ('Kakao', 1000, 0),
]
BEYAZ = set()
SIKI_YOK = {7}  # Alıç: beyaz çiçekler silinmesin


def yaprak_arasi_sil(im):
    """delik_sil + yaprak aralarında kalan küçük beyaz yarıklar (düşük doygunluk, çok açık) da silinir, kenar 1 px yumuşatılır"""
    import numpy as np
    from scipy import ndimage as ndi
    im = kg.delik_sil(im)
    a = np.asarray(im).astype(np.float32)
    rgb = a[..., :3]
    mn, mx = rgb.min(axis=2), rgb.max(axis=2)
    aday = (mn >= 232) & (mx - mn < 22) & (a[..., 3] > 8)
    lab, n = ndi.label(aday)
    boy = ndi.sum(aday, lab, range(1, n + 1))
    sil = np.isin(lab, [k + 1 for k, b in enumerate(boy) if b >= 6])
    sil = ndi.binary_dilation(sil, iterations=1) & (mn >= 200)
    a[..., 3] = np.where(sil, 0, a[..., 3])
    return Image.fromarray(a.astype(np.uint8), 'RGBA')

ADLAR = [e[0] for e in ESYALAR]


def kaynak_yolu(i):
    on = '%02d_' % (i + 1)
    for f in sorted(os.listdir(KAYNAK)):
        if f.startswith(on):
            return os.path.join(KAYNAK, f)
    return None


def main():
    bundle = os.path.join(KOK, 'bundle')
    eski = b''.join(open(f, 'rb').read() for f in sorted(glob.glob(os.path.join(bundle, 'theme6.p*'))))
    ez = zipfile.ZipFile(io.BytesIO(eski))
    proje = json.loads(ez.read('project.json'))
    bgler = {n: ez.read(n) for n in ez.namelist() if n.startswith('bg/')}
    proje['trees'] = {}
    resimler, ikonlar = [], []
    for i, (ad, md, yuk) in enumerate(ESYALAR):
        yol = kaynak_yolu(i)
        if not yol:
            sys.exit('eksik görsel: %02d_… (tools/c06_kaynak/) -> %s' % (i + 1, ad))
        kaynak = Image.open(yol)
        im = mg.beyaz_sil(kaynak, golge=True) if (i + 1) in BEYAZ else (kg.delik_sil(kaynak) if (i + 1) in SIKI_YOK else yaprak_arasi_sil(kaynak))
        resimler.append(kg.yerlestir(im, 'tek', md, yuk))
        ikonlar.append(kg.ikon(im, 'tek'))
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for n, b in bgler.items():
            z.writestr(n, b)
        for i, im in enumerate(resimler):
            d = 'c06_%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': mg.CW, 'h': mg.CH, 'name': ADLAR[i]}
            b = io.BytesIO(); ikonlar[i].save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    for f in os.listdir(bundle):
        if f.startswith('theme6.p'):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme6.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme6: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'c06_%02d.png' % (i + 1)))


if __name__ == '__main__':
    main()
