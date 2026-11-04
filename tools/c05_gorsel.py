#!/usr/bin/env python3
"""5. cüz (Nisâ 4:24 – 4:147) görsellerini kullanıcının görsellerinden kurar (theme5: ova sahnesi). Yeniden çizmez;
yalnız beyaz zemini siler, boyutlandırır ve yerleştirir. Arka planlar (bg/) mevcut theme5 paketinden korunur.

    python3 tools/c05_gorsel.py [onizleme_klasoru]   # tools/c05_kaynak/NN_ad.png -> bundle/theme5.pNN
    python3 tools/flutter_varlik.py

Sıra, 12. cüzün sayfa sırasıdır (sayfa 1 = 11:6-12 ... sayfa 20 = 12:44-52). Hepsi tek başına nesne ('tek')."""
import glob, io, json, os, sys, zipfile
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_gorsel as mg
import kus_gorsel as kg

KAYNAK = os.path.join(KOK, 'tools', 'c05_kaynak')
# (ad, md, yük)
ESYALAR = [
    ('Maydanoz', 950, 0),
    ('Havuç', 1000, 0),
    ('Pancar', 1000, 0),
    ('Pirinç', 950, 0),
    ('Kabak', 950, 0),
    ('Böğürtlen', 1000, 0),
    ('Buğday', 950, 0),
    ('Mercimek', 950, 0),
    ('Sarımsak', 900, 0),
    ('Soğan', 900, 0),
    ('Bezelye', 1000, 0),
    ('Nohut', 1000, 0),
    ('Hardal', 1000, 0),
    ('Balkabağı', 950, 0),
    ('Zencefil', 1000, 0),
    ('Patlıcan', 1000, 0),
    ('Domates', 1000, 0),
    ('Salatalık', 1000, 0),
    ('Biber', 1000, 0),
    ('Patates', 1000, 0),
]
# açık/beyaz nesneler (pirinç, mercimek, sarımsak, soğan, buğday, zencefil): yalnız kenardan beyaz silinir; bitkilerde yaprak arası boşluklar da silinir
BEYAZ = {4, 8, 9, 10, 15}
ADLAR = [e[0] for e in ESYALAR]


def kaynak_yolu(i):
    on = '%02d_' % (i + 1)
    for f in sorted(os.listdir(KAYNAK)):
        if f.startswith(on):
            return os.path.join(KAYNAK, f)
    return None


def main():
    bundle = os.path.join(KOK, 'bundle')
    eski = b''.join(open(f, 'rb').read() for f in sorted(glob.glob(os.path.join(bundle, 'theme5.p*'))))
    ez = zipfile.ZipFile(io.BytesIO(eski))
    proje = json.loads(ez.read('project.json'))
    bgler = {n: ez.read(n) for n in ez.namelist() if n.startswith('bg/')}
    proje['trees'] = {}
    resimler, ikonlar = [], []
    for i, (ad, md, yuk) in enumerate(ESYALAR):
        yol = kaynak_yolu(i)
        if not yol:
            sys.exit('eksik görsel: %02d_… (tools/c05_kaynak/) -> %s' % (i + 1, ad))
        kaynak = Image.open(yol)
        im = mg.beyaz_sil(kaynak, golge=True) if (i + 1) in BEYAZ else kg.delik_sil(kaynak)
        resimler.append(kg.yerlestir(im, 'tek', md, yuk))
        ikonlar.append(kg.ikon(im, 'tek'))
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for n, b in bgler.items():
            z.writestr(n, b)
        for i, im in enumerate(resimler):
            d = 'c05_%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': mg.CW, 'h': mg.CH, 'name': ADLAR[i]}
            b = io.BytesIO(); ikonlar[i].save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    for f in os.listdir(bundle):
        if f.startswith('theme5.p'):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme5.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme5: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'c05_%02d.png' % (i + 1)))


if __name__ == '__main__':
    main()
