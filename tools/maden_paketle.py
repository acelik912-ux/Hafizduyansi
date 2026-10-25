#!/usr/bin/env python3
"""2. cüz "Değerli Madenler" tema paketini üretir: çizer (maden_ciz.py), Chrome ile PNG'ye çevirir (svg_png.mjs),
zip'ler ve bundle/theme2.pNN parçalarına böler. Ardından: python3 tools/flutter_varlik.py

    python3 tools/maden_paketle.py
"""
import io, json, os, shutil, subprocess, sys, tempfile, zipfile

from PIL import Image

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KOK, 'tools'))
import maden_ciz  # noqa: E402

PARCA = 8_000_000

with tempfile.TemporaryDirectory() as tmp:
    subprocess.run([sys.executable, os.path.join(KOK, 'tools', 'maden_ciz.py'), tmp], check=True)
    subprocess.run(['node', os.path.join(KOK, 'tools', 'svg_png.mjs'), '1.5', os.path.join(tmp, 'svg'), os.path.join(tmp, 'png')], check=True)
    png = os.path.join(tmp, 'png')
    proje = {'version': 7, 'kind': 'theme', 'cuz': 2, 'name': 'Değerli Madenler (2. Cüz)', 'sahne': 'magara', 'ek': 'madeni', 'birim': 'maden', 'tanim': 'madenli değerli taşlar mağarası',
             'ui': {'bgGarden': 'magara.jpg', 'bgForest': 'magara.jpg', 'bgPage': 'magara_sayfa.jpg', 'bgAyet': 'magara_sayfa.jpg'}, 'trees': {}}
    tampon = io.BytesIO()
    with zipfile.ZipFile(tampon, 'w', zipfile.ZIP_STORED) as z:
        for i in range(20):
            ad = 'maden%02d.png' % (i + 1)
            w, h = Image.open(os.path.join(png, ad)).size
            proje['trees'][str(i + 1)] = {'file': ad, 'w': w, 'h': h, 'name': maden_ciz.ADLAR[i]}
            z.write(os.path.join(png, ad), 'trees/' + ad)
            for k in range(5):  # her madenin 5 değerli taşı (siyah, kırmızı, sarı, yeşil, lacivert)
                z.write(os.path.join(png, 'tas_%d.png' % k), 'fruits/%02d_%d.png' % (i + 1, k))
        for ad in ('magara', 'magara_sayfa'):
            b = io.BytesIO()
            Image.open(os.path.join(png, ad + '.png')).convert('RGB').save(b, 'JPEG', quality=95)
            z.writestr('bg/%s.jpg' % ad, b.getvalue())
        z.writestr('project.json', json.dumps(proje, ensure_ascii=False, indent=1))
    veri = tampon.getvalue()

bundle = os.path.join(KOK, 'bundle')
for f in os.listdir(bundle):
    if f.startswith('theme2.p'):
        os.remove(os.path.join(bundle, f))
for n in range(0, len(veri), PARCA):
    open(os.path.join(bundle, 'theme2.p%02d' % (n // PARCA + 1)), 'wb').write(veri[n:n + PARCA])
print('theme2: %d bayt, %d parça' % (len(veri), (len(veri) + PARCA - 1) // PARCA))
