#!/usr/bin/env python3
"""bundle/ içindeki parçalı paketleri (cuz1.pNN, theme1.pNN, ses1.pNN ...) birleştirip Flutter varlıklarına açar:
    python3 tools/flutter_varlik.py            ->  flutter_app/assets/paket/<ad>/...
Dosyalar olduğu gibi kopyalanır (yeniden sıkıştırma / küçültme yok). Ardından pubspec.yaml'daki
assets listesi otomatik güncellenir (Flutter klasörleri alt klasörleriyle birlikte saymaz, her klasör tek tek yazılır)."""
import io, os, re, shutil, sys, zipfile

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = os.path.join(KOK, 'bundle')
APP = os.path.join(KOK, 'flutter_app')
HEDEF = os.path.join(APP, 'assets', 'paket')

adlar = sorted({re.sub(r'\.p\d\d$', '', f) for f in os.listdir(BUNDLE) if re.search(r'\.p\d\d$', f)})
if not adlar:
    sys.exit('bundle/ içinde parça bulunamadı')
shutil.rmtree(HEDEF, ignore_errors=True)
klasorler = set()
for ad in adlar:
    parcalar = sorted(f for f in os.listdir(BUNDLE) if re.fullmatch(re.escape(ad) + r'\.p\d\d', f))
    veri = b''.join(open(os.path.join(BUNDLE, p), 'rb').read() for p in parcalar)
    with zipfile.ZipFile(io.BytesIO(veri)) as z:
        for n in z.namelist():
            if n.endswith('/'):
                continue
            yol = os.path.join(HEDEF, ad, n)
            os.makedirs(os.path.dirname(yol), exist_ok=True)
            with open(yol, 'wb') as o:
                o.write(z.read(n))
            klasorler.add(os.path.relpath(os.path.dirname(yol), APP).replace(os.sep, '/') + '/')
    print(f'{ad}: {len(parcalar)} parça açıldı')

# pubspec.yaml: '# PAKET-BAŞ' ile '# PAKET-SON' arası yeniden yazılır
ps = os.path.join(APP, 'pubspec.yaml')
metin = open(ps, encoding='utf-8').read()
satirlar = '\n'.join('    - ' + k for k in sorted(klasorler))
yeni = re.sub(r'(    # PAKET-BAŞ\n).*?(    # PAKET-SON)', lambda m: m.group(1) + satirlar + '\n' + m.group(2), metin, flags=re.S)
open(ps, 'w', encoding='utf-8').write(yeni)
print('pubspec.yaml güncellendi:', len(klasorler), 'klasör')
