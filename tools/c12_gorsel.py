#!/usr/bin/env python3
"""12. cüz (Hûd 11:6 – Yûsuf 12:52) görsellerini kullanıcının görsellerinden kurar (theme12: çöl sahnesi). Yeniden çizmez;
yalnız beyaz zemini siler, boyutlandırır ve yerleştirir. Arka planlar (bg/) mevcut theme12 paketinden korunur.

    python3 tools/c12_gorsel.py [onizleme_klasoru]   # tools/c12_kaynak/NN_ad.jpg -> bundle/theme12.pNN
    python3 tools/flutter_varlik.py

Sıra, 12. cüzün sayfa sırasıdır (sayfa 1 = 11:6-12 ... sayfa 20 = 12:44-52). Hepsi tek başına nesne ('tek')."""
import glob, io, json, os, sys, zipfile
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_gorsel as mg
import kus_gorsel as kg

KAYNAK = os.path.join(KOK, 'tools', 'c12_kaynak')
# (ad, md, yük)
ESYALAR = [
    ('Mercan Kayalığı', 1000, 0), ('Altın Hazine Sandığı', 1000, 0), ('Gemi Tezgâhı', 1000, 0), ('Tandır', 900, 0),
    ('Tufan ve Gemi', 1000, 0), ('Cûdî Dağı ve Gemi', 1000, 0), ('Âd Sütunları', 1000, 0), ('Semûd Kayaları', 980, 0),
    ('Kızartılmış Buzağı', 1000, 0), ('Lût’un Yıkılan Şehri', 1000, 0), ('Ölçü ve Terazi', 1000, 0), ('Firavun Dikilitaşı', 1000, 0),
    ('Güneş Saati', 960, 0), ('Güneş, Ay ve Yıldızlar', 900, 220), ('Yûsuf’un Kuyusu', 1000, 0), ('Dirhem Kesesi ve Sandık', 1000, 0),
    ('Kapalı Kapı', 960, 0), ('Ekmek ve Üzüm', 1000, 0), ('Yedi Başak', 1000, 0), ('Buğday Çuvalları', 1000, 0),
]
ADLAR = [e[0] for e in ESYALAR]


def kaynak_yolu(i):
    on = '%02d_' % (i + 1)
    for f in sorted(os.listdir(KAYNAK)):
        if f.startswith(on):
            return os.path.join(KAYNAK, f)
    return None


def main():
    bundle = os.path.join(KOK, 'bundle')
    eski = b''.join(open(f, 'rb').read() for f in sorted(glob.glob(os.path.join(bundle, 'theme12.p*'))))
    ez = zipfile.ZipFile(io.BytesIO(eski))
    proje = json.loads(ez.read('project.json'))
    # arka planlar: tools/sahne_bg.py misir (piramitli çöl) -> bg/misir_sayfa.jpg, bg/misir_kemer.jpg
    import subprocess, tempfile
    gecici = tempfile.mkdtemp()
    subprocess.check_call([sys.executable, os.path.join(KOK, 'tools', 'sahne_bg.py'), gecici, 'misir'])
    bgler = {'bg/misir_sayfa.jpg': open(os.path.join(gecici, 'misir_sayfa.jpg'), 'rb').read(),
             'bg/misir_kemer.jpg': open(os.path.join(gecici, 'misir_kemer.jpg'), 'rb').read()}
    proje['sahne'] = 'misir'
    proje['ui'] = {'bgGarden': 'misir_sayfa.jpg', 'bgForest': 'misir_sayfa.jpg', 'bgPage': 'misir_sayfa.jpg', 'bgAyet': 'misir_kemer.jpg'}
    proje.update({'name': 'Hûd ve Yûsuf (12. Cüz)', 'tanim': 'Hûd ve Yûsuf kıssaları', 'birim': 'nişan', 'trees': {}})
    resimler, ikonlar = [], []
    for i, (ad, md, yuk) in enumerate(ESYALAR):
        yol = kaynak_yolu(i)
        if not yol:
            sys.exit('eksik görsel: %02d_… (tools/c12_kaynak/) -> %s' % (i + 1, ad))
        im = mg.beyaz_sil(Image.open(yol), golge=(i != 13))  # bulutlu Güneş-Ay açık renkli: gölge silme kapalı
        resimler.append(kg.yerlestir(im, 'tek', md, yuk))
        ikonlar.append(kg.ikon(im, 'tek'))
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for n, b in bgler.items():
            z.writestr(n, b)
        for i, im in enumerate(resimler):
            d = 'c12_%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': mg.CW, 'h': mg.CH, 'name': ADLAR[i]}
            b = io.BytesIO(); ikonlar[i].save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    for f in os.listdir(bundle):
        if f.startswith('theme12.p'):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme12.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme12: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'c12_%02d.png' % (i + 1)))


if __name__ == '__main__':
    main()
