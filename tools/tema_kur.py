#!/usr/bin/env python3
"""Kodla çizilmiş cüz temalarını (c05..c15) bundle/themeN.pNN paketlerine çevirir.

    python3 tools/tema_kur.py [cüz ...] [--onizleme KLASÖR]   # varsayılan: 5..15
    python3 tools/flutter_varlik.py                           # paketleri flutter_app/assets/paket/ altına açar

Her cüz: tools/cNN.py (ADLAR, SAHNE, TANIM, BIRIM, EK, ciz) -> 720x960 SVG -> 1,5x PNG (1080x1440, dibi y~1425)
+ ikon (fruits/NN_k.png) + sahne arka planları (sahne_bg.py: <sahne>_sayfa.jpg, <sahne>_kemer.jpg).
Kullanıcı kendi illüstrasyonunu verince ilgili cüz bu araçla değil, kus_gorsel/bocek_gorsel gibi bir görsel aracıyla kurulmalı."""
import importlib, io, json, os, random, sys, tempfile, zipfile
from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import svg_png, sahne_bg
import kus_gorsel as kg

ADLAR = {5: 'Tarla ve Bostan', 6: 'Ağaçlar ve Orman', 7: 'Gök Cisimleri', 8: 'Çiftlik Hayvanları', 9: 'Dağlar', 10: 'Deniz Canlıları',
         11: 'Su ve Nimetleri', 12: 'Yûsuf Kıssası', 13: 'Hava Olayları', 14: 'Nahl Nimetleri', 15: 'Kehf ve İsrâ'}


def kur(n, onizleme=None):
    m = importlib.import_module('c%02d' % n)
    tmp = tempfile.mkdtemp()
    sd, pd = os.path.join(tmp, 'svg'), os.path.join(tmp, 'png')
    os.makedirs(sd)
    for i in range(20):
        sv = m.ciz(i, random.Random(1000 + i))
        open(os.path.join(sd, '%02d.svg' % (i + 1)), 'w', encoding='utf-8').write(str(sv))
    svg_png.donustur(1.5, sd, pd)
    sahne = m.SAHNE
    proje = {'version': 7, 'kind': 'theme', 'cuz': n, 'name': '%s (%d. Cüz)' % (ADLAR[n], n), 'sahne': sahne, 'ek': m.EK, 'birim': m.BIRIM,
             'tanim': m.TANIM, 'ui': {'bgGarden': sahne + '_sayfa.jpg', 'bgForest': sahne + '_sayfa.jpg', 'bgPage': sahne + '_sayfa.jpg', 'bgAyet': sahne + '_kemer.jpg'}, 'trees': {}}
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for i in range(20):
            im = Image.open(os.path.join(pd, '%02d.png' % (i + 1))).convert('RGBA')
            assert im.size == (1080, 1440), im.size
            d = 'c%02d_%02d.png' % (n, i + 1)
            b = io.BytesIO(); im.save(b, 'PNG'); z.writestr('trees/' + d, b.getvalue())
            proje['trees'][str(i + 1)] = {'file': d, 'w': 1080, 'h': 1440, 'name': m.ADLAR[i]}
            b = io.BytesIO(); kg.ikon(im, 'tek').save(b, 'PNG')
            for k in range(5):
                z.writestr('fruits/%02d_%d.png' % (i + 1, k), b.getvalue())
            if onizleme:
                os.makedirs(onizleme, exist_ok=True); im.save(os.path.join(onizleme, d))
        for ad, fn in ((sahne + '_sayfa.jpg', sahne_bg.sayfa), (sahne + '_kemer.jpg', sahne_bg.kemer)):
            b = io.BytesIO()
            fn(sahne).save(b, 'JPEG', quality=93 if 'sayfa' in ad else 94, subsampling=0)
            z.writestr('bg/' + ad, b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()
    bundle = os.path.join(KOK, 'bundle')
    for f in os.listdir(bundle):
        if f.startswith('theme%d.p' % n):
            os.remove(os.path.join(bundle, f))
    P = 8_000_000
    for k in range(0, len(veri), P):
        open(os.path.join(bundle, 'theme%d.p%02d' % (n, k // P + 1)), 'wb').write(veri[k:k + P])
    print('theme%d: %.1f MB, %d parça' % (n, len(veri) / 1e6, (len(veri) + P - 1) // P), flush=True)


def main():
    a = sys.argv[1:]
    on = None
    if '--onizleme' in a:
        j = a.index('--onizleme'); on = a[j + 1]; a = a[:j] + a[j + 2:]
    for n in ([int(x) for x in a] or range(5, 16)):
        kur(n, on and os.path.join(on, 'c%02d' % n))


if __name__ == '__main__':
    main()
