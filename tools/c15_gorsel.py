#!/usr/bin/env python3
"""15. cüz (İsrâ 17:1 – Kehf 18:74) görsellerini kullanıcının görsellerinden kurar (theme15: kale sahnesi). Yeniden çizmez;
yalnız beyaz zemini siler, boyutlandırır ve yerleştirir. Arka planlar (bg/) mevcut theme15 paketinden korunur.

    python3 tools/c15_gorsel.py [onizleme_klasoru]   # tools/c15_kaynak/NN_ad.jpg -> bundle/theme15.pNN
    python3 tools/flutter_varlik.py

Sıra, 12. cüzün sayfa sırasıdır (sayfa 1 = 11:6-12 ... sayfa 20 = 12:44-52). Hepsi tek başına nesne ('tek')."""
import glob, io, json, os, sys, zipfile
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_gorsel as mg
import kus_gorsel as kg

KAYNAK = os.path.join(KOK, 'tools', 'c15_kaynak')
# (ad, md, yük)
ESYALAR = [
    ('Kudüs Kalesi', 1000, 0),
    ('Kerek Kalesi', 1000, 0),
    ('Harput Kalesi', 1000, 0),
    ('Van Kalesi', 1000, 0),
    ('Elhamra Sarayı', 1000, 0),
    ('Kayıtbay Kalesi', 1000, 0),
    ('Buhara Ark Kalesi', 1000, 0),
    ('Şam Kalesi', 1000, 0),
    ('Kız Kulesi', 800, 0),
    ('Lahor Kalesi', 1000, 0),
    ('Travnik Kalesi', 1000, 0),
    ('Diyarbakır Surları', 1000, 0),
    ('Anadolu Hisarı', 1000, 0),
    ('İstanbul Surları', 1000, 0),
    ('Rumeli Hisarı', 1000, 0),
    ('Ahlat Kalesi', 1000, 0),
    ('Ani Kalesi', 1000, 0),
    ('Alamut Kalesi', 1000, 0),
    ('Hayber Kalesi', 1000, 0),
    ('Halep Kalesi', 1000, 0),
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
    eski = b''.join(open(f, 'rb').read() for f in sorted(glob.glob(os.path.join(bundle, 'theme15.p*'))))
    ez = zipfile.ZipFile(io.BytesIO(eski))
    proje = json.loads(ez.read('project.json'))
    # arka planlar: tools/sahne_bg.py kale (kale) -> bg/kale_sayfa.jpg, bg/kale_kemer.jpg
    import subprocess, tempfile
    gecici = tempfile.mkdtemp()
    subprocess.check_call([sys.executable, os.path.join(KOK, 'tools', 'sahne_bg.py'), gecici, 'kale'])
    bgler = {'bg/kale_sayfa.jpg': open(os.path.join(gecici, 'kale_sayfa.jpg'), 'rb').read(),
             'bg/kale_kemer.jpg': open(os.path.join(gecici, 'kale_kemer.jpg'), 'rb').read()}
    proje['sahne'] = 'kale'
    proje['ui'] = {'bgGarden': 'kale_sayfa.jpg', 'bgForest': 'kale_sayfa.jpg', 'bgPage': 'kale_sayfa.jpg', 'bgAyet': 'kale_kemer.jpg'}
    proje.update({'name': 'Kaleler (15. Cüz)', 'tanim': 'kaleler', 'birim': 'kale', 'trees': {}})
    resimler, ikonlar = [], []
    for i, (ad, md, yuk) in enumerate(ESYALAR):
        yol = kaynak_yolu(i)
        if not yol:
            sys.exit('eksik görsel: %02d_… (tools/c15_kaynak/) -> %s' % (i + 1, ad))
        im = mg.beyaz_sil(Image.open(yol), golge=(i != 13))  # bulutlu Güneş-Ay açık renkli: gölge silme kapalı
        resimler.append(kg.yerlestir(im, 'tek', md, yuk))
        ikonlar.append(kg.ikon(im, 'tek'))
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for n, b in bgler.items():
            z.writestr(n, b)
        for i, im in enumerate(resimler):
            d = 'c15_%02d.png' % (i + 1)
            b = io.BytesIO(); im.save(b, 'PNG', optimize=False)
            z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': mg.CW, 'h': mg.CH, 'name': ADLAR[i]}
            b = io.BytesIO(); ikonlar[i].save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    for f in os.listdir(bundle):
        if f.startswith('theme15.p'):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for n in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme15.p%02d' % (n // P + 1)), 'wb').write(veri[n:n + P])
    print('theme15: %d bayt, %d parça' % (len(veri), (len(veri) + P - 1) // P))
    if len(sys.argv) > 1:
        os.makedirs(sys.argv[1], exist_ok=True)
        for i, im in enumerate(resimler):
            im.save(os.path.join(sys.argv[1], 'c15_%02d.png' % (i + 1)))


if __name__ == '__main__':
    main()
